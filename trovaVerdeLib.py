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


def trova_Verde(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, light_green, dark_green)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cv2.imshow("verde", mask)
    if len(cnts) != 0:
        c = max(cnts, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        cx = (x + (w // 2))  # trova il punto medio
        area = w * h
        # print(area)
        if area > 100:  # contralla se l'area è valida
            if y > 10:  # controlla se ha la riga nera sopra
                nero = nero_presente(img, y - 7, cx)
                if nero:
                    if len(cnts) > 1:  # controlla se ci son 2 quadrati validi per retromarcia
                        c2 = cnts[1]
                        x2, y2, w2, h2 = cv2.boundingRect(c2)
                        a2 = w2 * h2
                        print(a2)
                        if a2 > 100:
                            if y2 > 10 and a2 < area:
                                nero = nero_presente(img, y2 - 7, x2 + (w2 // 2))
                                if nero:
                                    return 0  # indietro
                    if 10 < x < 125:  # controlla che si deve girare a destra
                        nero = nero_presente(img, y + (h // 2), x - 7)
                        if nero:
                            return 1  # destra
                    if x > 125:  # controlla se si deve girare a sinistra
                        nero = nero_presente(img, y + (h // 2), x + w + 2)
                        if nero:
                            return 2  # sinistra
                    if x < 10:  # in caso che sia attaca al bordo di sinistra curva a destra
                        return 1  # destra
                    if x + w > 246:  # in caso che sia attaca al bordo di destra curva a sinistra
                        return 2  # sinistra
    return -1


def nero_presente(img, y, cx):  # dice se c'è presente del nero
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (T, nero) = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY_INV)
    crop = nero[y:y + 5, cx:cx + 5]
    color = crop[4, 4]
    if color == 255:
        return True
    return False
