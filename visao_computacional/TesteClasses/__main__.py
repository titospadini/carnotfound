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
#from ImageHandler import ImageHandler
import platform
#import cv2
import time

#instanciando os objetos (o construtor da classe CarHandler precisa das portas do GPIO que serão utilizadas)
#objImageHandler = ImageHandler()
objCarHandler = CarHandler(8, 16, 10, 18, 12) #forwardA, forwardB, backwordsA, backwordsB, direction
#webcam = cv2.VideoCapture(0)

objCarHandler.setAngle(90)
objCarHandler.forward()
time.sleep(2)
objCarHandler.stop()
time.sleep(1)
objCarHandler.backward()
time.sleep(2)
objCarHandler.neutral()
time.sleep(1)
objCarHandler.cleanupPins()

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
	