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
# DESCRICAO: ROI.py 
# Python versao: 2 ou 3
#
# "ROI" é a sigla para "Region of Interest"
#
# Delimita a área do vídeo a ser processada (ignorando céu, 
# horizonte e algumas falhas na pista, por exemplo)
# =============================================================

import numpy as np
import cv2

#função que cria máscara que delimita a região útil (ROI)
#Parâmetros: 1- imagem // 2- array de vértices do polígono
def roi(img, vertices):
	mask = np.zeros_like(img)
	cv2.fillPoly(mask, vertices, 255)
	masked = cv2.bitwise_and(img, mask)
	return masked

#captura de vídeo
cap = cv2.VideoCapture('nissan.mp4')

while(1):
    ret, frame = cap.read()

    #converte video para gray scale
    gray_vid = cv2.cvtColor(frame, cv2.IMREAD_GRAYSCALE)

    #exibe frames originais
    cv2.imshow('Original',frame)

    #aplica efeito de borda (edge) nos frames. Threshold deve ser ajustado de acordo com o vídeo
    edged_frame = cv2.Canny(frame, threshold1=100, threshold2=200)

	#cada par ordenado são as coordenadas dos vértices que formam o polígono que determina a ROI
	#podem ser adicionados mais vértices para obter melhor ajuste da pista
    #vertices = np.array([[0,310],[350,300],[800,300],[1280,320],[1280,480],[750,430],[500,390],[220,400],[50,470],[0,720]]) #vértices para 'pista.mp4'
    vertices = np.array([[0,300],[300,230],[900,230],[1280,230],[1280,380],[900,405],[360,400],[0,400]]) 	#vértice para 'nissan.mp4'

	#imagem gerada, contendo apenas a ROI
    selected_image = roi(edged_frame, [vertices])

    #exibe frames apenas com Canny
    cv2.imshow('Canny Only', edged_frame)

    #exibe frames tratados. Use 'q' para sair
    cv2.imshow('Canny + ROI',selected_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()