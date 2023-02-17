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
light_green = np.array([36,50,50])
dark_green = np.array([85,255,255])

def Find_Verde(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, light_green, dark_green)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cv2.imshow("verde",mask)
    if len(cnts) != 0:
        c = max(cnts, key = cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        cx = (x+(w//2))     #trova il punto medio
        area=w*h
        print(area)
        if area>500:#contralla se l'area è valida
            if y>10:#controlla se ha la riga nera sopra
                nero = nero_presente(img,y-7,cx)
                if nero == "trovato":
                    if len(cnts) > 1: #controlla se ci son 2 quadrati validi per retromarcia
                        for c2 in cnts:
                            x2, y2, w2, h2 = cv2.boundingRect(c2)
                            a2=w2*h2
                            print(a2)
                            if y2>10 and a2 < area:
                                nero = nero_presente(img,y2-7,x2+(w2//2))
                                if nero == "trovato":
                                    return "indietro"
                    if x>10: #controlla che si deve girare a destra
                        nero= nero_presente(img,y+(h//2),x-7)
                        if nero == "trovato":
                            return "destra"
                    if x+w<246:#controlla se si deve girare a sinistra
                        nero= nero_presente(img,y+(h//2),x+w+2)
                        if nero == "trovato":
                            return "sinistra"
                    if x<10:# in caso che sia attaca al bordo di sinistra curva a destra
                        return "destra"
                    if x+w>246: # in caso che sia attaca al bordo di destra curva a sinistra
                        return "sinistra"
    return "non trovato"

def nero_presente(img ,y,cx ):#dice se c'è presente del nero
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (T, nero) = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY_INV)
    crop = nero[y:y+5, cx:cx+5]
    color=crop[4,4]
    print(color)
    if color == 255 :
        return "trovato"
    return "assente"


while True:
    im = picam2.capture_array()
    
    cv2.imshow("Camera", im)
    verde=Find_Verde(im)
    print(verde)
picam2.close()



