#!/bin/python
#Authors: Martin Herrera and Deepthi Krovvidi 

import RPi.GPIO as GPIO         #import RPi.GPIO module
import time
import sys

def RunCal(pin):

        GPIO.setmode(GPIO.BCM)          # choose BCM
        GPIO.setup(pin, GPIO.OUT)       # set pin as an output
        pwm = GPIO.PWM(pin, 50)         # setting pin and frequency
        pwm.start(0)                    # start LED on 0% duty cycle (off)
	pwmgo = 6

        try:

                while True:
                       #print('Sleeping')
                        pwm.ChangeDutyCycle(pwmgo)
                        time.sleep(5)
                        pwm.ChangeDutyCycle(pwmgo+0.5)
			time.sleep(5)
			pwm.ChangeDutyCycle(pwmgo+1.0)
			time.sleep(5)
                        pwm.ChangeDutyCycle(pwmgo+1.5)
			time.sleep(3)
        except KeyboardInterrupt:
                pwm.stop()              # stop PWM output
                GPIO.cleanup()          # cleanup GPIO on CTRL+C Exit
                return
if __name__ == '__main__':
        pin = int(sys.argv[1])
        RunCal(pin)

