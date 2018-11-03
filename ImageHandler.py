#-*- coding: utf-8 -*-
# =============================================================
#
#					   -- ROBOCAR --
# 
# TIME: CarNotFound
# CARRO: 404
#  
# =============================================================
#
# DESCRICAO: CarHandler.py 
# Python versao: 3
#
# Classe para manipular as imagens obtidas pela webcam com OpenCV.
#
# =============================================================

import cv2
import numpy as np
import time
from constants import *
import multiprocessing as mp
class ImageHandler():
	def preProcessamento(self,img):	
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)		
		#img = cv2.equalizeHist(img)
		img = cv2.GaussianBlur(img, KERNEL_GAUSSIAN_BLUR, 0)		
		#cv2.waitKey(1)
		img = cv2.threshold(img, LimiarBinarizacao, 255, cv2.THRESH_BINARY)[1]
		#img = cv2.dilate(img, None, iterations = QUANTIDADE_ITERACOES_DILATE)
		#img = cv2.bitwise_not(img)
		img = cv2.morphologyEx(img, cv2.MORPH_OPEN, KERNEL_OPENING)
#		cv2.imshow('final',img)
#		cv2.waitKey(1)
		return img
		
	def deteccaoDeCurvas(self, img):
		#obtencao das dimensoes da imagem
		height = np.size(img, 1)
		width= np.size(img, 0)
		#DirecaoASerTomada = 0
		QtdeContornos = 0
		CoordenadaXtarget = width/2
		CoordenadaXCentroContorno = width/2
		CoordenadaYCentroContorno = height/2
		M = cv2.moments(img)
		if M['m00'] > 0:
			CoordenadaXCentroContorno = int(M['m10']/M['m00'])
			CoordenadaYCentroContorno = int(M['m01']/M['m00'])
			print ('Xcenter: ' + str(CoordenadaXCentroContorno))
		else:
			pass  	
		return CoordenadaXCentroContorno, CoordenadaYCentroContorno, QtdeContornos


