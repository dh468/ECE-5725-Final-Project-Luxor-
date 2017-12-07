#!/usr/env python
#import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import cv2.aruco as aruco
import numpy as np
import sys

def FromFeed(id_Track, camera, b_pin, u_pin, bDC, uDC):
	# Need to initalize the camera for raw camera capture
	camera.resolution = (640, 480)
	camera.framerate = 32
	rawCapture = PiRGBArray(camera, size=(640, 480))

	# Allow the camera to warmup
	time.sleep(0.1)

	lost = 0
	center = [320, 240]
	# capture frames from the camera
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):   
        	# grab the raw NumPy array representing the image, then initialize the timestamp and occupied/unoccupied text
      		gray = frame.array
        	gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
        	aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        	parameters =  aruco.DetectorParameters_create()
        
        	#lists of ids and the corners beloning to each id
        	corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        	# clear the stream in preparation for the next frame
        	rawCapture.truncate(0)
        	break
        
        if ids == None:
		lost = 1;
 	else:	
		#want_corners=[[315, 235], [325,235], [315,245], [325,245]]
		#want_corners[0,0] = [315, 235]
		#want_corners[0,1] = [325, 235]
		#want_corners[0,2] = [315, 245]
		#want_corners[0,3] = [325, 245]
		# get the index of the requested id 
        	index = -1
        	for i in range(0,len(ids)):
        		if id_Track == ids[i]:
       				index = i
        	if index != -1:
       			want_corners = corners[index]
			# calculate center
        		length = 4
			pt1 = want_corners[0,0]
			pt2 = want_corners[0,1]
			pt3 = want_corners[0,2]
			pt4 = want_corners[0,3]
        		sum_x = pt1[0] + pt2[0] + pt3[0] + pt4[0]
        		sum_y = pt1[1] + pt2[1] + pt3[1] + pt4[1]
        		center = (sum_x/length, sum_y/length)            
	return center, lost
        
if __name__ == '__main__':
	id_Track = 3
	camera = PiCamera()
	b_pin = 26
	u_pin = 19
	bDC = 1500
	uDC = 2050
	while True:
    		center, lost = FromFeed(id_Track, camera, b_pin, u_pin, bDC, uDC)


