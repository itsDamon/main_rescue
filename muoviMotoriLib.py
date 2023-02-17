def avanti(ser):
    for i in range(5):
        ser.write(b'a')


def stop(ser):
    for i in range(5):
        ser.write(b'w')


def destra(ser):
    for i in range(5):
        ser.write(b'D')


def Sdestra(ser):
    for i in range(5):
        ser.write(b'd')


def sinistra(ser):
    for i in range(5):
        ser.write(b'S')


def Ssinistra(ser):
    for i in range(5):
        ser.write(b's')


def retro(ser):
    for i in range(5):
        ser.write(b'b')
