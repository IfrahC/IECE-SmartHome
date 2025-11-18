from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import pigpio
factory=PiGPIOFactory()
servo=Servo(18,pin_factory=factory)
while True:
    servo.min()
    sleep(2)
#     servo.mid()
#     sleep(2)
    servo.max()
    sleep(2)
# pi.set_servo_pulsewidth(servo_pin,1500)
# sleep(2)
# pi.set_servo_pulsewidth(servo_pin,1000)
# sleep(2)
# pi.set_servo_pulsewidth(servo_pin,2000)
# sleep(2)
#     pi.set_servo_pulsewidth(servo_pin,0)
# sleep(2)
#     pi.stop()