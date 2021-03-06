#!/usr/bin/env python

import RPi.GPIO as GPIO
import cario
import time
from enum import Enum
from direction import *
import threading

import inspect

IOPIN_SWITCH_F = 18 #11
IOPIN_SWITCH_B = 22 #13
IOPIN_SWITCH_L = 15
IOPIN_SWITCH_R = 16

class Movement:
	def __init__(self):
		self.dir = -1
		GPIO.setmode(GPIO.BOARD)
		self.IOPIN_F = cario.CARIO(IOPIN_SWITCH_F)
		self.IOPIN_B = cario.CARIO(IOPIN_SWITCH_B)
		self.IOPIN_L = cario.CARIO(IOPIN_SWITCH_L)
		self.IOPIN_R = cario.CARIO(IOPIN_SWITCH_R)
		self.dirY = DirY.H
		self.dirX = DirX.H

	def stopY(self):
		if self.dirY != DirY.H:
			#print("released y")
			self.IOPIN_F.OFF()
			self.IOPIN_B.OFF()
			self.dirY = DirY.H

			curframe = inspect.currentframe()
			calframe = inspect.getouterframes(curframe, 2)
			print 'caller name:', calframe[1][3]

	def stopX(self):
		if self.dirX != DirX.H:
			#print("released x")
			self.IOPIN_L.OFF()
			self.IOPIN_R.OFF()
			self.dirX = DirX.H

	def halt(self):
		self.stopY()
		self.stopX()

	def moveForward(self):
		if self.dirY != DirY.F:
			print("forward")
			self.IOPIN_B.OFF()
			self.IOPIN_F.ON()
			self.dirY = DirY.F

	def moveBackward(self):
		if self.dirY != DirY.B:
			print("backward")
			self.IOPIN_F.OFF()
			self.IOPIN_B.ON()
			self.dirY = DirY.B

	def turnLeft(self):
		if self.dirX != DirX.L:
			print("left")
			self.IOPIN_R.OFF()
			self.IOPIN_L.ON()
			self.dirX = DirX.L

	def turnRight(self):
		if self.dirX != DirX.R:
			print("right")
			self.IOPIN_L.OFF()
			self.IOPIN_R.ON()
			self.dirX = DirX.R

	def moveForwardLeft(self):
		self.moveForward()
		self.turnLeft()

	def moveBackwardLeft(self):
		self.moveBackward()
		self.turnLeft()

	def moveForwardRight(self):
		self.moveForward()
		self.turnRight()

	def moveBackwardRight(self):
		self.moveBackward()
		self.turnRight()

	def moveForwardFor(self, delay):
		self.moveForward()
		time.sleep(delay)
		self.halt()

	def moveBackwardFor(self, delay):
		self.moveBackward()
		time.sleep(delay)
		self.halt()

	def moveForwardLeftFor(self, delay):
		self.moveForwardLeft()
		time.sleep(delay)
		self.halt()

	def moveForwardRightFor(self, delay):
		self.moveForwardRight()
		time.sleep(delay)
		self.halt()

	def moveBackwardLeftFor(self, delay):
		self.moveBackwardLeft()
		time.sleep(delay)
		self.halt()

	def moveBackwardRightFor(self, delay):
		self.moveBackwardRight()
		time.sleep(delay)
		self.halt()

	def moveLeftFor(self, delay):
		if self.dirX == DirX.H and self.dirY == DirY.H:
			def delayBgL():
				self.moveBackwardRightFor(delay*0.5)
				self.moveForwardLeftFor(delay*0.5)
			mv = threading.Thread(target=delayBgL)
			mv.start()

	def moveRightFor(self, delay):
		if self.dirX == DirX.H and self.dirY == DirY.H:
			def delayBgR():
				self.moveBackwardLeftFor(delay*0.5)
				self.moveForwardRightFor(delay*0.5)
			mv = threading.Thread(target=delayBgR)
			mv.start()

	def turnLeftFor(self, delay):
		self.turnLeft()
		time.sleep(delay)
		self.halt()

	def turnRightFor(self, delay):
		self.turnRight()
		time.sleep(delay)
		self.halt()
