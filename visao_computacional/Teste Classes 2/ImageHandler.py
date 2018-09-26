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

	def tratarImagem(self, img):
		LimiarBinarizacao = 125
		AreaContornoLimiteMin = 5000

		#obtencao das dimensoes da imagem
		height = np.size(img,0)
		width= np.size(img,1)
		QtdeContornos = 0
		DirecaoASerTomada = 0
		
		#tratamento da imagem
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (21, 21), 0)
		FrameBinarizado = cv2.threshold(gray,LimiarBinarizacao,255,cv2.THRESH_BINARY_INV)[1]
		FrameBinarizado = cv2.dilate(FrameBinarizado,None,iterations=2)
		FrameBinarizado = cv2.bitwise_not(FrameBinarizado)

		_, cnts, _ = cv2.findContours(FrameBinarizado.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cv2.drawContours(img,cnts,-1,(255,0,255),3)
		
		for c in cnts:
			#se a area do contorno capturado for pequena, nada acontece
			if cv2.contourArea(c) < AreaContornoLimiteMin:
				continue
						
			QtdeContornos = QtdeContornos + 1
			#obtem coordenadas do contorno (na verdade, de um retangulo que consegue abrangir todo ocontorno) e
			#realca o contorno com um retangulo.
			(x, y, w, h) = cv2.boundingRect(c)   #x e y: coordenadas do vertice superior esquerdo #w e h: respectivamente largura e altura do retangulo
			cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

			#determina o ponto central do contorno e desenha um circulo para indicar
			CoordenadaXCentroContorno = (x+x+w)//2
			CoordenadaYCentroContorno = (y+y+h)//2
			PontoCentralContorno = (CoordenadaXCentroContorno,CoordenadaYCentroContorno)
			cv2.circle(img, PontoCentralContorno, 1, (0, 0, 0), 5)
				
			DirecaoASerTomada = CoordenadaXCentroContorno - (width//2)   #em relacao a linha central
		 
		#output da imagem
		#linha em azul: linha central / referencia
		#linha em verde: linha que mostra distancia entre linha e a referencia
		cv2.line(img,(width//2,0),(width//2,height),(255,0,0),2)
		
		if (QtdeContornos > 0):
			cv2.line(img,PontoCentralContorno,(width//2,CoordenadaYCentroContorno),(0,255,0),1)
		
		cv2.imshow('Analise de rota',img)
		cv2.waitKey(10)
		
		return DirecaoASerTomada, QtdeContornos