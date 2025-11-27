from gpiozero import Servo, DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from luma.core.interface.serial import pcf8574
from luma.oled.device import hd44780
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
serial = pcf8574(port=1, address=0x27)
device = hd44780(serial, width = 16, height = 2)

# --- Global variables ---
gateStat = "Unknown"
gateOpen = False
distanceDisplay = -1
device.text = ""

# -------------------------------------------------
# FUNCTIONS
# -------------------------------------------------

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
        device.text = f"{gateStat}\n{distance:.2f} cm"
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

