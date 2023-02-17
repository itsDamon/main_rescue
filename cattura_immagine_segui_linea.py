from picamera.array import PiRGBArray
from picamera2 import Picamera2, Preview
import cv2
import numpy as np
import imutils
import serial
from time import sleep
import RPi.GPIO as GPIO
from muoviMotoriLib import *
from trovaVerdeLib import *

#set pin
pin1d=27 #pin 13 D3
pin2d=22 #pin 15 D4
#set pinmod
GPIO.setmode(GPIO.BCM) #enable gpio
GPIO.setup(pin1d, GPIO.OUT) #set pin output
GPIO.setup(pin2d, GPIO.OUT) #set pin output
ser = serial.Serial ("/dev/ttyACM0", 9600) #set porta seriale


MAXX=256
MAXY=144
cv2.startWindowThread()   #permette l'aggiornamento di cv2.imshow()
camera = Picamera2()      #assegna la videocamera e assegna il video a camera
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (MAXX, MAXY)})) #configura la videocamera
camera.start()            #avvia la videocamera
sleep(2)             #pausa 2s


def filtro(img):        #converte l'immagine in bianco e nero invertito,(nero reale=bianco e viceversa)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#converte l'immagine da bgr a grayscale
    (T, threshed) = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY_INV)#converte in bianco e nero l'immagine
    threshed=cv2.erode(threshed,None,iterations=3)
    cv2.imshow("Tresh", threshed)#la mostra a video
    return threshed

def findBordi(originale,ymin,ymax):
    mask = originale[ymin:ymax, 20:MAXX-20]
    cv2.imshow("nero",mask)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    if len(cnts) != 0:
        c = max(cnts, key = cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        cx = (x+(w//2))     #trova il punto medio
        #print(w)
        controllo = 1
        if w > 60:
            controllo = incrocio(originale,50,ymin)
            if controllo != 4:
               return controllo
            else:
                controllo = 10
        #print(cx)
        if cx>(MAXX//2)+25:
            return 1*controllo  #gira a destra
        if cx<(MAXX//2)-25:
            return 2*controllo  #gira a sinistra
        
    return 3 #vai dritto

def incrocio(originale,ymin,ymax):
    mask = originale[ymin:ymax, 20:MAXX-20]
    cv2.imshow("incrocio",mask)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    if len(cnts) != 0:
        c = max(cnts, key = cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        cx = (x+(w//2))     #trova il punto medio
        #print(w)
        if cx>(MAXX//2)+25:
            return 1  #gira a destra
        if cx<(MAXX//2)-25:
            return 2  #gira a sinistra  
        return 3 #vai dritto
    return 4 # bianc guarda indietro
    
hold=0          
direzione = 3
checkVerde = False

while True:
    #Prende immagini dalla cam e le mostra ad ogni iterazione del ciclo
    im = camera.capture_array()    
    #im = cv2.flip(im, 0) #decommentare in caso che la videocamera è al contrario
    cv2.imshow("Camera", im)  #mostra l'immagine a video
    #verde = Find_Verde(im)
    #if verde > -1:
    #    curva()
    mask = filtro(im) #chiama la funione filtro e assegna il valore a mask
    direzione = findBordi(mask,100,MAXY-10)  #ritorna la direnzione in cui è il robot e la assegna a direnzione
    if not checkVerde:
        imV = im[100:MAXY, 20:MAXX//2-20]
        checkVerde = isverde(im)
        #print(f"verde {hverde}")
    else:
        imV = im[100:MAXY, 20:MAXX-20]
        cv2.imshow("verde",imV)
        verde = isverde(imV)
        print(verde)
        if verde:
            verde = trova_Verde(im)
            print("curvaVerde")
            print(verde)
            stop(ser)
            if verde == 0:
                break
            curva(ser,verde,camera)
            checkVerde = False
            direnzione = 3
            hold=5
    #else:
    if direzione != hold:
        hold = direzione
        stop(ser)
        if direzione == 1:   #gira a destra
            destra(ser)
            print("destra")
        elif direzione == 2: #gira a sinstra
            sinistra(ser)
            print("sinistra")
        elif direzione == 3:                #vai dritto
            avanti(ser)
            print("avanti")
        elif direzione >= 10:
            print("curva")
            print(direzione)
            stop(ser)
            sleep(1)
            direzione = int( direzione / 10)
            curva(ser,direzione,camera)
            retro(ser)
            sleep(0.6)   
                
camera.close()

'''
    if __name__ == '__main__':
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0)
        ser.reset_input_buffer()
        
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)
    '''