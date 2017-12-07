#!/usr/env python
# Authors: Diego Horna

# Import Library and Initialize 
import time

def dc(base_servo, camera_servo, ocx, ocy, bDC, uDC):
	addDC_x = 0
	addDC_y = 0
	 # Calculating change in x
        if ocx < 290 or ocx > 350:
                add_phi_x = ((ocx-320)*30)/320
                addDC_x = (add_phi_x*333)/(30)
                bDC = bDC - addDC_x
	# Calculating change in y
        if ocy < 210 or ocy > 270:
                add_phi_y = ((240-ocy)*30)/240
                addDC_y = (add_phi_y*333)/(30)
                uDC = uDC + addDC_y
        
	if bDC > 2500:
		bDC = 2500
	if bDC < 500:
		bDC = 500
	if uDC > 2500:
		uDC = 2500
	if uDC < 500:
		uDC = 500
	return bDC, uDC

if __name__ == '__main__':
	base_servo = 26
	camera_servo = 19
	dc_length, dc_width = dc(base_servo, camera_servo, bDC, uDC)	
