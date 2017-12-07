#!/usr/env python
import pygame
from pygame.locals import *

def colors(screen,red,green,ids):
        pygame.draw.rect(screen,red,(70,70,20,20),0)
        pygame.draw.rect(screen,red,(150,70,20,20),0)
        pygame.draw.rect(screen,red,(230,70,20,20),0)
        pygame.draw.rect(screen,red,(70,130,20,20),0)
        pygame.draw.rect(screen,red,(150,130,20,20),0)
        pygame.draw.rect(screen,red,(230,130,20,20),0)
	pygame.draw.rect(screen,red,(70,190,20,20),0)
        pygame.draw.rect(screen,red,(150,190,20,20),0)
        pygame.draw.rect(screen,red,(230,190,20,20),0)
	
	for tag_green in ids:
            if tag_green == 1:
                pygame.draw.rect(screen,green,(70,70,20,20),0)
            if tag_green == 2:
                pygame.draw.rect(screen,green,(150,70,20,20),0)
            if tag_green == 3:
                pygame.draw.rect(screen,green,(230,70,20,20),0)
            if tag_green == 4:
                pygame.draw.rect(screen,green,(70,130,20,20),0)                
            if tag_green == 5:
                pygame.draw.rect(screen,green,(150,130,20,20),0)                
            if tag_green == 6:
                pygame.draw.rect(screen,green,(230,130,20,20),0)
            if tag_green == 7:
                pygame.draw.rect(screen,green,(70,190,20,20),0)    
            if tag_green == 8:
                pygame.draw.rect(screen,green,(150,190,20,20),0)
            if tag_green == 9:
                pygame.draw.rect(screen,green,(230,190,20,20),0)
	
if __name__ == '__main__':
	ids =[1, 2, 4, 6, 8]
	colors(screen,red,green,ids)
