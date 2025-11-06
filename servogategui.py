from guizero import App, Text, Box
from gpiozero import LED, DistanceSensor

led1 = LED(2)
led2 = LED(4)
trigger = 17
echo = 27
sensor = DistanceSensor(echo=echo, trigger=trigger, max_distance=1.5)

app = App(title="Project", width=480, height=220)

top_spacer = Box(app, height=20)
container = Box(app, layout="grid")

gateStat = -1
gateStat = "Unknown"

Text(container, text="Gate Status", grid=[0, 2], align="left", size=16)
gateStatus = Text(container, text=gateStat, grid=[1, 2], align="right", size=16)

def detected():
    global gateStat
    led2.off()
    led1.on()
    gateStat = "Open"
    gateStatus.value = gateStat

def not_detected():
    global gateStat
    led1.off()
    led2.on()
    gateStat = "Closed"
    gateStatus.value = gateStat

def check_distance():
    distance = sensor.distance * 100
    print("Distance: %.2f cm" % distance)
    if distance > 40:
        not_detected()
    else:
        detected()

check_distance()
app.repeat(100, check_distance) # poll every 100 ms

app.display()