from time import sleep

import cv2
import imutils
from picamera2 import Picamera2

from variabiliGlobali import *

cv2.startWindowThread()  # permette l'aggiornamento di cv2.imshow()
camera = Picamera2()  # assegna la videocamera e assegna il video a camera
camera.configure(
    camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (MAXX, MAXY)}))  # configura la videocamera
camera.controls.Brightness = 0
camera.set_controls({"ExposureTime": EXPOSURE, "AnalogueGain": 1.0, "AeEnable": 0})  # controllo esposizione
camera.start()  # avvia la videocamera
sleep(2)  # pausa 2s


def filtro(img):  # converte l'immagine in bianco e nero invertito,(nero reale=bianco e viceversa)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # converte l'immagine da bgr a grayscale
    (T, threshed) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)  # converte in bianco e nero l'immagine
    threshed = cv2.erode(threshed, None, iterations=3)
    copy = threshed.copy()
    cv2.rectangle(copy, (MAXX - offset - dim, MINY), (MAXX - offset, CROPSTART - 10), (255, 0, 0))
    cv2.rectangle(copy, (offset, MINY), (dim + offset, CROPSTART - 10), (255, 0, 0))
    cv2.imshow("Tresh", copy)  # la mostra a video
    return threshed


def lookup(originale):
    mask = originale[MINY2:MINY, 0:MAXX]
    cv2.imshow("incrocio", mask)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if len(cnts) != 0:
        c = max(cnts, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        cx = (x + (w // 2))  # trova il punto medio
        if cx > (MAXX // 2) + 25:
            return 1  # gira a destra
        elif cx < (MAXX // 2) - 25:
            return 2  # gira a sinistra
        else:
            return 3
    return -1


def findBordi(originale, ymin, ymax):
    mask = originale[ymin:ymax, 20:MAXX - 20]
    cv2.imshow("nero", mask)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if len(cnts) != 0:
        c = max(cnts, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        cx = (x + (w // 2))  # trova il punto medio
        # print(w)
        controllo = 1
        if w > 60:
            controllo = incrocio(originale, MINY, ymin)
            if controllo != 4:
                return controllo
            else:
                controllo = 10
        # print(cx)
        if cx > (MAXX // 2) + 25:
            return 1 * controllo  # gira a destra
        if cx < (MAXX // 2) - 25:
            return 2 * controllo  # gira a sinistra

    return 3  # vai dritto


'''
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
'''


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
    if destra == 4 or sinistra == 4:
        return lookup(originale)
        #pino = incrocio(originale, MINY2, ymin)
        #if pino != 4:
        #   return pino
        # elif pino == 4:
        #     return lookup(originale)
    if (destra or destra == 4) and not sinistra:
        return 1
    elif not destra and (sinistra or sinistra == 4):
        return 2
    return 3


direzione = 3
checkVerde = False
