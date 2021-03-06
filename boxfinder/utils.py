#!/usr/bin/env python

import sys
import cv2
import numpy as np
import base64
import threading

meterdiff = 95

lower_1 = np.array([170,100,120])
upper_1 = np.array([180,235,255])
lower_2 = np.array([0,100,120])
upper_2 = np.array([5,235,255])

camera = 0
fov = 60

delay = 0.05
cport = 42069
iport = 6969
dport = 6666

def getch():
	import termios, tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def _getchthread():
	while True:
		if getch() == 'q':
			print("\nHALT")
			sys.exit()

def getchthread():
	getch = threading.Thread(target=_getchthread)
	getch.daemon = True
	getch.start()

def rprint(str):
	sys.stdout.write('%s\r' % str)
	sys.stdout.flush()

def mattostr(mat):
	return cv2.imencode('.jpg', mat)[1] #remove [1] if doesn't work

def strtomat(str):
	arr = np.fromstring(str, np.uint8)
	return cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)

def mattobase64(mat):
	retval, buffer = cv2.imencode('.jpg', mat)
	str = base64.b64encode(buffer)+'.'
	return str

def int_to_bytes(val, num_bytes):
    return [(val & (0xff << pos*8)) >> pos*8 for pos in range(num_bytes)]
