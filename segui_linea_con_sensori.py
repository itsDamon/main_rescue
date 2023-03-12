from time import sleep

import cv2
import imutils
from picamera2 import Picamera2

from variabiliGlobali import *

cv2.startWindowThread()  # permette l'aggiornamento di cv2.imshow()
camera = Picamera2()  # assegna la videocamera e assegna il video a camera
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (MAXX, MAXY)}))  # configura la videocamera
camera.controls.Brightness = 0
camera.set_controls({"ExposureTime": 14000, "AnalogueGain": 1.0, "AeEnable": 0})  # controllo esposizione
camera.start()  # avvia la videocamera
sleep(2)  # pausa 2s

def incrocio(originale, ymin, ymax):
    destra = check_destra(originale, ymin, ymax)
    sinistra = check_sinistra(originale, ymin, ymax)

    if destra and sinistra:
        return 4
    elif destra and not sinistra:
        return 1
    elif not destra and sinistra:
        return 2
    return 4

def check_centro(originale, ymin, ymax):
    mask = originale[ymin:ymax, dim + offset : MAXX - offset - dim]
    cv2.imshow("sinistra", mask)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if len(cnts) != 0:
        c = max(cnts, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        area = h * w
        if areaValidaMin < area:
            return True
    return False

def check_sinistra(originale, ymin, ymax):
    mask = originale[ymin:ymax, offset:dim + offset]
    cv2.imshow("sinistra", mask)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if len(cnts) != 0:
        c = max(cnts, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        area = h * w
        if areaValidaMin < area < areaValidaMax:
            return True
        elif area >= areaValidaMax:
            return 4
    return False


def check_destra(originale, ymin, ymax):
    mask = originale[ymin:ymax, MAXX - offset - dim:MAXX - offset]
    cv2.imshow("destra", mask)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if len(cnts) != 0:
        c = max(cnts, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        area = h * w
        if areaValidaMin < area < areaValidaMax:
            return True
        elif area >= areaValidaMax:
            return 4
    return False


def assegnaDirezione(originale, ymin, ymax):
    destra = check_destra(originale, ymin, ymax)
    sinistra = check_sinistra(originale, ymin, ymax)
    centro = check_centro(originale, ymin, ymax)
    if centro :
        return 3
    if destra == 4 or sinistra == 4:
        pino = incrocio(originale, MINY2, ymin)
        if pino != 4:
            return pino
    if (destra or destra == 4) and not sinistra:
        return 1
    elif not destra and (sinistra or sinistra == 4):
        return 2
    return 3


direzione = 3
checkVerde = False

