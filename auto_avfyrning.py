import RPi.GPIO as GPIO
import smbus
import time

bus = smbus.SMBus(1)
address = 0x08

min_pwm = 982
max_pwm = 2006

valve_pin = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(valve_pin, GPIO.OUT)

p = GPIO.PWM(17, 50)
p.start(12)

try:
	while True:
		tilt_val = (int.from_bytes(bus.read_i2c_block_data(address, 2, 2), "big") - min_pwm) / (max_pwm - min_pwm)
		fire_val = (int.from_bytes(bus.read_i2c_block_data(address, 1, 2), "big") - min_pwm) / (max_pwm - min_pwm)
		servo_val = 2.5*tilt_val + 10
		p.ChangeDutyCycle(max(servo_val,0))
		GPIO.output(valve_pin, fire_val > 0.5)
		print(tilt_val, fire_val, servo_val)
		time.sleep(0.01)
except KeyboardInterrupt:
	print("Stopping")
	p.ChangeDutyCycle(12)
	p.stop()
	GPIO.cleanup()
p.stop()
