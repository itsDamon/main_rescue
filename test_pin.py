import RPi.GPIO as GPIO
import time

#set pin
pin1d=27 #pin 13 D3
pin2d=22 #pin 15 D4
#set pinmod
GPIO.setmode(GPIO.BCM) #enable gpio
GPIO.setup(pin1d, GPIO.OUT) #set pin output
GPIO.setup(pin2d, GPIO.OUT) #set pin output

time.sleep(2)
GPIO.output(pin1d, GPIO.HIGH)
GPIO.output(pin2d, GPIO.LOW)

print("pino")