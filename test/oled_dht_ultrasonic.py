from time import sleep
from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory

import board
import adafruit_dht

from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import Image, ImageDraw, ImageFont


# -------------------------------------------------
# INITIAL SETUP
# -------------------------------------------------

# --- Ultrasonic Sensor ---
factory = PiGPIOFactory()
sensor = DistanceSensor(echo=27, trigger=17, max_distance=1.5, pin_factory=factory)

# --- DHT22 Sensor ---
dht_device = adafruit_dht.DHT11(board.D22)

# --- OLED SH1106 ---
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)
font = ImageFont.load_default()


# -------------------------------------------------
# MAIN LOOP
# -------------------------------------------------

while True:
    # ----- READ DISTANCE -----
    distance_cm = sensor.distance * 100

    # Determine gate status
    gate_status = "Detected" if distance_cm <= 40 else "Not Detected"

    # ----- READ TEMP/HUM -----
    temp_c = None
    hum = None

    try:
        temp_c = dht_device.temperature
        hum = dht_device.humidity
    except RuntimeError:
        # DHT22 throws errors often, ignore a single bad reading
        pass

    # ----- OLED Update -----
    try:
        # Make blank image
        image = Image.new("1", (device.width, device.height))
        draw = ImageDraw.Draw(image)

        # Ultrasonic values
        draw.text((5, 5), f"Gate: {gate_status}", font=font, fill=255)
        draw.text((5, 20), f"Dist: {distance_cm:.1f} cm", font=font, fill=255)

        # Temp + humidity (if valid)
        if temp_c is not None and hum is not None:
            draw.text((5, 35), f"Temp: {temp_c:.1f}C", font=font, fill=255)
            draw.text((5, 50), f"Hum:  {hum:.1f}%", font=font, fill=255)
        else:
            draw.text((5, 35), f"Temp/Hum: --", font=font, fill=255)

        device.display(image)

    except Exception as e:
        print("OLED Error:", e)
        
    except KeyboardInterrupt:
        print("Interrupted")
        dht_device.close()

    # ----- Print to terminal -----
    print(f"Gate: {gate_status} | Distance: {distance_cm:.1f} cm")

    if temp_c is not None and hum is not None:
        print(f"Temp: {temp_c:.1f}°C  Humidity: {hum:.1f}%")

    print("-" * 40)
    
    sleep(1)

