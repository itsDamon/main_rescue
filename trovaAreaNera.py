import time

import cv2
import imutils
from picamera2 import Picamera2

MAXX=256
MAXY=144
cv2.startWindowThread()   #permette l'aggiornamento di cv2.imshow()
camera = Picamera2()      #assegna la videocamera e assegna il video a camera
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (MAXX, MAXY)})) #configura la videocamera
camera.start()            #avvia la videocamera
time.sleep(2) 


def findAreaNera(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (T, nero) = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow("Threshold", nero)
    cnts = cv2.findContours(nero.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    if len(cnts) != 0:
        c = max(cnts, key = cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        cx = (x+(w//2))     #trova il punto medio
        area=w*h
        print(area)
        
        cy = (y+(h//2))
    
        if area>2000:
            return True
    return False


while True:
    # reads frames from a camera 
    im = camera.capture_array()
    if(findAreaNera(im)):
        print("NERO")
    else:
        print("NON è NERO")
    #cv2.imshow("",im)
    #cv2.waitKey(1)