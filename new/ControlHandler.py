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
# DESCRICAO: ControlHandler.py
# Python versao: 3
#
# Classe para manipular as imagens obtidas pela webcam com OpenCV.
#
# =============================================================
import numpy as np


class  ControlHandler():

	def Controle(self, x_contorno, x_target):
		max_error_px=x_target
		error = (x_contorno - x_target) / max_error_px
		#error = (x_target - x_contorno) / max_error_px		
		print('erro = ' + str(error)) 
			# -1 para curva a esquerda
			# 0 para reta
			# 1 para curva direita
		angle = 30*error + 90 #ajustar depois dos testes
		print('angle1 = ' + str(angle)) 
		return angle
			
	def Linearizacao(self,x,y):
		#V = np.array([x**1, x**0]).transpose()
		#coef = ((np.linalg.inv((V.transpose()).dot(V))).dot(V.transpose())).dot(y)
		coef = np.polyfit(x,y,1,full=False)		
		return coef
			
			
