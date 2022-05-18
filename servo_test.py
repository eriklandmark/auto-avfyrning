import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

p = GPIO.PWM(17, 50)
p.start(12)

try:
	while True:
		p.ChangeDutyCycle(12)
		time.sleep(2)
		p.ChangeDutyCycle(10.5)
		time.sleep(2)
except KeyboardInterrupt:
	print("Stopping")
	p.ChangeDutyCycle(12)
	p.stop()
	GPIO.cleanup()
p.stop()
