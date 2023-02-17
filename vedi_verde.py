import numpy as np
from picamera2 import Picamera2, Preview
import imutils
import time
import cv2

cv2.startWindowThread()
picam2 = Picamera2()
picam2.configure(picam2.preview_configuration(main={"format": 'XRGB8888', "size": (1920, 1080)}))
picam2.start()
time.sleep(2)
light_green = np.array([36,50,50])
dark_green = np.array([85,255,255])

def Find_Verde(mask):
    cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    mask = cv2.inRange(hsv, light_green, dark_green)
    cv2.imshow("input",mask)
    if len(cnts) != 0:
        c = max(cnts, key = cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        cx = (x+(w//2))     #trova il punto medio
        area=w*h
        print(area)
    
        #if area>10400:
        
        #return "non trovato"

def filtro(img):        #converte l'immagine in bianco e nero invertito,(nero reale=bianco e viceversa)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#converte l'immagine da bgr a grayscale
    (T, threshed) = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY_INV)#converte in bianco e nero l'immagine
    cv2.imshow("Tresh", threshed)#la mostra a video
    return threshed



while True:
    im = picam2.capture_array()
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    cv2.imshow("Camera", im)

picam2.close()


