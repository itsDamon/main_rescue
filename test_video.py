from picamera.array import PiRGBArray
from picamera2 import Picamera2, Preview
import cv2
import numpy as np
import imutils
import serial
import time

MAXX=256
MAXY=144
cv2.startWindowThread()   #permette l'aggiornamento di cv2.imshow()
camera = Picamera2()      #assegna la videocamera e assegna il video a camera
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (MAXX, MAXY)})) #configura la videocamera
camera.start()            #avvia la videocamera
time.sleep(2)      

while True:
    im = camera.capture_array()
    im = cv2.flip(im,0)
    cv2.imshow("Camera", im)
    im = cv2.flip(im,2)
    cv2.imshow("Camera2", im)    

picam2.close()
