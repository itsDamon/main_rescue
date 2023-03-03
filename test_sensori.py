import serial

from letturaSensoriLib import *

sensori = serial.Serial("/dev/ttyACM1", 9600)

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
'''
print("sinistra")
svuota(sensori)
accendiUltrasuoniSinistra(sensori)
sleep(1)
while True:
    print(sensori.read_until())
spegniSensoreInUso(sensori)


print("destra")
svuota(sensori)
accendiUltrasuoniDestra(sensori)
sleep(1)
print(sensori.readline())
spegniSensoreInUso(sensori)
