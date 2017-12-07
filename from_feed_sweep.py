#!/usr/env python
# Author: Deepthi Krovvidi
# Code for sweeping and collecting ids for 5725 project

import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import cv2.aruco as aruco
import numpy as np 
import sys
import pigpio

# Setup outside to prevent issues
camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640,480))

# Allow the camera to warmup
time.sleep(0.1) 

# Initialize and set up pins 
pi = pigpio.pi()

def FromFeed(id_Sweep, b_pin, u_pin, lost, track_id):
    bDC = 700
    uDC = 1800

    # Setting up id_List and found for keeping track of which variables are found
    id_List = [];
    bDC_List = [];
    uDC_List = [];
    found = 0; 
    emptyframe = 1
    # Here is where the function sweeps
    while found!=id_Sweep and emptyframe:
	# Set servo speed values here
	pi.set_servo_pulsewidth(b_pin, bDC)
	pi.set_servo_pulsewidth(u_pin, uDC)	
	time.sleep(0.5)

        # capture frames from the camera
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):   
        
            # grab the raw NumPy array representing the image, then initialize the timestamp and occupied/unoccupied text
            gray = frame.array
            gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
            aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
            parameters =  aruco.DetectorParameters_create()
        
            #lists of ids and the corners beloning to each id
            corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
	    gray = aruco.drawDetectedMarkers(gray, corners, ids) 
	    
	    #show the frame
	    #cv2.imshow("Frame", gray)
	    #key = cv2.waitKey(1) & 0xFF

            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)
	    break
        
        time.sleep(0.1)
	
        if ids != None:
	    if lost == 1:
		for i in ids:
			if i[0] == track_id:
				found = id_Sweep
				bDC_List.append(bDC)
				uDC_List.append(uDC)
				id_List.append(track_id)
				emptyframe = 0
            else:
		for i in ids:
                	if i not in id_List and found != id_Sweep:
                    		id_List.append(i[0])
		    		bDC_List.append(bDC)
		    		uDC_List.append(uDC)
                    		found = found+1
                    		#print(id_List)
                    		#print(found)

        time.sleep(0.5) 
        if bDC < 2300 and uDC < 2300:
            bDC = bDC + 150
        elif bDC > 2300 and uDC < 2300:
            bDC = 700
            uDC = uDC + 100
	elif uDC > 2200:
	    emptyframe = 0
	    found = id_Sweep 
	#print(bDC)
	#print(uDC)
	#print(emptyframe)
    return id_List, found, camera, bDC_List, uDC_List, emptyframe


if __name__ == '__main__':
	b_pin = 26
	u_pin = 19
	id_Sweep = 2
	lost = 1
	track_id = 3
	found_ids, found, camera, bDC_List, uDC_List, emptyframe = FromFeed(id_Sweep, b_pin, u_pin, lost, track_id)
