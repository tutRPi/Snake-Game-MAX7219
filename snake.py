#!/usr/bin/env python
# ---------------------------------------------------------
# Filename: snake.py
# ---------------------------------------------------------
# snake Game for using with MAX7219 Matrices
#
# v1.0
# F.Stern 2014
# ---------------------------------------------------------
# You need to copy the files of this repository to this folder
# https://github.com/tutRPi/multilineMAX7219
# multilineMAX7219.py and multilineMAX7219_fonts.py
#
# The RPi.GPIO library has to be installed, if joypad is used
# https://pypi.python.org/pypi/RPi.GPIO
# ---------------------------------------------------------
#
# run as root with:
# sudo python snake.py
#
# If you use a joypad, set USE_JOYPAD = True and make sure the
# GPIO Pins are correct
# You also have to adjust your Matrix width and height in multilineMAX7219.py
# ---------------------------------------------------------


from Point import Point
import RPi.GPIO as GPIO
import multilineMAX7219 as LEDMatrix # from https://github.com/tutRPi/multilineMAX7219
from multilineMAX7219 import GFX_ON, GFX_OFF, GFX_INVERT
from random import randrange
import threading, sys
import time


USE_JOYPAD = False 	# if you set this to True, you have to connect 4 Buttons
					# else you can control it with your arrow keys (USE_JOYPAD=False)

# only necessary if USE_JOYPAD = True
# RPi.GPIO Layout (GPIO numbers)
GPIO_UP 	= 4
GPIO_DOWN 	= 17
GPIO_RIGHT 	= 21
GPIO_LEFT	= 22

# Directions
DIR_U = Point(0,1)
DIR_D = Point(0,-1)
DIR_R = Point(1,0)
DIR_L = Point(-1,0)

# Make sure you set these correct in multilineMAX7219.py
WIDTH = 8*LEDMatrix.MATRIX_WIDTH-1
HEIGHT = 8*LEDMatrix.MATRIX_HEIGHT-1

tail = [Point(WIDTH//2, HEIGHT//2)]
start = randrange(2)
direction = Point(start, 1 - start)	# init direction

target = Point()
running = True			# loop variable
speed = 0.3				# getting faster, the longer the snake is
wasDisplayed = True		# to allow only one new direction per frame

LEDMatrix.init()


def display():
	# displays all on the LED Matrices
	LEDMatrix.gfx_set_all(GFX_OFF)
	for p in tail:
		LEDMatrix.gfx_set_px(int(p.x), int(p.y), GFX_ON)
	LEDMatrix.gfx_set_px(int(target.x), int(target.y), GFX_ON)
	LEDMatrix.gfx_render()
	global wasDisplayed
	wasDisplayed = True

def setTarget():
	# sets a new target, which is not in the tail of the snake
	global target
	target = Point(randrange(WIDTH+1), randrange(HEIGHT+1))
	while target in tail:
		target = Point(randrange(WIDTH+1), randrange(HEIGHT+1))

def move():
	global running, speed
	if running:
		newPosition = tail[0] + direction
		if newPosition.x > WIDTH:
			newPosition.x -= WIDTH+1
		elif newPosition.x < 0:
			newPosition.x += WIDTH+1
		if newPosition.y > HEIGHT:
			newPosition.y -= HEIGHT+1
		elif newPosition.y < 0:
			newPosition.y += HEIGHT+1
		
		if newPosition == target:
			tail.insert(0,newPosition)
			setTarget()
			speed = max(0.07, min(0.3, 2/float(len(tail))))
		elif newPosition not in tail:
			tail.insert(0, newPosition)
			tail.pop()
		else:
			# Game Over
			running = False
			for i in range(6):
				LEDMatrix.gfx_set_all(GFX_INVERT)
				LEDMatrix.gfx_render()
				time.sleep(0.3)
			if USE_JOYPAD:
				print "Game Over. Score: " + str(len(tail)-1)
			else:
				print "Game Over. Press any Key to exit. Score: " + str(len(tail)-1)
			LEDMatrix.clear_all()
			raise SystemExit("\n")
		
		# threading for calling it every period
		threading.Timer(speed, move).start ()
	else:
		LEDMatrix.clear_all()
	display()

	
def changeDirection(newDirection = direction):
	global direction, wasDisplayed
	if wasDisplayed:
		if newDirection != direction and (newDirection.x != -direction.x or newDirection.y != -direction.y):
			direction = newDirection
			wasDisplayed = False
	
	

if __name__ == "__main__":
	
	setTarget()
	move()
	
	if USE_JOYPAD:
		# do not press several buttons once
		try:
			print "To end the game press <CTRL> + C"
			# RPi.GPIO Layout (GPIO numbers)
			GPIO.setmode(GPIO.BCM)
			GPIO.setwarnings(False)
			# set GPIOs to Input
			GPIO.setup(GPIO_UP, GPIO.IN)
			GPIO.setup(GPIO_DOWN, GPIO.IN)
			GPIO.setup(GPIO_RIGHT, GPIO.IN)
			GPIO.setup(GPIO_LEFT, GPIO.IN)
			while running:
				if GPIO.input(GPIO_UP) == GPIO.HIGH:
					changeDirection(DIR_U)
				elif GPIO.input(GPIO_DOWN) == GPIO.HIGH:
					changeDirection(DIR_D)
				elif GPIO.input(GPIO_RIGHT) == GPIO.HIGH:
					changeDirection(DIR_R)
				elif GPIO.input(GPIO_LEFT) == GPIO.HIGH:
					changeDirection(DIR_L)
				time.sleep(0.1)
		except KeyboardInterrupt:
			# CTRL + C
			print "\nGoodbye"
			LEDMatrix.clear_all()
			time.sleep(0.1)
			running = False
			GPIO.cleanup(GPIO_UP)
			GPIO.cleanup(GPIO_DOWN)
			GPIO.cleanup(GPIO_RIGHT)
			GPIO.cleanup(GPIO_LEFT)
	else:
		# Use Keyboard Arrows
		from _Getch import _Getch
		getch = _Getch()
		print "To end the game press <q>"
		while running:
			key = ord(getch())
			if key == 27: #ESC
				key = ord(getch())
				if key == 91:
					key = ord(getch())
					if key == 65: #Up arrow
						changeDirection(DIR_U)
					if key == 66: #Down arrow
						changeDirection(DIR_D)
					elif key == 67: #right arrow
						changeDirection(DIR_R)
					elif key == 68: #left arrow
						changeDirection(DIR_L)
			elif key == 113:
				print "Goodbye"
				running = False
				break
