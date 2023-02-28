import cv2
import serial
from picamera2 import Picamera2
from variabiliGlobali import *
from letturaSensoriLib import *
from time import sleep

cv2.startWindowThread()  # permette l'aggiornamento di cv2.imshow()
camera = Picamera2()  # assegna la videocamera e assegna il video a camera
camera.configure(
    camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (MAXX, MAXY)}))  # configura la videocamera
camera.set_controls({"ExposureTime": 13000, "AnalogueGain": 1.0})  # controllo esposizione
camera.start()  # avvia la videocamera
sleep(2)  # pausa 2s

try:
    sensori = serial.Serial("/dev/ttyACM0", 9600)
except:
    try:
        sensori = serial.Serial("/dev/ttyACM1", 9600)
    except:
        sensori = serial.Serial("/dev/ttyACM2", 9600)

# test sensori


'''
print("avanti")
accendiTofFrontale(sensori)
sleep(1)
while True:
    print(sensori.readline())
spegniSensoreInUso(sensori)
sleep(1)

print("retro")
accendiTofRetro(sensori)
sleep(1)
print(sensori.readline())
spegniSensoreInUso(sensori)
sleep(1)

print("sinistra")
accendiUltrasuoniSinistra(sensori)
sleep(1)
print(sensori.readline())
spegniSensoreInUso(sensori)
sleep(1)


print("destra")
accendiUltrasuoniDestra(sensori)
sleep(1)
print(sensori.readline())
spegniSensoreInUso(sensori)
'''
