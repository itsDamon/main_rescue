from test_sensori import *
from segui_linea_con_sensori import findAreaNera
from muoviMotoriLib import *


def ostacolo(cam, mot, sens):
    retro(mot)
    sleep(0.5)
    stop(mot)
    sinistra90(mot)
    controllo = 0
    while controllo != 1:
        x = 0
        while x == 0:
            accendiUltrasuoniSinistra(sens)
            x = str(sens.readLine()).strip().replace('\'', "")
            print(x)
            avanti(mot)
            sleep(0.1)
            stop(mot)
        spegniSensoreInUso(sens)
        while x == 1:
            im = cam.capture_array()
            if findAreaNera(im):
                controllo = 1
                break
            accendiUltrasuoniSinistra(sens)
            x = str(sens.readLine()).strip().replace('\'', "")
            print(x)
            avanti(mot)
            sleep(0.1)
            stop(mot)

        destra90(mot)
