from time import sleep

import serial

n = 10


def svuota(ser):
    ser.flushInput()
    ser.flushOutput()
    ser.flush()


def accendiTofFrontale(ser):
    for _ in range(n):
        ser.write(b'f')


def accendiTofRetro(ser):
    for _ in range(n):
        ser.write(b'r')


def accendiUltrasuoniSinistra(ser):
    for _ in range(n):
        ser.write(b's')


def accendiUltrasuoniDestra(ser):
    for _ in range(n):
        ser.write(b'd')


def spegniSensoreInUso(ser):
    for _ in range(n):
        sleep(0.2)
        ser.write(b'0')


def check(ser):
    print("lon")
    svuota(ser)
    for _ in range(n):
        ser.write(b'?')
    sleep(0.3)
    x = str(ser.read_until())[2:3]
    print(x)
    for lettera in x:
        if lettera == 'y':
            return True
    return False


def motoriOSensori():
    test1 = serial.Serial("/dev/ttyACM2", 9600)
    test2 = serial.Serial("/dev/ttyACM3", 9600)
    print(test1)
    print(test2)
    x = check(test1)

    if x:
        motori = test1
        sensori = test2
    else:
        motori = test2
        sensori = test1
    return motori, sensori
