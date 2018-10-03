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
# DESCRICAO: __main__.py 
# Python versao: 3
#
# Arquivo principal que vai instânciar os objetos das classes 
# CarHandler e ImageHandler para mover o carrinho de acordo 
# com as imagens obtidas pela webcam
#
# =============================================================

import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from CarHandler import CarHandler
from ImageHandler import ImageHandler

# INSTANCIANDO OBJETOS DAS CLASSES IMAGEHANDLER E CARHANDLER
objImageHandler = ImageHandler() # Objeto para ImageHandler
objCarHandler = CarHandler()

#PREPARANDO A CAMERA
camera = PiCamera() # Objeto para a Pi Camera
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)
print("CAMERA PREPARADA\n")

time.sleep(0.5)
print("Executando rotina de teste dos motores.")

objCarHandler.setAngle(90)
time.sleep(10) # Espera 10 segundoa antes de sair andando para dar tempo de eu sair lá fora
objCarHandler.forward()
time.sleep(2)
objCarHandler.setAngle(60)
time.sleep(2)
objCarHandler.setAngle(90)
time.sleep(2)
objCarHandler.setAngle(115)
time.sleep(2)
objCarHandler.setAngle(90)
time.sleep(2)
objCarHandler.stop()
time.sleep(2)
objCarHandler.backward()
time.sleep(2)
objCarHandler.neutral()

print("Fom da rotina de teste dos motores.")
time.sleep(0.5)
print("Iniciando rotina de tomada de decisão a partir das imagens da câmera.")

#PEGANDO FRAME POR FRAME PARA TRATAR E TOMAR UMA DECISAO
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	
	image = frame.array
	print("Frame Capturado")
	#DEPOIS DE CAPTURAR O FRAME EU TENTO TRATA-LO
	try:
		#print("Tentando tratar frame")
		Direcao, QtdeLinhas = objImageHandler.tratarImagem(image)

		#DEPOIS DE TRATAR, EU TOMO UMA DECISAO
		if (QtdeLinhas == 0):
			print("PARE")
			objCarHandler.stop();
		else:
			objCarHandler.forward();
			if (Direcao > 0):
				print("DIREITA")
				objCarHandler.setAngle(115)
			if (Direcao < 0):
				print("ESQUERDA")
				objCarHandler.setAngle(75)
			if (Direcao == 0):
				print("EM FRENTE")
				objCarHandler.setAngle(90)
		#print("Frame tratado")
	except (KeyboardInterrupt):
		objCarHandler.cleanupPins()
		exit(1)

	rawCapture.truncate(0)	

# Libera os pinos
objCarHandler.cleanupPins()