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
		#print("Dimensões da imagem obtidas")		
		#tratamento da imagem		
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
		#print("Tratamento 1 completo")
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
		#_, cnts, _ = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		#for c in cnts:
			#se a area do contorno capturado for pequena, nada acontece
		#	if cv2.contourArea(c) < AreaContornoLimiteMin:
		#		continue						
		#	QtdeContornos = QtdeContornos + 1
			#obtem coordenadas do contorno (na verdade, de um retangulo que consegue abrangir todo ocontorno) e
			#realca o contorno com um retangulo.
		#	(x, y, w, h) = cv2.boundingRect(c)   #x e y: coordenadas do vertice superior esquerdo #w e h: respectivamente largura e altura do retangulo
			#cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
			#determina o ponto central do contorno e desenha um circulo para indicar
		#	CoordenadaXCentroContorno = (x+x+w)//2
		#	CoordenadaYCentroContorno = (y+y+h)//2
			#PontoCentralContorno = (CoordenadaXCentroContorno,CoordenadaYCentroContorno
			
		M = cv2.moments(img)
		if M['m00'] > 0:
			CoordenadaXCentroContorno = int(M['m10']/M['m00'])
			CoordenadaYCentroContorno = int(M['m01']/M['m00'])
			print ('Xcenter: ' + str(CoordenadaXCentroContorno))
		else:
			pass	   
				
		return CoordenadaXCentroContorno, CoordenadaYCentroContorno, QtdeContornos

class ImageHandlerMomentos():
	def preProcessamento(self,img):			
		#print("Dimensões da imagem obtidas")		
		#tratamento da imagem		
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)		
		img = cv2.GaussianBlur(img, KERNEL_GAUSSIAN_BLUR, 0)		
		#cv2.waitKey(1)
		img = cv2.threshold(img, LimiarBinarizacao, 255, cv2.THRESH_BINARY)[1]
		#img = cv2.dilate(img, None, iterations = QUANTIDADE_ITERACOES_DILATE)
		img = cv2.bitwise_not(img)
		#cv2.imshow('final',img)
		#cv2.waitKey(1)
		#print("Tratamento 1 completo")
		return img
		
	def deteccaoDeCurvas(self, img):
		#obtencao das dimensoes da imagem
		height = np.size(img, 1)
		width= np.size(img, 0)
		#DirecaoASerTomada = 0
		QtdeContornos = 0
		CoordenadaXtarget = width/2
		CoordenadaXCentroContorno = width//2
		CoordenadaYCentroContorno = height//2
		
			
		M = cv2.moments(img)
		if M['m00'] > 0:
			CoordenadaXCentroContorno = int(M['m10']/M['m00'])
			CoordenadaYCentroContorno = int(M['m01']/M['m00'])
			print ('Xcenter: ' + str(CoordenadaXCentroContorno))
		else:
			pass	   
				
		#return CoordenadaXCentroContorno, CoordenadaYCentroContorno, QtdeContornos
		return CoordenadaXCentroContorno, CoordenadaYCentroContorno
		
	def criaRois(self,img):
		#cria três regiões de interesse
		height = np.size(img, 0)
		
		img = self.preProcessamento(img)
		#cv2.imshow('imag',img)
		#cv2.waitKey(1)
		cut1 = height//3
		cut2 = 2*cut1

		roi1 = img[0:cut1,:]
		roi2 = img[cut1:cut2,:]
		roi3 = img[cut2:height,:]
		
		return roi1, roi2, roi3
#	def interpolacao
	def tratarImagem(self,img):
		roi1, roi2, roi3 = self.criaRois(img)
		print(1)
		x1, y1 = self.deteccaoDeCurvas(roi1)
		print(2)
		x2, y2 = self.deteccaoDeCurvas(roi2)
		print(3)
		x3, y3 = self.deteccaoDeCurvas(roi3)
		
		x = np.array([x1,x2,x3])
		y = np.array([y1,y2,y3])
		
		A = np.vstack([y, np.ones(len(y))]).T
		
		m, c = np.linalg.lstsq(A, x, rcond=None)[0]
		if m>0:
			print((np.degrees(np.arctan(m))+180)%180 + 90)
			return (np.degrees(np.arctan(m))+180)%180 + 90
		else:
			print((np.degrees(np.arctan(m))+180)%180 - 90)
			return (np.degrees(np.arctan(m))+180)%180 - 90
			
