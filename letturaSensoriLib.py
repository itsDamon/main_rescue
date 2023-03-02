from time import sleep

n = 10


def svuota(ser):
    ser.flushInput()
    ser.flushOutput()


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
