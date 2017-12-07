#!/usr/env python
# this is used to draw the numbers on the screen

def numberbuttons(x,y):
	if y < 100 and x > 50 and x < 110:
        # they pressed one
	        tag_id = 1
        if y < 100 and x > 130 and x < 190:
        # they pressed two
	        tag_id = 2

        if y < 100 and x > 210:
        # they pressed three
        	tag_id = 3

	if y > 120 and y < 180 and x < 100:
        # they pressed four
        	tag_id = 4

        if y > 120 and y < 180 and x > 130 and x < 190:
        # they pressed five
        	tag_id = 5

        if y > 120 and y < 180 and x > 210 and x < 270:
	# they pressed six
        	tag_id = 6

        if y > 200 and x > 50 and x < 100:
  	# they pressed seven
        	tag_id = 7

   	if y > 200 and x > 130 and x < 190:
        # they pressed eight
        	tag_id = 8

      	if y > 200 and x > 210 and x < 270:
        # they pressed nine
        	tag_id = 9

	return tag_id
if __name__ == '__main__':

	tag_id = numberbuttons(x,y)
	
