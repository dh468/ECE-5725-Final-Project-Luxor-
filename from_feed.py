#!/usr/env python
#import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import cv2.aruco as aruco
import numpy as np
import RPi.GPIO as GPIO
import sys

def FromFeed(sweep, id_Sweep, b_pin, u_pin,track, id_Track):
    
    # Need to initalize the camera for raw camera capture
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))

    # Allow the camera to warmup
    time.sleep(0.1)

    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):   
        # grab the raw NumPy array representing the image, then initialize the timestamp and occupied/unoccupied text
        gray = frame.array
        gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        parameters =  aruco.DetectorParameters_create()
        
        #lists of ids and the corners beloning to each id
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        
        print(ids)
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        break
        
    if sweep:
##        # set up the pins
##        GPIO.setmode(GPIO.BCM)
##        GPIO.setup(b_pin, GPIO.out)
##        GPIO.setup(u_pin, GPIO.out)
##        b_pwm = GPIO.PWM(b_pin, 50)        # setting pin and frequency
##        u_pwm = GPIO.PWM(u_pin, 50)        # setting pin and frequency
##        b_pwm.start(0)
##        u_pwm.start(0)
##                
##        # Set the duty cycle in incrememnts
##        b_DC = 4
##        u_DC = 4
##        
##        while id_Sweep not in ids:
##            b_pwm.ChangeDutyCycle(b_DC)
##            u_pwm.ChangeDutyCycle(u_DC)
##            
##            b_DC = b_DC + 0.1
##            u_DC = u_DC + 0.1
##        try:
##
##                while True:
##                       #print('Sleeping')
##                        pwm.ChangeDutyCycle(4)
##                        time.sleep(1)
##                        pwm.ChangeDutyCycle(5)
##                        time.sleep(1)
##                        pwm.ChangeDutyCycle(7)
##                        time.sleep(1)
##                        pwm.ChangeDutyCycle(8)
##                        time.sleep(3)
##        except KeyboardInterrupt:
##                pwm.stop()              # stop PWM output
##                GPIO.cleanup()          # cleanup GPIO on CTRL+C Ex
##        
##            
        print('sweep')
        
    if track:
        # get the index of the requested id 
        index = -1
        i = 0
        for i in range(0,len(ids)):
            if id_Track == ids[i]:
                index = i
                print(index)
        if index != -1:
            want_corners = corners[index]
            want_corners = np.asarray(want_corners)
            
            # calculate center
            length = want_corners.shape[0]
            sum_x = np.sum(want_corners[:,0])
            sum_y = np.sum(want_corners[:,1])
            center = (sum_x/length, sum_y/length)            
    return center
        
if __name__ == '__main__':
    sweep = True
    id_Sweep = 1
    b_pin = 19
    u_pin = 26
    track = True
    id_Track = 3
    center = FromFeed(sweep, id_Sweep, b_pin, u_pin, track, id_Track)
    print(center)

