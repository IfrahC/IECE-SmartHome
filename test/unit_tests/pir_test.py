from gpiozero import MotionSensor
from time import sleep

# Replace 22 with the GPIO pin your PIR is connected to
pir = MotionSensor(22)

print("PIR test started. Move in front of the sensor...")

try:
    while True:
        if pir.motion_detected:
            print("Motion detected!")
        else:
            print("No motion")
        sleep(0.5)

except KeyboardInterrupt:
    print("Exiting PIR test...")
    pir.close()
