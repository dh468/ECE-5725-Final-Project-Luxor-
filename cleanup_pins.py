#!/usr/env python

import time
import RPi.GPIO as GPIO
import sys

def CleanPin(pin):
	# set up pins
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin, GPIO.OUT)
	pwm = GPIO.PWM(pin, 50)
	pwm.start(0)

	time.sleep(1)
	GPIO.cleanup()

if __name__ == '__main__':
	pin = int(sys.argv[1])
	CleanPin(pin)
