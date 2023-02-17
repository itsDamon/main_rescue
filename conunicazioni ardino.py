import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

pin1d=5
pin2d=6
pin3d= 13
pin4=12

GPIO.output(pin1d, GPIO.LOW)
GPIO.output(pin2d, GPIO.LOW)
GPIO.output(pin3d, GPIO.LOW)
GPIO.output(pin4d, GPIO.LOW)