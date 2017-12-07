#!/usr/env python

from picamera import PiCamera
import time
import cv2
import cv2.aruco as aruco
import numpy as np
import sys
import pigpio
from picamera.array import PiRGBArray
#camera = PiCamera()

def FromFeed(id_Track, camera, b_pin, u_pin, bDC, uDC):
        # Need to initalize the camera for raw camera capture
        camera.resolution = (640, 480)
        camera.framerate = 32
        rawCapture = PiRGBArray(camera, size=(640, 480))

        # Allow the camera to warmup
        time.sleep(0.1)

        # Initalize and set up pins for servo control and send the motors to the previously known location of the tag
        pi = pigpio.pi()
        pi.set_servo_pulsewidth(b_pin, bDC)
        pi.set_servo_pulsewidth(u_pin, uDC)
	
	time.sleep(2)
	
        lost = 0
        #center = [320, 240]
        # capture frames from the camera
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                # grab the raw NumPy array representing the image, then initialize the timestamp and occupied/unoccupied text
                gray = frame.array
                gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
                aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
                parameters =  aruco.DetectorParameters_create()

                #lists of ids and the corners beloning to each id
                corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

                #print(ids)
                # clear the stream in preparation for the next frame
                # show the frame
		#cv2.imshow("Frame", gray)
		#key = cv2.waitKey(1) & 0xFF
		rawCapture.truncate(0)
                break

        if ids == None:
                lost = 1;
        else:
                # get the index of the requested id
                index = -1
                for i in range(0,len(ids)):
                        if id_Track == ids[i]:
                                index = i
                if index != -1:
                        #print('here')
                        want_corners = corners[index]
                        want_corners = np.asarray(want_corners)

                # calculate center
                length = 4
                sum_x = np.sum(want_corners[:,0])
                sum_y = np.sum(want_corners[:,1])
                center = (sum_x/length, sum_y/length)
		print('center from track: ')
		print(center)
	#print(lost)
        return center, lost

def dc(base_servo, camera_servo, ocx, ocy, bDC, uDC):
        # set pins as outputs
        pi = pigpio.pi()
	print('x and y: ')
	print(ocx)
	print(ocy)

        # set each pin and frequency

        if ocx < 140:
                scalar_l = 1
        elif ocx > 180:
                scalar_l = -1
        else:
                scalar_l = 0

        if ocy < 100:
                scalar_w = 1
        elif ocy > 140:
                scalar_w = -1
        else:
                scalar_w = 0

        # calculate change in phi
        add_phi_length = ((abs(ocx-160))*30)/160
        add_phi_width = ((abs(ocy-120))*30)/120
        print('x phi and y phi: ') 
	print(add_phi_length)
	print(add_phi_width)
	print('scalar x and scalar y: ')
	print(scalar_l)
	print(scalar_w)
	addDC_length = (add_phi_length*333)/(30*2)
        addDC_width = (add_phi_width*333)/(30*2)
        
	newDC_length = bDC + scalar_l*addDC_length
        newDC_width = uDC + scalar_w*addDC_width
	print('new dc x and nwe dc y: ')
	print(newDC_length)
	print(newDC_width)
	#pi.set_servo_pulsewidth(base_servo, newDC_length)
        #pi.set_servo_pulsewidth(camera_servo, newDC_width)
	
	time.sleep(2)
        return newDC_length, newDC_width


if __name__ == '__main__':
        id_Track = 3
        camera = PiCamera()
        b_pin = 26
        u_pin = 19
        bDC = 1500
        uDC = 2050
        while True:
		center, lost = FromFeed(id_Track, camera, b_pin, u_pin, bDC, uDC)
        	#print(center)
		
        	dc_length, dc_width = dc(b_pin, u_pin, center[0], center[1], bDC, uDC)
		#print(dc_length)
		#print(dc_width)
		bDC = dc_length
		uDC = dc_width
