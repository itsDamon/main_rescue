import numpy as np
from picamera2 import Picamera2, Preview
import imutils
import time
import cv2

cv2.startWindowThread()
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()
time.sleep(2)

def findBordi(mask):
    cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    if len(cnts) != 0:
        c = max(cnts, key = cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        cx = (x+(w//2))     #trova il punto medio
        area=w*h
        print(area)
    
        if area>10400 :
            return "stop"
    
    return "non trovato"

while True:
    im = picam2.capture_array()
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    cv2.imshow("Camera", im)
    light_red = np.array([0,100,100])
    dark_red = np.array([10,255,255])
    mask = cv2.inRange(hsv, light_red, dark_red)
    cv2.imshow("input",mask)
    stop=findBordi(mask)
    print(stop)
picam2.close()


