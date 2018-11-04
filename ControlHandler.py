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
from constants import *
class  ControlHandler():

	def Controle(self, x_contorno):
		
		dX = X_REF - x_contorno
		if dX == 0:
			beta = 0
			erro = 0
			alfa = 90
		else:
			alfa = np.degrees(np.arctan(Y_REF/dX))
			beta = 90 - abs(alfa)
			
			if dX > 0:
				erro = ((-1.0)*beta)/ANG_ERRO_MAX
			else:
				erro = beta/ANG_ERRO_MAX
		
		#TODO: implementar sinal de controle
		return erro, beta, alfa
			
			 
			
			
