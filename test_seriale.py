import serial
from muoviMotoriLib import *
from time import sleep

ser = serial.Serial ("/dev/ttyACM0", 9600)   
avanti(ser)
sleep(0.2)
stop(ser)
