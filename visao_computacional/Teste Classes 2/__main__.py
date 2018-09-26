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
# Python versao: 2
#
# Arquivo principal que vai instânciar os objetos das classes CarHandler e 
# ImageHandler para mover o carrinho de acordo com as imagens obtidas pela camera
#
# =============================================================

import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from CarHandler import CarHandler
from ImageHandler import ImageHandler

#INSTANCIANDO OBJETOS DAS CLASSES IMAGEHANDLER E CARHANDLER
objImageHandler = ImageHandler()
objCarHandler = CarHandler()

#PREPARANDO A CAMERA
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)
print("CAMERA PREPARADA\n")

#PEGANDO FRAME POR FRAME PARA TRATAR E TOMAR UMA DECISAO
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	
	image = frame.array

	#DEPOIS DE CAPTURAR O FRAME EU TENTO TRATA-LO
	try:
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
	except (KeyboardInterrupt):
		objCarHandler.cleanupPins()
		exit(1)   

	rawCapture.truncate(0)