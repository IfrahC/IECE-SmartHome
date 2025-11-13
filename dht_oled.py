import time
import board
import adafruit_dht
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import Image, ImageDraw, ImageFont

# --- Initialize DHT22 Sensor ---
dht_device = adafruit_dht.DHT22(board.D4)

# --- Initialize OLED Display (SH1106) ---
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

# --- Font setup ---
font = ImageFont.load_default()

while True:
    try:
        temperature_c = dht_device.temperature
        humidity = dht_device.humidity

        if temperature_c is not None and humidity is not None:
            temperature_f = temperature_c * (9 / 5) + 32

            # Create blank image for drawing
            image = Image.new("1", (device.width, device.height))
            draw = ImageDraw.Draw(image)

            # Draw text on display
            draw.text((5, 10), "Temp: {:.1f}°C".format(temperature_c), font=font, fill=255)
            draw.text((5, 25), "Hum: {:.1f}%".format(humidity), font=font, fill=255)

            # Display image
            device.display(image)

            print(f"Temp: {temperature_c:.1f} C / {temperature_f:.1f} F  Humidity: {humidity:.1f}%")

        else:
            print("Sensor returned None values, retrying...")

    except RuntimeError as e:
        print("Error reading DHT22:", e.args[0])

    time.sleep(2.0)
