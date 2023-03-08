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


def ostacolo(mot, sens):
    # retro(mot)
    # sleep(0.5)
    stop(mot)
    sleep(5)
    camera.stop()
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
            # if findAreaNera(img):
            #     controllo = 1
            #     break
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
        camera.start()
        for _ in range(15):
            frame = camera.capture_array()
            cv2.imshow("DopoOstacolo", frame)
        camera.stop()
        svuota(mot)
        stop(mot)
        print("Mario")
        sleep(5)
        print("La Vecchia")


cv2.startWindowThread()  # permette l'aggiornamento di cv2.imshow()
camera = Picamera2()  # assegna la videocamera e assegna il video a camera
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (MAXX, MAXY)}))  # configura la videocamera
camera.controls.Brightness = 0
camera.set_controls({"ExposureTime": 12000, "AnalogueGain": 1.0, "AeEnable": 0})  # controllo esposizione
camera.start()  # avvia la videocamera

false = True
mot, sens = motoriOSensori()
while false:
    im = camera.capture_array()
    cv2.imshow("Camera", im)
    ostacolo(mot, sens)
