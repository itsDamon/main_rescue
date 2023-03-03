import serial
from picamera2 import Picamera2

from libOstacolo import *

MAXX = 256
MAXY = 144
cv2.startWindowThread()  # permette l'aggiornamento di cv2.imshow()
camera = Picamera2()  # assegna la videocamera e assegna il video a camera
camera.configure(
    camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (MAXX, MAXY)}))  # configura la videocamera
camera.controls.Brightness = 0
camera.set_controls({"ExposureTime": 30000, "AnalogueGain": 1.0, "AeEnable": 0})  # controllo esposizione
camera.start()  # avvia la videocamer
sleep(2)

test1 = serial.Serial("/dev/ttyACM0", 9600)
test2 = serial.Serial("/dev/ttyACM1", 9600)
print(test1)
print(test2)
x = check(test1)

if x:
    motori = test1
    sensori = test2
else:
    motori = test2
    sensori = test1

# test motori
print("l")
print(motori)
ostacolo(motori, sensori)
while True:
    avanti(motori)
    sleep(1)
    retro(motori)
    sleep(1)
    stop(motori)
    sleep(1)
    destra(motori)
    sleep(1)
    sinistra(motori)
    sleep(1)

# test sensori

svuota(sensori)
print("avanti")
accendiTofFrontale(sensori)
sleep(0.3)
print("qui: ", str(sensori.readline())[2:3])
spegniSensoreInUso(sensori)
sleep(0.3)

svuota(sensori)
print("retro")
accendiTofRetro(sensori)
sleep(0.3)
print(sensori.readline())
spegniSensoreInUso(sensori)
sleep(0.3)

svuota(sensori)
print("sinistra")
accendiUltrasuoniSinistra(sensori)
sleep(0.3)
print(sensori.readline())
spegniSensoreInUso(sensori)
sleep(0.3)

svuota(sensori)
print("destra")
accendiUltrasuoniDestra(sensori)
sleep(0.3)
print(sensori.readline())
spegniSensoreInUso(sensori)

ostacolo(camera, motori, sensori)
