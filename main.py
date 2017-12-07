#!/bin/bash
# Authors: Diego Horna (dh468), Deepthi Krovvidi (dk562)
# Final Project Main code (main.py)
# December 2nd

# Import and initialize libraries
import pygame 
from pygame.locals import *
from math import sqrt
import time
import random
import RPi.GPIO as GPIO
import subprocess
import os
import from_feed_sweep
import from_feed_track
import quit_button
import number_buttons
import arm_dynamic
from picamera import PiCamera
import pigpio
import sys
import number_collors 

# Setting up fail safe pin on piTFT screen (top right corner)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def GPIO17_callback(channel):
    GPIO.cleanup()
    exit()
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)

# Commands to run program on piTFT (COMMENT OUT TO RUN ON MONITOR)
#os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
#os.putenv('SDL_FBDEV', '/dev/fb1')
#os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT
#os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

# Pygame init
pygame.init()
#pygame.mouse.set_visible(False)  # MOUSE not shown if FALSE, otherwise set to TRUE
pygame.mouse.set_visible(True)  # MOUSE not shown if FALSE, otherwise set to TRUE


# colors for screen (what if it's below 255? Does intensity change?)
WHITE = 255, 255, 255
black = 0, 0, 0
blue = 0, 0 , 255
green = 0, 255, 0
red = 255, 0, 0

# Screen size for piTFT (or monitor too)
size = width, height = 320, 240       
screen = pygame.display.set_mode((size))

# Initializing luxor jr main photo
#luxor_jr = pygame.image.load("home/pi/embeddedfinalproject/luxor_jr.png")
luxor_jr = pygame.image.load("luxor_jr.png")
luxor_rect = luxor_jr.get_rect()
luxor_rect.x = -60
luxor_rect.y = 0

# Showing the image above before text so text goes on top of it. 
screen.blit(luxor_jr,luxor_rect)

# Main screen text initializing
my_font = pygame.font.Font(None, 20)
screen_one = { 'Welcome to Luxor III':(220,20),'Inspired by Pixars own':(220,40),'Next':(280,220),'Quit':(40,220)}

for my_text, text_pos in screen_one.items():
   text_surface = my_font.render(my_text, True, WHITE)
   rect = text_surface.get_rect(center=text_pos)
   screen.blit(text_surface, rect)

# displaying main screen text
pygame.display.flip()

run = 0     # index for main page

