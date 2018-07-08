# =============================================================
#
#                       -- ROBOCAR --
# 
# TIME: CarNotFound
# CARRO: 404
#  
# =============================================================
#
# DESCRICAO: camSmartphone.py 
# Python versao: 3.6.6
# OpenCV versao: 3.4.1
#
# Captura e exibe a imagem da câmera do Smartphone conectado 
# pelos endereço IP e Porta identificados na url.
# 
# =============================================================

from urllib import request
import cv2
import numpy as np
import time

# Substitua pela URL obtida pelo aplicativo IP Webcam (Android), 
# com IP:porta e mantendo o '/shot.jpg' ao final.
url='http://192.168.1.30:8080/shot.jpg'

x0 = 0
y0 = 0

while True:
    # Obtém a imagem a partir da câmera IP
    rgb_frame_Resp = request.urlopen(url)
    
    # Converte a imagem para um array de números 
    # inteiros de 0 a 255.
    rgb_frame_NP = np.array(bytearray(rgb_frame_Resp.read()),dtype=np.uint8)
    
    # Converte o array da imagem para um formato
    # mais comumente usado pelo OpenCV
    rgb_frame = cv2.imdecode(rgb_frame_NP,-1)

    rgb_frame = cv2.flip(rgb_frame, 1) # Espelha a imagem

    #Separa os canais da imagem
    gray_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2GRAY)
    (blue_frame, green_frame, red_frame) = cv2.split(rgb_frame)

    diffframe_red = cv2.subtract(red_frame, gray_frame)   
    diffframe_red = cv2.medianBlur(diffframe_red, 3)
    T_red, bin_red = cv2.threshold(diffframe_red, 40, 255, cv2.THRESH_BINARY)
	
	# Exibe a imagem capturada
    #cv2.imshow('IPWebcam',rgb_frame)
    cv2.imshow('Resultado', bin_red)

    M = cv2.moments(bin_red)    
    if M['m00'] > 0:
        x = int(M['m10'] / M['m00'])
        y = int(M['m01'] / M['m00'])
        if x > x0:
            print ('direita')
        elif x < x0:
            print ('esquerda')
        else:
            print ('parado')
        x0 = x
        y0 = y
    else:
        print ('Objeto nao encontrado')

    #Utilize isto para dar um "descanso" ao processador
    #time.sleep(0.1) 

    # Encerra o programa se precionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break