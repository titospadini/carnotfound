# =============================================================
#
#                       -- ROBOCAR --
# 
# TIME: CarNotFound
# CARRO: 404
#  
# =============================================================
#
# DESCRICAO: meta01.py 
# Python versao: 2.7.12
# OpenCV versao: 4.0.0-pre
#
# Identifica um objeto de interesse na frente da camera e 
# movimenta um servo-motor de acordo com o movimento do objeto
# 
# =============================================================

import platform
import time
import numpy as np
import cv2 as cv

print 'Python versao:', platform.python_version()
#Python versao: 2.7.12

print 'OpenCV versao:', cv.__version__
#OpenCV versao: 4.0.0-pre

webcam = cv.VideoCapture(0) #objeto captura de frames
x0 = 0
y0 = 0

while(True):
	
    # Captura de frames
    s, rgb_frame = webcam.read()
    rgb_frame = cv.flip(rgb_frame, 1) # Espelha a imagem

    #Separa os canais da imagem
    gray_frame = cv.cvtColor(rgb_frame, cv.COLOR_BGR2GRAY)
    (blue_frame, green_frame, red_frame) = cv.split(rgb_frame)   

    diffframe_red = cv.subtract(red_frame, gray_frame)   
    diffframe_red = cv.medianBlur(diffframe_red, 3)
    T_red, bin_red = cv.threshold(diffframe_red, 40, 255, cv.THRESH_BINARY)

    # Exibe os frames resultantes 
    cv.imshow('Resultado', bin_red)
    M = cv.moments(bin_red)    
    if M['m00'] > 0:
    	x = int(M['m10']/M['m00'])
    	y = int(M['m01']/M['m00'])
    	if x > x0:
    		print 'direita'
    	elif x < x0:
    		print 'esquerda'
    	else:
    		print 'parado'
    	x0 = x
    	y0 = y
    else:
    	print 'Objeto nao encontrado'

    #time.sleep(0.3)

    #Fecha o loop - interrompe processo com 'q'
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    
#Encerrando processo
webcam.release() # Dispensa o uso da webcam
cv.destroyAllWindows() # Fecha todas a janelas abertas