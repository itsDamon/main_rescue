import numpy as np
from picamera2 import Picamera2, Preview
import imutils
import time
import cv2

cv2.startWindowThread()
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (256, 144)}))
picam2.start()
time.sleep(2)


while True:
    img = picam2.capture_array()
    crop = img[100:120, 100:200]
    crop=cv2.rectangle(crop,(0,0),(50,50),(0,255,0),5)
    cv2.imshow("limo",crop)
    img=cv2.rectangle(img,(0,0),(50,50),(0,255,0),5)
    cv2.imshow("vera",img)
    color=0
    print(color)
    if color == 255 :
        print ("trovato")
    print ("assente")

picam2.close()