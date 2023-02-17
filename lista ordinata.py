import numpy as np
from picamera2 import Picamera2, Preview
import imutils
import time
import cv2

cv2.startWindowThread()
'''
picam2 = Picamera2()
picam2.configure(picam2.preview_configuration(main={"format": 'XRGB8888', "size": (256, 144)}))
picam2.start()
time.sleep(2)
'''
light_green = np.array([30,00,50])
dark_green = np.array([85,255,255])
    
im = cv2.imread('/home/pi/foto2.jpg')
cv2.imshow("gigi",im)
    #cv2.imshow("Camera", im)
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, light_green, dark_green)
cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cv2.imshow("verde",mask)
if len(cnts) != 0:
    c = max(cnts, key = cv2.contourArea)
    cnts.sort(reverse=True, key= cv2.contourArea)
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        print(c)
        print(w*h)
    print("next \n")
#print(verde)
#picam2.close()
