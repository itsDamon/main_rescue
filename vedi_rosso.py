import time

import cv2
import imutils
import numpy as np
from picamera2 import Picamera2

light_red = np.array([0,50,50])
dark_red = np.array([10,255,255])
MAXX=256
MAXY=144
cv2.startWindowThread()   #permette l'aggiornamento di cv2.imshow()
camera = Picamera2()      #assegna la videocamera e assegna il video a camera
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (MAXX, MAXY)})) #configura la videocamera
camera.start()            #avvia la videocamera
time.sleep(2)             #pausa 2s





def Rosso(originale,ymin,ymax):

    mask = cv2.inRange(hsv, light_red, dark_red)
    mask=mask[ymax:ymin,50:200]
    cv2.imshow("rosso",mask)
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
    trovato= Rosso(im,MAXY,100)
    print(trovato)
picam2.close()