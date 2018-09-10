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
# Arquivo principal que vai instânciar os objetos das classes CarHandler e ImageHandler para mover o carrinho de acordo com as imagens obtidas pela webcam
#
# =============================================================

from CarHandler import CarHandler
from picamera import PiCamera
#from ImageHandler import ImageHandler
import platform
#import cv2
import time

#instanciando os objetos (o construtor da classe CarHandler precisa das portas do GPIO que serão utilizadas)
#objImageHandler = ImageHandler() # Objeto para ImageHandler
objCarHandler = CarHandler()
#webcam = cv2.VideoCapture(0)

camera = PiCamera() # Objeto para a Pi Camera
camera.rotation = 180 # Rotação da câmera porque ela está de ponta cabeça
camera.framerate = 25 # Taxa de captura de quadros

camera.start_recording('/home/pi/Desktop/Pedro/video_teste_02.h264')

objCarHandler.setAngle(90)
objCarHandler.forward()
time.sleep(2)
objCarHandler.stop()
time.sleep(1)
objCarHandler.backward()
time.sleep(2)
objCarHandler.neutral()
time.sleep(1)

# Libera os pinos
objCarHandler.cleanupPins()

# Finaliza gravação
camera.stop_recording()

#while True:
	#pegando o frame atual da webcam
	# s, frame = webcam.read() 

	#tratando o frame para saber onde está a bolinha vermelha
	# binRed = objImageHandler.tratarFrame(frame)

	#exibindo a imagem tratada (só use esse comando se seu raspberry tiver interface gráfica)
	#objImageHandler.exibirCaptura(binRed)

	#Verificando qual é a situacao da bolinha em relacao ao frame anterior e de acordo com a situacao, movendo o carro de um jeito diferente
	#situacao = objImageHandler.verificarSituacao(binRed)
	#if situacao == "naoencontrado":
	#	objCarHandler.stop() #para o carro
	#else:
	#	objCarHandler.forward() #acelera
	#	if situacao == "direita":
	#		objCarHandler.setAngle(75) #vira pra direita
	#	elif situacao == "esquerda":
	#		objCarHandler.setAngle(115) #vira pra esquerda
	#	else:
	#		objCarHandler.setAngle(90) #anda reto
	#time.sleep(0.1)
	