class ImageHandlerRetangulos():

	def salvaImagemAtual(self):
		cv2.imwrite('imagemAtual.png',self.imagemAtual)
		
	def salvaDadosAtuais(self):
		with open(DATA_PATH + 'dadosAtuais.txt','w') as file:
			text = ''
			text += 'x: ' + str(self.x) + '\n'
			text += 'y: ' + str(self.y) + '\n'
			text += 'angulo: ' + str(self.angulo) + '\n'
			file.write(text)
			
	def preProcessamento(self,img):			
		self.originalImage = img.copy()
		#print("Dimensões da imagem obtidas")		
		#tratamento da imagem		
#		cv2.imshow('original',img)
		cv2.waitKey(1)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		img = cv2.equalizeHist(img)
		img = cv2.GaussianBlur(img, KERNEL_GAUSSIAN_BLUR, 0)		
		#cv2.waitKey(1)
		#img = cv2.threshold(img, LimiarBinarizacao, 255, cv2.THRESH_BINARY)[1]
		img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 30)
		#img = cv2.dilate(img, None, iterations = QUANTIDADE_ITERACOES_DILATE)
		img = cv2.bitwise_not(img)
#		cv2.imshow('final',img)
		cv2.waitKey(1)
		#print("Tratamento 1 completo")
		return img
		
	def deteccaoDeCurvas(self, img):
		#obtencao das dimensoes da imagem
		height = np.size(img, 1)
		width= np.size(img, 0)
		#DirecaoASerTomada = 0
		angulo_retangulo = 90.0#ângulo default para caso de nenhum contorno ser detectado
		QtdeContornos = 0
		#CoordenadaXtarget = width/2
		CoordenadaXCentroContorno = ROI_WIDTH//2
		CoordenadaYCentroContorno = ROI_HEIGTH//2
		_, cnts, _ = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		for c in cnts:
			
			if cv2.contourArea(c) < AreaContornoLimiteMin:#filtra por área do contorno
				continue						
			

			#obtem coordenadas do contorno (na verdade, de um retangulo que consegue abrangir todo ocontorno) e
			#realca o contorno com um retangulo.
			retangulo = cv2.minAreaRect(c)
			
			#pega centróide, largura e altura do retângulo e arredonda para inteiros
			((x,y),(w,h),_) = retangulo
			x=(int)(x)
			y=(int)(y)
			w=(int)(w)
			h=(int)(h)
			
			try:#tenta pegar aspect ratio
				aspectRatio_retangulo = self.aspectRatio(retangulo)
			except ZeroDivisionError:
				continue
			if aspectRatio_retangulo>ASPECT_RATIO_MAX:#filtra retângulos por aspect ratio
				continue
			
			QtdeContornos = QtdeContornos + 1	
			angulo_retangulo = self.anguloDoRetangulo(retangulo)
			
			#desenha retângulo na imagem
			caixa = cv2.boxPoints(retangulo)
			caixa = np.int0(caixa)
			cv2.drawContours(self.originalImage,[caixa],0,(0,255,0),3)
			
			
			#self.escreveTexto(self.originalImage, str(angulo_retangulo),(y,x))#escreve ângulo do retângulo
			#self.escreveTexto(self.originalImage, str(cv2.contourArea(c)),(y,x))#escreve área do contorno
			#self.escreveTexto(self.originalImage, str(self.areaRetangulo(retangulo)),(y,x))#escreve área do retangulo
			#self.escreveTexto(self.originalImage, str(y) + ',' +str(x),(x,y), cor = (255,0,0))#escreve área do retangulo
			
			#determina o ponto central do contorno e desenha um circulo para indicar
			CoordenadaXCentroContorno = x
			CoordenadaYCentroContorno = y
			
			#salva dados para armazenamento ao sair do programa
			self.x = x
			self.y = y
			self.angulo = angulo_retangulo
			self.imagemAtual = self.originalImage
			
			#desenha círculo no centróide encontrado
			cv2.circle(self.originalImage,(x,y), 10, (0,0,255), -1)
		
		#desenha linha
		cv2.line(self.originalImage,(ROI_WIDTH//2,0),(ROI_WIDTH//2,ROI_HEIGTH),(255,255,255),2)
		
		
#		cv2.imshow('img',self.originalImage)
		#cv2.waitKey(1)
		
		return CoordenadaXCentroContorno, CoordenadaYCentroContorno, angulo_retangulo#retorna também último ângulo detectado
		
	def anguloDoRetangulo(self, retangulo):
		"""calcula o ângulo de retangulo dado pela função minAreaRect"""
		#retângulo armazena ângulos de uma forma que é necessário fazer uns ajustes para conseguir o ângulo corretamente
		largura = retangulo[1][0]
		altura = retangulo[1][1]
		angulo = retangulo[2]
		if largura < altura:
			angulo = 90-angulo
		if angulo<0:
			angulo = abs(angulo)
		return round(angulo,2)
		
	def aspectRatio(self,retangulo):
		largura = min(retangulo[1][0],retangulo[1][1])
		altura = max(retangulo[1][0],retangulo[1][1])

		aspectRatio = largura/altura

		return round(aspectRatio,2)
		
	def areaRetangulo(self,retangulo):
		return round(retangulo[1][0]*retangulo[1][1],2)
		
	def escreveTexto(self, img,texto,coord, cor = (0,255,0)):
		"""escreve texto na imagem"""
		fonte = cv2.FONT_HERSHEY_PLAIN
		escala = 2
		linha = 2

		cv2.putText(img,texto, coord, fonte, escala, cor, linha)
class ImageHandlerMultiProc():
	"""versão de ImageHandler que tenta paralelizar processamento - no momento é mais devagar"""
	def __init__(self):
		
		self.qtdeProcessos = 3
		self.inputs = mp.Queue(self.qtdeProcessos) #cria uma fila para armazenar entradas
		self.outputs = mp.Queue(self.qtdeProcessos) #cria uma fila para armazenar resultados
		

		#cria um processo para cada core
		self.processes = [mp.Process(target=self.multiprocessamento) for i in range(self.qtdeProcessos)]

		#inicia cada processo
		for p in self.processes:
			p.start()
	
	def tratarImagem(self,img):
		"""Realiza operação com multiprocessamento"""

		#cria três regiões de interesse, cada uma será enviada para um core
		height = np.size(img, 0)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		cut1 = height//3
		cut2 = 2*cut1

		roi1 = img[0:cut1,:]
		roi2 = img[cut1:cut2,:]
		roi3 = img[cut2:height,:]

		self.inputs.put(roi1)
		self.inputs.put(roi2)
		self.inputs.put(roi3)
		
		#espera fila de saídas estar cheia
		while(not self.outputs.full()):
			continue   
				
		#pega resultados da fila

		resultados = [self.outputs.get() for p in self.processes]
		
		cent_x = 0
		cent_y = 0
		qtdeContornos =0
		
		for cx, cy, qtCont in resultados:
			cent_x += cx
			cent_y += cy
			qtdeContornos += qtCont
			
		return cent_x/3, cent_y/3, qtdeContornos
		
	def multiprocessamento(self):
		#roda continuamente, lendo entradas da fila inputs e escrevendo resultados na fila outputs
		while(True):
			#enquanto fila de inputs estiver vazia, faz nada
			if(self.inputs.empty()):
				continue
				
			#tenta ler de inputs e processar, caso ocorra erro, faz nada
			try:
				img = self.inputs.get()
				img = self.preProcessamento(img)
				result = self.deteccaoDeCurvas(img)
				self.outputs.put(result)
			except KeyboardInterrupt:
				break
			except:
				continue
				
	def preProcessamento(self,img):			
		#print("Dimensões da imagem obtidas")		
		#tratamento da imagem		
		#img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)		
		img = cv2.GaussianBlur(img, KERNEL_GAUSSIAN_BLUR, 0)		
		#cv2.waitKey(1)
		img = cv2.threshold(img, LimiarBinarizacao, 255, cv2.THRESH_BINARY)[1]
		#img = cv2.dilate(img, None, iterations = QUANTIDADE_ITERACOES_DILATE)
		#img = cv2.bitwise_not(img)
		#cv2.imshow('final',img)
		#cv2.waitKey(1)
		#print("Tratamento 1 completo")
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
		#_, cnts, _ = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		#for c in cnts:
			#se a area do contorno capturado for pequena, nada acontece
		#	if cv2.contourArea(c) < AreaContornoLimiteMin:
		#		continue						
		#	QtdeContornos = QtdeContornos + 1
			#obtem coordenadas do contorno (na verdade, de um retangulo que consegue abrangir todo ocontorno) e
			#realca o contorno com um retangulo.
		#	(x, y, w, h) = cv2.boundingRect(c)   #x e y: coordenadas do vertice superior esquerdo #w e h: respectivamente largura e altura do retangulo
			#cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
			#determina o ponto central do contorno e desenha um circulo para indicar
		#	CoordenadaXCentroContorno = (x+x+w)//2
		#	CoordenadaYCentroContorno = (y+y+h)//2
			#PontoCentralContorno = (CoordenadaXCentroContorno,CoordenadaYCentroContorno
			
		M = cv2.moments(img)
		if M['m00'] > 0:
			CoordenadaXCentroContorno = int(M['m10']/M['m00'])
			CoordenadaYCentroContorno = int(M['m01']/M['m00'])
			print ('Xcenter: ' + str(CoordenadaXCentroContorno))
		else:
			pass	   
				
		return CoordenadaXCentroContorno, CoordenadaYCentroContorno, QtdeContornos
