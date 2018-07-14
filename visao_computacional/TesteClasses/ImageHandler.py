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
# DESCRICAO: CarHandler.py 
# Python versao: 2
#
# Classe para manipular as imagens obtidas pela webcam com OpenCV.
#
# =============================================================

import cv2
import numpy as np
import time

class ImageHandler():

	#construtor da classe. O x0 sempre armazena a posição anterior da bolinha
	def __init__(self):
		self.x0 = 0

	#a função de tratar o frame recebe a imagem "pura" da webcam e a transforma na matriz binária que indica onde está vermelho
	def tratarFrame(self, frame):
		frame = cv2.flip(frame, 1)
		grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		(blueFrame, greenFrame, redFrame) = cv2.split(frame)
		diffFrameRed = cv2.subtract(redFrame, grayFrame)
		diffFrameRed = cv2.medianBlur(diffFrameRed, 15)
		TRed, binRed = cv2.threshold(diffFrameRed, 50, 255, cv2.THRESH_BINARY)
		return binRed

	#função que abre uma janela no sistema operacional para mostrar o vídeo com a imagem já tratada
	def exibirCaptura(self, binRed):
		cv2.imshow('Resultado', binRed)

	#função que verifica se o novo frame indica que a bolinha foi para a direita, esquerda, se está parada ou se não foi encontrada
	def verificarSituacao(self, binRed):
		M = cv2.moments(binRed)
		if M['m00'] > 0:
			x = int(M['m10'] / M['m00'])			
			if x > self.x0 + 10:
				situacao = "direita"
			elif x < self.x0 - 10:
				situacao = "esquerda"
			else:
				situacao = "parado"
			self.x0 = x #a posição nova se torna a posição antiga
		else:
			situacao = "naoencontrado"
		return situacao
