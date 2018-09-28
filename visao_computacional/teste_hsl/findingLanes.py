#-*- coding: utf-8 -*-
# =============================================================
#
#                       -- ROBOCAR --
# 
# TIME: CarNotFound
# CARRO: 404
#  
# =============================================================

import cv2;
import numpy as np;
from matplotlib import pyplot as plt
 
#lendo a imagem
imagem = cv2.imread("b.jpg")

hsl = cv2.cvtColor(imagem, cv2.COLOR_BGR2HLS)


# range de branco em HSL
lower_white = np.array([0, 235, 0], dtype=np.uint8)
upper_white = np.array([255, 255, 255], dtype=np.uint8)

# aplica threshold para achar somente branco em HSL
mask = cv2.inRange(hsl, lower_white, upper_white)
res = cv2.bitwise_and(imagem, imagem, mask= mask)

#aplica gaussian blur
blur = cv2.GaussianBlur(res,(5,5),0)

#aplica canny edges para detecção de bordas
edges = cv2.Canny(blur, 100, 200)

#achando as linhas pelo método de hough
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 10, maxLineGap = 50)

#desenhando as linhas na imagem original
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(imagem, (x1, y1), (x2, y2), (0, 255, 0), 3)



cv2.imshow('blur', blur)
cv2.imshow('HoughLines', edges)
cv2.imshow('image', imagem)

cv2.waitKey(0)