# First loop which includes luxor pic and welcoming
while run == 0: 
  # Checking if user has pressed anything on the main screen
  for event in pygame.event.get():
    if(event.type is MOUSEBUTTONDOWN):
      pos = pygame.mouse.get_pos()

    elif(event.type is MOUSEBUTTONUP):
      pos = pygame.mouse.get_pos()
      x,y = pos
      
      # if they clicked on quit
      quit_button.QuitButton(x,y) 
      
      # if they clicked on next
      if y > 200 and x > 220:
        run = 1     # index for second page cannot go back to main page

        # time to turn on the servos
        while run == 1:
          screen.fill(blue)     # reset the screen to new color

          # Text for second page
          switch_on = {'Next':(280,220),'Turn the red switch on!':(160,120),'Quit':(40,220)}

          for my_text, text_pos in switch_on.items():
              text_surface = my_font.render(my_text, True, WHITE)
              rect = text_surface.get_rect(center=text_pos)
              screen.blit(text_surface, rect)

          # displaying second page text
          pygame.display.flip()

          for event in pygame.event.get():
            if(event.type is MOUSEBUTTONDOWN):
              pos = pygame.mouse.get_pos()
            elif(event.type is MOUSEBUTTONUP):
              pos = pygame.mouse.get_pos()
              x,y = pos
	      quit_button.QuitButton(x,y)

              if y > 200  and  x > 220:
                run = 2

                # Time to put tags on objects
                while run == 2: 
                  screen.fill(blue)
                  
                  tags_on = {'Put tags on objects to track':(160,120),'Next':(280,220),'Quit':(40,220)}
                  
                  for my_text, text_pos in tags_on.items():
                        text_surface = my_font.render(my_text, True, WHITE)
                        rect = text_surface.get_rect(center=text_pos)
                        screen.blit(text_surface, rect)
                  pygame.display.flip()
                  
                  for event in pygame.event.get():
                      if(event.type is MOUSEBUTTONDOWN):
                        pos = pygame.mouse.get_pos()
                      elif(event.type is MOUSEBUTTONUP):
                        pos = pygame.mouse.get_pos()
                        x,y = pos
			quit_button.QuitButton(x,y)

                        if y > 200 and x > 220:
                          run = 3
                          tag_id = 0      # this tag id is used for an iff statement in the next while loop
                          # If they pressed next ask to input number of tags
			  while run == 3:
                            screen.fill(blue)

                            number_tags = {'Number of tags':(160,40),'1':(80,80),'2':(160,80),'3':(240,80),'4':(80,140),'5':(160,140),'6':(240,140),'7':(80,200),'8':(160,200),'9':(240,200),'Quit':(40,220)}                          
                            for my_text, text_pos in number_tags.items():
                                text_surface = my_font.render(my_text, True, WHITE)
                                rect = text_surface.get_rect(center=text_pos)
                                screen.blit(text_surface, rect)
                            pygame.display.flip()

                            for event in pygame.event.get():
                              if(event.type is MOUSEBUTTONDOWN):
                                pos = pygame.mouse.get_pos()      	   
                              elif(event.type is MOUSEBUTTONUP):       
                                pos = pygame.mouse.get_pos()
                                x,y = pos
				quit_button.QuitButton(x,y)

				tag_id = number_buttons.numberbuttons(x,y)
                                
                                # number of tags found 
                                found = 0
	                        # if the tag_id (number of ID's selected) is greater than 0 and the number of found tags is not the same 
				#sweeping while loop
				while (tag_id != 0) and (found != tag_id):
					screen.fill(blue)
					id_List, found, camera, bDC_List, uDC_List, emptyframe = from_feed_sweep.FromFeed(tag_id, 26, 19, 0, 0)
					quit_button.QuitButton(x,y)
				if not emptyframe:
					# Prompt new number of tags input
					my_font = pygame.font.Font(None, 20)
					screen_oops = { 'Could Not Find Tags':(160, 120)}

					for my_text, text_pos in screen_oops.items():
   						text_surface = my_font.render(my_text, True, WHITE)
   						rect = text_surface.get_rect(center=text_pos)
   						screen.blit(text_surface, rect)

					# displaying main screen text
					pygame.display.flip()
					time.sleep(5)
					break
				status_tags = {'Select marker to track':(160,40),'1':(80,80),'2':(160,80),'3':(240,80),'4':(80,140),'5':(160,140),'6':(240,140),'7':(80,200),'8':(160,200),'9':(240,200), 'Quit':(40, 220)}
				number_collors.colors(screen,red,green,id_List)
				
				for my_text, text_pos in status_tags.items():
                                	text_surface = my_font.render(my_text, True, WHITE)
                                	rect = text_surface.get_rect(center=text_pos)
                                	screen.blit(text_surface, rect)
				
				pygame.display.flip()
                                track_id = 0
				x = 0
				count = 0
				b_pin = 26
				u_pin = 19
				while (found == tag_id):
					time.sleep(0.8)
                                        for event in pygame.event.get():
  	                                      if(event.type is MOUSEBUTTONDOWN):
        	                                      pos = pygame.mouse.get_pos()
                                              elif(event.type is MOUSEBUTTONUP):
							pos = pygame.mouse.get_pos()
							x,y = pos
							track_id = 0
							count = 0
							while track_id < 1 and x >0:
						        	quit_button.QuitButton(x,y)
								if y < 80 and x > 50 and x < 110:
                                					# they pressed one
                                  					if 1 in id_List:
										track_id = 1				    
	
	        	                        		if y < 80 and x > 130 and x < 190:
		                                			# they pressed two
               			                  			if 2 in id_List:
										track_id = 2
	
        	                        			if y < 100 and x > 210:
                	                				# they pressed three
                       			           			if 3 in id_List:
										track_id = 3
						
	                                			if y > 120 and y < 190 and x > 50 and x < 100:
        	                        				# they pressed four
                	                  				if 4 in id_List:
										track_id = 4

	                              	  			if y > 120 and y < 190 and x > 130 and x < 190:
        	                        				# they pressed five
                	                  				if 5 in id_List:
										track_id = 5

	                                			if y > 120 and y < 190 and x > 210 and x < 270:
        	                        				# they pressed six
                	                  				if 6 in id_List:
										track_id = 6

	                                			if y > 210 and x > 50 and x < 100:
        	                        				# they pressed seven
                	                  				if 7 in id_List:
										track_id = 7

	                                			if y > 210 and x > 130 and x < 190:
        	                        				# they pressed eight
                	                  				if 8 in id_List:
										track_id = 8

	                                			if y > 210 and x > 210 and x < 270:
        	                        				# they pressed nine
                	                  				if 9 in id_List:
										track_id = 9
								else:
									break

					if track_id > 0:
						for i in range(0, len(id_List)):
							if track_id == id_List[i]:
								bDC = bDC_List[i]
								uDC = uDC_List[i]
								index = i
						# Set the value for the position of the servo at the last known location
						pi = pigpio.pi()
						pi.set_servo_pulsewidth(b_pin, bDC)
						pi.set_servo_pulsewidth(u_pin, uDC)
						time.sleep(0.1)
						center, lost = from_feed_track.FromFeed(track_id, camera, 26, 19, bDC, uDC)
						if not lost:
							dc_base, dc_cam = arm_dynamic.dc(26, 19, center[0], center[1], bDC, uDC)
							bDC_List[index] = dc_base
							uDC_List[index] = dc_cam
							count = 0
						else:
							lost = 0
							count = count + 1
							if count == 3:
								count = 0							
								id_List, found, camera, bDC_List, uDC_List, emptyframe = from_feed_sweep.FromFeed(tag_id, 26, 19, lost, track_id)
