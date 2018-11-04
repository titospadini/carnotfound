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
		#mostrando imagem original
		#cv2.imshow('imagem original',img)
		
		img = img[ROI_Y1:ROI_Y2,ROI_X1:ROI_X2]#pega região de interesse
		
		self.orgImg = img #salva imagem original para desenhar em cima
		
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)		
		
		#img = cv2.equalizeHist(img)
		
		img = cv2.GaussianBlur(img, KERNEL_GAUSSIAN_BLUR, 0)		
		
		img = cv2.threshold(img, LimiarBinarizacao, 255, cv2.THRESH_BINARY)[1]
		
		img = cv2.bitwise_not(img)
		
		#img = cv2.morphologyEx(img, cv2.MORPH_OPEN, KERNEL_OPENING)
		
		#mostar imagem após processada
#		cv2.imshow('final',img)
#		cv2.waitKey(1)
		return img
		
	def deteccaoDeCurvas(self, img):
		
		
		CoordenadaXCentroContorno = X_REF
		CoordenadaYCentroContorno = Y_REF
		
		M = cv2.moments(img)
		
		if M['m00'] > 0:
			CoordenadaXCentroContorno = int(M['m10']/M['m00'])
			CoordenadaYCentroContorno = int(M['m01']/M['m00'])
		else:
			pass  	
			
		#desenha círculo na centróide
		cv2.circle(self.orgImg,(CoordenadaXCentroContorno,CoordenadaYCentroContorno), 5, (0,0,255), -1)
		
		#desenha linhas
		cv2.line(self.orgImg,(X_REF,0),(X_REF,ROI_HEIGTH),(255,255,255),2)
		cv2.line(self.orgImg,(0,Y_REF),(ROI_WIDTH,Y_REF),(255,255,255),2)
		
		#mostra imagem com referências
		cv2.imshow('roi', self.orgImg)
		cv2.waitKey(1)
		
		return CoordenadaXCentroContorno, CoordenadaYCentroContorno


