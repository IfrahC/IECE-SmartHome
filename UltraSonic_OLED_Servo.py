from gpiozero import Servo, DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import Image, ImageDraw, ImageFont

# -------------------------------------------------
# INITIAL SETUP
# -------------------------------------------------

# --- Factory for pigpio ---
factory = PiGPIOFactory()

# --- Servo ---
servo = Servo(13, pin_factory=factory)

# --- Ultrasonic Sensor ---
sensor = DistanceSensor(echo=27, trigger=17, max_distance=1.5, pin_factory=factory)

# --- OLED ---
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)
font = ImageFont.load_default()

# --- Global variables ---
gateStat = "Unknown"
gateOpen = False
distanceDisplay = -1

# -------------------------------------------------
# FUNCTIONS
# -------------------------------------------------

# def move_servo(angle):
#     """Move servo to a specific angle in degrees (0 to 180)."""
#     # Convert 0-180° to -1 to 1 for gpiozero Servo
#     value = (angle / 90.0) - 1
#     value = max(-1, min(1, value))  # clamp to valid range
#     servo.value = value
#     sleep(0.5)

def detected():
    global gateStat, gateOpen
    if not gateOpen:
        gateStat = "Gate OPEN"
        gateOpen = True
        servo.max()
        print("Detected")
#         move_servo(90)  # move servo to 90° when something is detected
#         sleep(2)
#         move_servo(0)
#         sleep(1)

def not_detected():
    global gateStat, gateOpen
    if gateOpen:
        gateStat = "Gate CLOSED"
        gateOpen = False
        servo.min()
        print("Not Detected")

def check_distance():
    distance = sensor.distance * 100
    global distanceDisplay
    distanceDisplay = f"{distance:.2f} cm"
    print(f"{distance:.2f} cm")

    if distance > 40:
        not_detected()
    else:
        detected()
    
    update_oled(distance)

def update_oled(distance):
    try:
        image = Image.new("1", (device.width, device.height))
        draw = ImageDraw.Draw(image)
        draw.text((5, 5), gateStat, font=font, fill=255)
        draw.text((5, 20), f"{distance:.2f} cm", font=font, fill=255)
        device.display(image)
    except Exception as e:
        print("OLED error:", e)

# -------------------------------------------------
# MAIN LOOP
# -------------------------------------------------

try:
    while True:
        check_distance()
        sleep(0.5)

except KeyboardInterrupt:
    print("Exiting...")
    servo.detach()       # safely release servo
    sensor.close()

