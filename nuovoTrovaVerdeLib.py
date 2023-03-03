import cv2
import imutils
import numpy as np

cv2.startWindowThread()
light_green = np.array([36, 50, 50])
dark_green = np.array([85, 255, 255])


def isverde(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, light_green, dark_green)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cv2.imshow("isverde", mask)
    if len(cnts) != 0:
        c = max(cnts, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        cx = (x + (w // 2))  # trova il punto medio
        area = w * h
        if area > 200:
            return True
    return False


def trovaVerde(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, light_green, dark_green)
    mask = cv2.erode(mask, None, iterations=3)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if len(cnts) > 0:
        listaAree = []
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            listaAree.append(nero(img, x, y, w, h))

        if len(listaAree) > 2:
            return -1

        isPrimaAreaNonTrovata = True
        direzione = -1
        for area in listaAree:
            if area["sopra"] and not area["sotto"]:
                if area["destra"] and isPrimaAreaNonTrovata:
                    direzione = 1
                    isPrimaAreaNonTrovata = False
                elif area["sinistra"] and isPrimaAreaNonTrovata:
                    direzione = 2
                    isPrimaAreaNonTrovata = False
                elif not isPrimaAreaNonTrovata and direzione == 2 and area["destra"]:
                    direzione = 0
                elif not isPrimaAreaNonTrovata and direzione == 1 and area["sinistra"]:
                    direzione = 0
        return direzione


def isNero(crop):
    count = 0
    for i in range(len(crop)):
        for j in range(len(crop)):
            pixel = crop[i:j]
            print(pixel)
            if pixel == 255:
                count += 1
    return count >= ((len(crop) * len(crop)) // 4) * 3


def nero(img, x, y, w, h):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # converte l'immagine da bgr a grayscale
    (T, threshed) = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY_INV)  # converte in bianco e nero l'immagine
    threshed = cv2.erode(threshed, None, iterations=3)
    cx = x + (w // 2)
    cy = y + (h // 2)

    sopra = img[y - 5:y - 1, cx - 3:cx + 3]
    sotto = img[y + h + 1:y + h + 5, cx - 3:cx + 3]
    destra = img[cy - 5:cy, x + w + 1:x + w + 5]
    sinistra = img[cy - 5:cy, x - 5: x - 1]
    area = {
        "sopra": isNero(sopra),
        "sotto": isNero(sotto),
        "destra": isNero(destra),
        "sinistra": isNero(sinistra)
    }
    return area
