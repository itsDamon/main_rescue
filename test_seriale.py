import serial
from muoviMotoriLib import *
from letturaSensoriLib import *
from time import sleep

startpoint = 0
'''
try:
    test1 = serial.Serial("/dev/ttyACM0", 9600)
    startpoint += 1
except:
    try:
        test1 = serial.Serial("/dev/ttyACM1", 9600)
        startpoint += 1
    except:
        test1 = serial.Serial("/dev/ttyACM2", 9600)
        startpoint += 1

print(test1)

try:
    print("testing: ", startpoint)
    test2 = serial.Serial("/dev/tty/ACM" + str(startpoint), 9600)
except:
    startpoint += 1
    try:
        print("testing: ", startpoint)
        test2 = serial.Serial("/dev/tty/ACM" + str(startpoint), 9600)
    except:
        startpoint += 1
        try:
            print("testing: ", startpoint)
            test2 = serial.Serial("/dev/tty/ACM" + str(startpoint), 9600)
        except:
            test2 = "null"
'''
test1 = serial.Serial("/dev/ttyACM0", 9600)
test2 = serial.Serial("/dev/ttyACM1", 9600)
print(test1)
print(test2)
if check(test1) == 'y':
    motori = test1
    sensori = test2
else:
    motori = test2
    sensori = test1

# test motori
avanti(motori)
sleep(0.2)
stop(motori)

# test sensori
print("avanti")
accendiTofFrontale(sensori)
sleep(0.3)
print(sensori.readline())
spegniSensoreInUso(sensori)
sleep(0.3)

print("retro")
accendiTofRetro(sensori)
sleep(0.3)
print(sensori.readline())
spegniSensoreInUso(sensori)
sleep(0.3)

print("sinistra")
accendiUltrasuoniSinistra(sensori)
sleep(0.3)
print(sensori.readline())
spegniSensoreInUso(sensori)
sleep(0.3)

print("destra")
accendiUltrasuoniDestra(sensori)
sleep(0.3)
print(sensori.readline())
spegniSensoreInUso(sensori)
