#-*- coding: utf-8 -*-
# ===============================================================
#
#                       -- ROBOCAR --
# 
# TIME: CarNotFound
# CARRO: 404
#  
# ===============================================================
#
# DESCRICAO: ROI.py 
# Python versao: 2 ou 3
#
# Detecta linhas no vídeo
#
#
# Contém funções para:
#   > aplicar efeito de borda (Canny)
#   > selecionar área do vídeo a ser processada (ROI)
#   > detectar linhas no vídeo (HoughLines)
#
# Obs: os parâmetros das funções 'Canny', 'array' (vértices) e 
#      'HoughLinesP' devem ser ajustados de acordo com a pista
# ===============================================================

import numpy as np
import cv2


#função que desenha linhas de borda da pista
#Parâmetros: 1- imagem // 2- informações sobre as linhas
def draw_lines(img, lines):
    try:
        for line in lines:
            coords = line[0]
            cv2.line(img, (coords[0],coords[1]), (coords[2],coords[3]), [255,255,255], 3)
    except:
        pass


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
    edged_frame = cv2.Canny(frame, threshold1=140, threshold2=200)

    #suaviza os "edged_frames"
    gaussFrame = cv2.GaussianBlur(edged_frame, (9,9), 0)

	#cada par ordenado são as coordenadas dos vértices que formam o polígono que determina a ROI
	#podem ser adicionados mais vértices para obter melhor ajuste da pista
    ##vertices = np.array([[0,310],[350,300],[800,300],[1280,320],[1280,480],[750,430],[500,390],[220,400],[50,470],[0,720]]) #vértices para 'pista.mp4'
    vertices = np.array([[0,300],[300,230],[900,230],[1280,230],[1280,720],[0,720]]) 	#vértice para 'nissan.mp4'
    ##vertices = np.array([[0,0],[480,0],[480,360],[0,360]]) ## 'album.mp4'
	
    #imagem gerada, contendo apenas a ROI
    selected_image = roi(gaussFrame, [vertices])

    #exibe frames com Canny e Desfoque Gaussiano
    cv2.imshow('Canny + Gaussian Blur', gaussFrame)


    #parâmetros das linhas que serão desenhadas
        #minLineLength >> espessura mínima da linha
        #maxLineGap >> espaço máximo entre as linhas
    lines = cv2.HoughLinesP(selected_image, 1, np.pi/180, 180, np.array([]), minLineLength=150, maxLineGap=15)
    draw_lines(selected_image, lines)



    #exibe frames tratados. Use 'q' para sair
    cv2.imshow('Canny + ROI + HoughLines',selected_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()