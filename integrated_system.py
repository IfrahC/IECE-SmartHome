from gpiozero import LED, DistanceSensor, MotionSensor
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep, time
from guizero import App, Text, Box
from signal import pause

# --- Servo + pigpio ---
# import pigpio
factory = PiGPIOFactory()
# servo = Servo(18, pin_factory=factory)

# --- DHT22 ---
# import adafruit_dht
# import board

# --- OLED ---
# from luma.core.interface.serial import i2c
# from luma.oled.device import sh1106
# from PIL import Image, ImageDraw, ImageFont

# -----------------------------------------
# INITIAL SETUP
# -----------------------------------------

# LEDs
# led1 = LED(2)
# led2 = LED(4)
# led3 = LED(18)
# led2.on()

# Distance Sensor
trig = 17
echo = 27
sensor = DistanceSensor(echo=echo, trigger=trig, max_distance=1.5, pin_factory=factory)

# PIR
# pir = MotionSensor(10)

# DHT22
# dht_device = adafruit_dht.DHT22(board.D3)

# OLED
# serial = i2c(port=1, address=0x3C)
# device = sh1106(serial)
# font = ImageFont.load_default()

# GUI
# app = App(title="Project", width=400, height=220)
# top_spacer = Box(app, height=20)
# container = Box(app, layout="grid")

gateStat = "Unknown"

# Text(container, text="Gate Status", grid=[0,2], align="left", size=16)
# gateStatus = Text(container, text=gateStat, grid=[1,2], align="right", size=16)

# Text(container, text="Distance", grid=[0,3], align="left", size=16)
# distanceDisplay = Text(container, text="-- cm", grid=[1,3], align="right", size=16)

# Text(container, text="Temp", grid=[0,4], align="left", size=16)
# tempDisplay = Text(container, text="-- °C", grid=[1,4], align="right", size=16)

# Text(container, text="Humidity", grid=[0,5], align="left", size=16)
# humDisplay = Text(container, text="-- %", grid=[1,5], align="right", size=16)


# -----------------------------------------
# FUNCTIONS
# -----------------------------------------

# def setAngle(angle):
#     value = (angle/90) - 1
#     value = max(-1, min(1, value))
    # servo.value = value   # uncomment when servo installed
    # sleep(1)


def detected():
    global gateStat
    # led2.off()
    # led1.on()
    gateStat = "Detected"
    # gateStatus.value = gateStat
    # setAngle(90)
    sleep(0.5)


def not_detected():
    global gateStat
    # led1.off()
    # led2.on()
    gateStat = "Not Detected"
    # gateStatus.value = gateStat
    # setAngle(50)
    sleep(0.5)


def check_distance():
    distance = (sensor.distance) * 100
    # distanceDisplay.value = f"{distance:.2f} cm"
    print(f"{distance:.2f} cm")

    if distance > 40:
        not_detected()
    else:
        detected()

    # update_oled()


# def read_dht():
#     try:
#         temperature_c = dht_device.temperature
#         humidity = dht_device.humidity

#         if temperature_c is not None and humidity is not None:
#             tempDisplay.value = f"{temperature_c:.1f}°C"
#             humDisplay.value = f"{humidity:.1f}%"
#             print(f"Temp: {temperature_c:.1f} C  Hum: {humidity:.1f}%")

#     except RuntimeError as e:
#         print("Error reading DHT22:", e.args[0])

#     update_oled()


# def update_oled():
#     try:
#         image = Image.new("1", (device.width, device.height))
#         draw = ImageDraw.Draw(image)

#         draw.text((5, 5), f"Gate: {gateStatus.value}", font=font, fill=255)
#         draw.text((5, 20), f"Dist: {distanceDisplay.value}", font=font, fill=255)
#         draw.text((5, 35), f"Temp: {tempDisplay.value}", font=font, fill=255)
#         draw.text((5, 50), f"Hum: {humDisplay.value}", font=font, fill=255)

    #     device.display(image)
    # except Exception as e:
    #     print("OLED error:", e)


# -----------------------------------------
# PIR CALLBACKS (your original logic)
# -----------------------------------------

# def pir_on():
#     print("motion detected")
#     led3.on()
#     sleep(3)

# def pir_off():
#     print("motion not detected")
#     led3.off()

# pir.when_motion = pir_on
# pir.when_no_motion = pir_off

# print("PIR initialized")


# -----------------------------------------
# GUI Update Loops
# -----------------------------------------

while True:
    check_distance()
    sleep(0.5)

# app.repeat(300, check_distance)     # every 0.3s
# app.repeat(1500, read_dht)         # every 1.5s

# Start GUI
# app.display()
