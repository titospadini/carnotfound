#-*- coding: utf-8 -*-
# =============================================================
#
#                       -- ROBOCAR --
# 
# TIME: CarNotFound
# CARRO: 404
#  
# =============================================================
#
# DESCRICAO: CannyFilter.py 
# Python versao: 2 ou 3
#
# Aplica o efeito borda em vídeo
# =============================================================

#from transform import four_point_transform
import numpy as np
import argparse
import cv2

#substituir 'nissan.mp4' pela entrada de vídeo 
cap = cv2.VideoCapture('nissan.mp4')

 
while(1):
    ret, frame = cap.read()

    gray_vid = cv2.cvtColor(frame, cv2.IMREAD_GRAYSCALE)

    #exibe frames originais
    cv2.imshow('Original',frame)


    #aplica efeito de borda (edge) nos frames. O threshold depende da imagem
    edged_frame = cv2.Canny(frame, threshold1=100, threshold2=200)

    #exibe frames tratados. Use 'q' para sair
    cv2.imshow('Edges',edged_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()