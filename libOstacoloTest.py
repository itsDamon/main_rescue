import cv2
import imutils

from picamera2 import Picamera2
from variabiliGlobali import *

from letturaSensoriLib import *
from muoviMotoriLib import *


def findAreaNera(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (T, nero) = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow("Threshold", nero)
    cnts = cv2.findContours(nero.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if len(cnts) != 0:
        c = max(cnts, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        cx = (x + (w // 2))  # trova il punto medio
        area = w * h
        print(area)
        if area > 200:
            return True
    return False


def ostacolo(mot, sens, camera):
    # retro(mot)
    # sleep(0.5)
    stop(mot)
    sleep(5)
    camera.stop()
    svuota(mot)
    svuota(sens)
    sinistra90(mot)
    controllo = 0
    while controllo != 1:
        x = '0'
        while True:
            svuota(sens)

            accendiUltrasuoniDestra(sens)
            x = str(sens.read_until())[2:3]
            print(x)
            if x == '1':
                stop(mot)
                break
            avanti(mot)
            sleep(0.1)
            stop(mot)
            sleep(0.1)
        svuota(sens)
        spegniSensoreInUso(sens)
        print("fine vuoto")
        sleep(1)
        while True:
            camera.start()
            im = camera.capture_array()
            if findAreaNera(im):
                controllo = 1
                break
            camera.stop()
            svuota(mot)
            svuota(sens)
            accendiUltrasuoniDestra(sens)
            x = str(sens.read_until())[2:3]
            print(x)
            if x == '0':
                stop(mot)
                break
            avanti(mot)
            sleep(0.1)
            stop(mot)
            sleep(0.1)
        svuota(sens)
        spegniSensoreInUso(sens)
        print("fine pieno")
        destra90(mot)
        sleep(5)

false = True
mot, sens = motoriOSensori()
while false:
    im = camera.capture_array()
    cv2.imshow("Camera", im)
    ostacolo(mot, sens)
