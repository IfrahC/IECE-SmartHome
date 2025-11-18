from gpiozero import LED,DistanceSensor, Button, PWMLED,Servo,MotionSensor
from time import sleep, time
from guizero import App, Text, Box
from signal import pause
import adafruit_dht
import board


led1=LED(2)
led2=LED(4)
led3=LED(18)
trig=17
echo=27
led2.on()
pir=MotionSensor(10)
# servo=Servo(18,min_pulse_width=0.0005,max_pulse_width=0.0024)
# servo.value=0.0
dht_device = adafruit_dht.DHT22(board.D3)
sensor=DistanceSensor(echo=echo,trigger=trig,max_distance=1.5)

app = App(title="Project", width = 400, height=220)

top_spacer = Box(app, height=20)
container = Box(app, layout="grid")

gateStat = "Unknown"

Text(container, text = "Gate Status", grid=[0,2], align="left", size = 16)
gateStatus = Text(container, text = gateStat, grid=[1,2], align="right", size = 16)

def setAngle(angle):
    value = (angle/90) - 1
    value = max(-1, min(1,value))
#     servo.value = value
#     sleep(1)
    
def detected():
    global gateStat
    led2.off()
    led1.on()
    gateStat = "Detected"
    gateStatus.value = gateStat
#     setAngle(90)

#     sleep
    sleep(0.5)
    
    
def not_detected():
    global gateStat
    led1.off()
    led2.on()
    gateStat = "Not Detected"
    gateStatus.value = gateStat
    sleep(0.5)
#     setAngle(50)
    
    
def check_distance():
    distance=(sensor.distance)*100
    print(f"{distance:.2f} cm")
    if distance>40:
        
        not_detected()
        
    else:
        
        detected()
def pir_on():
    print("motion detected")
    led3.on()
    sleep(3)
def pir_off():
    print(" motion not detected")
    led3.off()
pir.when_motion=pir_on
pir.when_no_motion=pir_off
print("PIR initialized")
while True:
    check_distance()
    
while True:
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
# check_distance()
# app.repeat(100 , check_distance)
# app.display()

