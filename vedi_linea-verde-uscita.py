from picamera.array import PiRGBArray
from picamera2 import Picamera2, Preview
import cv2
import numpy as np
import imutils
import serial
import time

light_green = np.array([36,50,50])
dark_green = np.array([85,255,255])
MAXX=256
MAXY=144
cv2.startWindowThread()   #permette l'aggiornamento di cv2.imshow()
camera = Picamera2()      #assegna la videocamera e assegna il video a camera
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (MAXX, MAXY)})) #configura la videocamera
camera.start()            #avvia la videocamera
time.sleep(2)             #pausa 2s





def vediLinreaVerde(originale,ymin,ymax):

    mask = cv2.inRange(hsv, light_green, dark_green)
    mask=mask[ymin:ymax,50:200]
    cv2.imshow("verde",mask)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    if len(cnts) != 0:
        c = max(cnts, key = cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        cx = (x+(w//2))
        print(w*h)
        if(w*h>1000):
            return "trovato"
        
while True:
    im = camera.capture_array()
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    #im = cv2.flip(im, 0)
    cv2.imshow("Camera", im)
    trovato= vediLinreaVerde(im,100,MAXY)
    print(trovato)
picam2.close()