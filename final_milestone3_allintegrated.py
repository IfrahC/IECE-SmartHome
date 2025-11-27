from gpiozero import Servo, DistanceSensor,LED,MotionSensor
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from luma.core.interface.serial import pcf8574
from luma.lcd.device import hd44780
from PIL import Image, ImageDraw, ImageFont
import time
import board
import adafruit_dht

# -------------------------------------------------
# INITIAL SETUP
# -------------------------------------------------

# --- Factory for pigpio ---
factory = PiGPIOFactory()

#  --- LED ---
led1=LED(9)
relay=LED(19)
led2=LED(3)
led1.on()
led2.off()

#  --- PIR ---
pir=MotionSensor(6,  pin_factory = factory)
 
# --- Servo ---
servo = Servo(13, pin_factory = factory, min_pulse_width = 0.001, max_pulse_width=0.002)

# --- Ultrasonic Sensor ---
sensor = DistanceSensor(echo=27, trigger=17, max_distance=1.5, pin_factory=factory)
servo.min()

# --- OLED ---
# serial = pcf8574(port=1, address=0x27)
# device = hd44780(serial,width=16,height=2)

# --- DHT ---
dht_device = adafruit_dht.DHT11(board.D22)

# --- Global variables ---
gateStat = "Unknown"
gateOpen = False
distanceDisplay = -1
temp_c = humidity = None
# device.text=""

# -------------------------------------------------
# FUNCTIONS
# -------------------------------------------------

def detected():
    global gateStat, gateOpen
    if not gateOpen:
        gateStat = "Gate OPEN"
        gateOpen = True
        led1.on()
        led2.off()
        servo.max()
        sleep(2)
        print("Detected")
        relay.on()


def not_detected():
    global gateStat, gateOpen
    if gateOpen:
        gateStat = "Gate CLOSED"
        gateOpen = False
        led1.off()
        led2.on()
        servo.min()
        sleep(3)
        print("Not Detected")
        relay.off()


def check_distance():
    distance = sensor.distance * 100
    global distanceDisplay
    distanceDisplay = f"{distance:.2f} cm"
    print(f"{distance:.2f} cm")

    if distance > 40:
        not_detected()
    else:
        detected()
        
def read_DHT():
    global temp_c, humidity
    try:
        # Get both temperature and humidity in a single line
        temperature_c = dht_device.temperature
        humidity = dht_device.humidity
        
        # Convert to Fahrenheit if needed
        temperature_f = temperature_c * (9 / 5) + 32
        
        # Print the results
        print("Temp: {:.1f} C / {:.1f} F Humidity: {}%".format(temperature_c, temperature_f, humidity))

    except RuntimeError as e:
        # Reading a sensor is not always successful, so retry
        print("Error reading data: {}".format(e.args[0]))
        
    time.sleep(2.0) # Wait for 2 seconds before repeating
    
def check_motion():
    motion_status = "Motion Detected" if pir.motion_detected else "No Motion"
    print(motion_status)
    
#     update_oled(distance)

# def update_oled(distance):
#      try:
#         while True:
#             device.text=f"{distance:.2f} cm"
#             sleep(0.5)
#      except Exception as e:
#          print("OLED error:", e)

# -------------------------------------------------
# MAIN LOOP
# -------------------------------------------------

try:
    while True:
        check_distance()
        read_DHT()
        check_motion()
        sleep(0.5)

except KeyboardInterrupt:
    print("Exiting...")
