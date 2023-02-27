import serial
from letturaSensoriLib import *
from time import sleep

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
'''

print("destra")
accendiUltrasuoniDestra(sensori)
sleep(1)
while True:
    print(sensori.readline())
spegniSensoreInUso(sensori)
