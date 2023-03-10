import RPi.GPIO as GPIO

from letturaSensoriLib import motoriOSensori
from muoviMotoriLib import *
from nuovoTrovaVerdeLibPaganiV2 import *
from segui_linea_con_sensori import *

motori, sensori = motoriOSensori()

# set pin
pinReset = 27  # pin 13 D3
# set pin mode
GPIO.setmode(GPIO.BCM)  # enable gpio
GPIO.setup(pinReset, GPIO.IN)  # set pin output
# setup thread per reset
GPIO.setup(pinReset, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# variabili
direzione = 3
checkVerde = False
STATO = 1


def reset():
    global STATO, checkVerde, direzione
    checkVerde = False
    STATO = 1
    direzione = 3


GPIO.add_event_detect(pinReset, GPIO.FALLING, callback=reset, bouncetime=100)

if __name__ == '__main__':
    while True:
        if STATO == 0:
            stop(motori)
        elif STATO == 1:
            # Prende immagini dalla cam e le mostra a ogni iterazione del ciclo
            im = camera.capture_array()
            # im = cv2.flip(im, 0) #decommentare in caso che la videocamera è al contrario
            copia = im.copy()
            cv2.rectangle(copia, (MAXX - offset - dim, MINY), (MAXX - offset, CROPSTART - 10), (255, 0, 0))
            cv2.rectangle(copia, (offset, MINY), (dim + offset, CROPSTART - 10), (255, 0, 0))
            cv2.imshow("Camera", copia)  # mostra l'immagine a video

            verde = trovaVerde(im)
            print(verde)
            if verde == 0:
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
            stop(motori)
            sleep(0.01)
            if direzione == 1:  # gira a destra
                destra(motori)
                print("destra")
            elif direzione == 2:  # gira a sinistra
                sinistra(motori)
                print("sinistra")
            elif direzione == 3:  # vai dritto
                avanti(motori)
                print("avanti")

'''
camera.close()
cv2.destroyAllWindows()
'''
