from picamera2 import Picamera2, Preview
import cv2
import numpy as np
import time

# capture frames from a camera
MAXX=256
MAXY=144
cv2.startWindowThread()   #permette l'aggiornamento di cv2.imshow()
camera = Picamera2()      #assegna la videocamera e assegna il video a camera
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (MAXX, MAXY)})) #configura la videocamera
camera.start()            #avvia la videocamera
time.sleep(2)
  
# read the frames from the camera

def isNero(img, x, y):
    count = 0
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (T, nero) = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY_INV)
    crop = nero[y:y+5, x:x+5]
    for row in crop:
        for pixel in row:
            if pixel == 255:
                count += 1
    if count >= 15:
        return "trovato"
    return "assente"
    
  
# loop runs if capturing has been initialized. 
while True:
    # reads frames from a camera 
    im = camera.capture_array()
    copia = im.copy()
    copia = cv2.cvtColor(copia, cv2.COLOR_BGR2GRAY)
    #img = cv2.medianBlur(img,5)
    # Find circles
    circles = cv2.HoughCircles(copia,cv2.HOUGH_GRADIENT,2,150,minRadius=20,maxRadius=50)
    # If some circle is found
    if circles is not None:
       # Get the (x, y, r) as integers
       circles = np.round(circles[0, :]).astype("int")
       print(circles)
       # loop over the circles
       for (x, y, r) in circles:
          print(isNero(im, x, y))
          cv2.circle(im, (x, y), r, (0, 255, 0), 2)
# show the output image
    cv2.imshow("circle",im)
    cv2.waitKey(1)
