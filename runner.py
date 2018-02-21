#!/usr/bin/env python

import cv2
import camera
import worker
import time
import coordinates
import network
import sys
import threading
import utils
import time
import tcp

rip = '10.56.35.2'
if len(sys.argv) != 2:
	print("=====ATTENTION=====")
	print("Usage: " + sys.argv[0] + " DRIVERIP")
	print("No IP addresses specified! Defaulting to 10.56.35.69")
	print("=====ATTENTION=====")
	dip = '10.56.35.69'
else:
	dip = sys.argv[1]

print("Launched!")

camera = camera.Camera()

cconn       = network.Network(rip, utils.cport)
iconn       = network.Network(dip, utils.iport)
#dconn       = network.Network(rip, utils.dport)

coordinates = coordinates.Coordinates()

def run():
	mat = camera.tomat()
	picture,coordinates = worker.process(mat)
	lineThickness = 2
	cv2.line(picture, (coordinates.cX, 0), (coordinates.cX, 240), (0,255,0), lineThickness)
	cconn.send(str(coordinates.angle))
	coordinates.latest = time.time()
	matstr = utils.mattostr(picture)
	iconn.send(matstr)

while True:
	cconn = network.Network(rip, utils.cport)
	iconn = network.Network(dip, utils.iport)
	cconn.connect()
	iconn.connect()
	while iconn.alive and cconn.alive:
		if camera.latest != -1 and camera.latest > coordinates.latest:
			run()
