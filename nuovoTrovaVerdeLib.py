import cv2
import imutils
import numpy as np

cv2.startWindowThread()
light_green = np.array([36, 50, 50])
dark_green = np.array([85, 255, 255])


def isverde(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, light_green, dark_green)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cv2.imshow("isverde", mask)
    if len(cnts) != 0:
        c = max(cnts, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        cx = (x + (w // 2))  # trova il punto medio
        area = w * h
        if area > 200:
            return True
    return False


def trovaVerde(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, light_green, dark_green)
    mask = cv2.erode(mask, None, iterations=3)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if len(cnts) > 0:
        listaAree = []
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            listaAree.append(nero(mask, c))
            cx = x + (w // 2)
            cy = y + (h // 2)

def nero(img, c):
    
