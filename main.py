import RPi.GPIO as GPIO

from letturaSensoriLib import motoriOSensori
from muoviMotoriLib import *
from nuovoTrovaVerdeLibPaganiV2 import *
from segui_linea_con_sensori import *
import sys

motori, sensori = motoriOSensori()

# set pin
pinReset = 21  # pin 40
pinOstacolo = 2 #pin 38
# set pin mode
GPIO.setmode(GPIO.BCM)  # enable gpio
GPIO.setup(pinReset, GPIO.IN)  # set pin output
# setup thread per reset
GPIO.setup(pinReset, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pinOstacolo, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# variabili
direzione = 3
checkVerde = False
STATO = 1


def reset(channel):
    global STATO, checkVerde, direzione
    checkVerde = False
    STATO = 1
    print("RESETTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    direzione = 3
    sys.exit()


def setOstacolo():
    print("OSTACOLOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    stop(motori)
    STATO = 2


#GPIO.add_event_detect(pinReset, GPIO.FALLING, callback=reset, bouncetime=100)
#GPIO.add_event_detect(pinOstacolo, GPIO.RISING, callback=setOstacolo, bouncetime=1000)

if __name__ == '__main__':
    while True:
        if STATO == 0:
            stop(motori)
        elif STATO == 1:
            # Prende immagini dalla cam e le mostra a ogni iterazione del ciclo
            im = camera.capture_array()
            # im = cv2.flip(im, 0) #decommentare in caso che la videocamera Ã¨ al contrario
            copia = im.copy()
            cv2.rectangle(copia, (MAXX - offset - dim, MINY), (MAXX - offset, CROPSTART - 10), (255, 0, 0))
            cv2.rectangle(copia, (offset, MINY), (dim + offset, CROPSTART - 10), (255, 0, 0))
            cv2.imshow("Camera", copia)  # mostra l'immagine a video

            verde = trovaVerde(im)
            print(verde)
            if verde == 0:
                avanti(motori)
                sleep(0.8)
                curva180(motori)
                print("vstop")
            if verde == 1:  # gira a destra
                avanti(motori)
                sleep(0.8)
                destra90(motori)
                print("Vdestra")
            elif verde == 2:  # gira a sinistra
                avanti(motori)
                sleep(0.8)
                sinistra90(motori)
                print("Vsinistra")

            mask = filtro(im)  # chiama la funzione filtro e assegna il valore a mask
            direzione = assegnaDirezione(mask, MINY, CROPSTART - 10)
            # print(direzione)
            if direzione == 1:  # gira a destra
                destra(motori)
                print("destra")
                sleep(0.5)
            elif direzione == 2:  # gira a sinistra
                sinistra(motori)
                print("sinistra")
                sleep(0.5)
            elif direzione == 3:  # vai dritto
                avanti(motori)
                print("avanti")
            sleep(0.1)
            stop(motori)
            sleep(0.05)
        elif STATO == 2:
            ostacolo(motori)

'''
camera.close()
cv2.destroyAllWindows()
'''