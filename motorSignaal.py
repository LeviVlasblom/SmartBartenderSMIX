import RPi.GPIO as GP
import time

GP.setmode(GP.BCM)
GP.setup(18, GP.OUT)

trigger = GP.PWM(18, 1000)
trigger.start(40.0)
#GP.output(18, 1)

time.sleep(3)
trigger.ChangeDutyCycle(60)
#GP.output(18, 0)

time.sleep(3)
trigger.ChangeDutyCycle(80)

time.sleep(3)
trigger.stop()
time.sleep(3)
GP.cleanup()