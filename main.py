import RPi.GPIO as GPIO

from muoviMotoriLib import *
from segui_linea_con_sensori import *

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
STATO = 0


def reset():
    global STATO, checkVerde, direzione
    checkVerde = False
    STATO = 1
    direzione = 3


GPIO.add_event_detect(pinReset, GPIO.FALLING, callback=reset, bouncetime=100)

if __name__ == '__main__':
    while True:
        if STATO == 0:
            stop(ser)
        elif STATO == 1:
            # Prende immagini dalla cam e le mostra a ogni iterazione del ciclo
            im = camera.capture_array()
            # im = cv2.flip(im, 0) #decommentare in caso che la videocamera è al contrario
            copia = im.copy()
            cv2.rectangle(copia, (MAXX - 30 - dim, 100), (MAXX - 30, MAXY - 10), (255, 0, 0))
            cv2.rectangle(copia, (30, 100), (dim + 30, MAXY - 10), (255, 0, 0))
            cv2.imshow("Camera", copia)  # mostra l'immagine a video

            if not checkVerde:
                imV = im[10:MAXY, 20:MAXX - 20]
                checkVerde = isverde(imV)
                print(f"verde {checkVerde}")
            else:
                imV = im[100:MAXY, 20:MAXX - 20]
                cv2.imshow("verde", imV)
                verde = isverde(imV)
                print(verde)
                if verde:
                    stop(ser)
                    verde = trova_Verde(im)
                    print("curvaVerde")
                    print(verde)
                    sleep(5)
                    if verde == 0:
                        stop(ser)
                        print("vstop")
                    if verde == 1:  # gira a destra
                        Sdestra(ser)
                        print("Vdestra")
                    elif verde == 2:  # gira a sinstra
                        Ssinistra(ser)
                        print("Vsinistra")
                    # break
                    checkVerde = False

            mask = filtro(im)  # chiama la funione filtro e assegna il valore a mask
            direzione = assegnaDirezione(mask, 100, MAXY - 10)
            # print(direzione)
            stop(ser)
            sleep(0.01)
            if direzione == 1:  # gira a destra
                destra(ser)
                print("destra")
            elif direzione == 2:  # gira a sinstra
                sinistra(ser)
                print("sinistra")
            elif direzione == 3:  # vai dritto
                avanti(ser)
                print("avanti")

    camera.close()
    cv2.destroyAllWindows()
