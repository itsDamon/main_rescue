import imutils
import cv2

from muoviMotoriLib import *
from letturaSensoriLib import *


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


def ostacolo(cam, mot, sens):
    retro(mot)
    sleep(0.5)
    stop(mot)
    sinistra90(mot)
    controllo = 0
    while controllo != 1:
        x = '0'
        while x == '0':
            svuota(sens)
            accendiUltrasuoniSinistra(sens)
            # x = str(sens.readLine()).strip().replace('\\PL', "")
            x = str(sens.readLine())[2:3]
            print(x)
            avanti(mot)
            sleep(0.1)
            stop(mot)
        spegniSensoreInUso(sens)
        while x == '1':
            svuota(sens)
            im = cam.capture_array()
            if findAreaNera(im):
                controllo = 1
                break
            accendiUltrasuoniSinistra(sens)
            # x = str(sens.readLine()).strip().replace('\\PL', "")
            x = str(sens.readLine())[2:3]
            print(x)
            avanti(mot)
            sleep(0.1)
            stop(mot)

        destra90(mot)
