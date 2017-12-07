#!/bin/bash
# Authors: Diego Horna (dh468), Deepthi Krovvidi (dk562)
# Final Project GUI
# November 14th

# Packages needed to run the code
import pygame # Import Library and initialize
from pygame.locals import *
from math import sqrt
import time
import random
import RPi.GPIO as GPIO
import subprocess
import os

# Setting up fail safe pin on piTFT screen
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def GPIO17_callback(channel):
	GPIO.cleanup()
        exit()
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)

# Commands to run program on piTFT
os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

# Pygame init
pygame.init()
pygame.mouse.set_visible(True)  #cursor not shown if False, otherwise set to True

#Initializing the main text
WHITE = 255, 255, 255
black = 0, 0, 0
size = width, height = 320, 240       # Screen size
screen = pygame.display.set_mode((size))

# Initializing the first image
luxor_jr = pygame.image.load("luxor_jr.png")
luxor_rect = luxor_jr.get_rect()
luxor_rect.x = -60
luxor_rect.y = 0

screen.blit(luxor_jr,luxor_rect)

my_font = pygame.font.Font(None, 20)
screen_one = { 'Welcome to Luxor III':(220,20),'Inspired by Pixars own':(220,40),'Next':(280,220)}

for my_text, text_pos in screen_one.items():
   text_surface = my_font.render(my_text, True, WHITE)
   rect = text_surface.get_rect(center=text_pos)
   screen.blit(text_surface, rect)

pygame.display.flip()

# First loop
run = 0
while run == 0: 
  
  # Checking if user has pressed anything on the main screen
#  print('check 1')
  for event in pygame.event.get():
    if(event.type is MOUSEBUTTONDOWN):
      pos = pygame.mouse.get_pos()

    elif(event.type is MOUSEBUTTONUP):
      pos = pygame.mouse.get_pos()
      x,y = pos
      if y > 200 and x > 280:
#          print('If they pressed Next on the screen to move to the turning components on')
          run = 1
          while run == 1:
            screen.fill(black)
#            print('turn red switch on')  
            switch_on = {'Next':(280,220),'Turn the red switch on!':(160,120)}
            for my_text, text_pos in switch_on.items():
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
                if y > 200  and  x > 280:
                    run_two = 2
                    # If they pressed Next ask to put tags on obects to track
		    while run_two == 2: 
                      screen.fill(black)
#		      print('put tags on shit')	
		      tags_on = {'Put tags on objects to track':(160,120),'Next':(280,220)}
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
                          if y > 200 and x > 280:
                              
			    run_three = 3
                            # If they pressed next ask to input how many tags
			    while run_three == 3:
                                screen.fill(black)
                                number_tags = {'Number of tags':(160,40),'1':(80,80),'2':(160,80),'3':(240,80),'4':(80,140),'5':(160,140),'6':(240,140),'7':(80,200),'8':(160,200),'9':(240,200)}
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
                                      if y < 80 and x > 50 and x < 110:
                                      # they pressed one
                                          s = 1	

                                      if y < 80 and x > 130 and x < 190:
                                      # they pressed two
                                          s = 2
                                      if y < 80 and x > 210 and x < 270:
                                      # they pressed three
                                          s = 3
                                      if y > 120 and y < 190 and x > 50 and x < 100:
                                      # they pressed four
                                          s = 4
                                      if y > 120 and y < 190 and x > 130 and x < 190:
                                      # they pressed five
                                          s = 5
                                      if y > 120 and y < 190 and x > 210 and x < 270:
                                          # they pressed six
                                          s = 6
                                      if y > 210 and x > 50 and x < 100:
                                          # they pressed seven
                                          s = 7
                                      if y > 210 and x > 130 and x < 190:
                                          # they pressed eight
                                          s =8
                                      if y > 210 and x > 210 and x < 270:
                                          # they pressed nine
                                          s = 9
