from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np


def calculaMatrizBEV(dstCols,dstRows,margemCols,margemRows):
		rowHigh = dstRows
		colHigh = dstCols - (int)(dstRows*margemCols)
		rowLow = (int)(dstRows*margemCols)
		colLow = 0 + (int)(dstRows*margemCols)
		pts1 = np.float32([[214,192],[0,330],[404,192],[640,330]])
		pts2 = np.float32([[colLow,rowLow],[colLow,rowHigh],[colHigh,rowLow],[colHigh,rowHigh]])
		return cv2.getPerspectiveTransform(pts1,pts2)
	
def birdEyeView(img,matriz):
		return cv2.warpPerspective(img,matriz,(640,480))
	
	

LimiarBinMax = 10
AreaContornoLimiteMin = 5000

camera = PiCamera() # Objeto para a Pi Camera/ fps = 90 (colocar em constantes depois)

camera.resolution = (600, 240)
#camera.sensor_mode = 7 #resolution = 640x480 e 40<fps<90
camera.framerate = 90
print(camera.resolution)
camera.awb_mode = 'auto'
camera.exposure_mode = 'auto'
rawCapture = PiRGBArray(camera, size=camera.resolution)
time.sleep(0.1)
print("CAMERA PREPARADA\n")
time.sleep(0.5) #Ajusta os ganhos antes de permitir a retirada do primeiro frame		
matriz = calculaMatrizBEV(600, 240,0,0) 

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	start = time.time()
	image = frame.array		
	print("Frame Capturado")
	#cv2.imshow('Imagem Capturada', image)
	
	#image = birdEyeView(image,matriz) #converte para BirdEyeView
	#cv2.imshow('Correcao Bird View', image)
	
	#obtencao das dimensoes da imagem
	height = np.size(image,0)
	width= np.size(image,1)
	QtdeContornos = 0
	DirecaoASerTomada = 0
	
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	#cv2.imshow('Escala de Cinza', gray)
	
	image = cv2.GaussianBlur(gray, (21, 21), 0)
	#cv2.imshow('Filtro Gaussiano', image)
	
	LimiarBinarizacao = 75
	#LimiarBinMax = 125
	
	ret, image = cv2.threshold(image,LimiarBinarizacao,255,cv2.THRESH_BINARY_INV)
	#cv2.imshow('Limiarizacao', image)
	
	#image = cv2.inRange(image, LimiarBinarizacao,LimiarBinMax)
	#cv2.imshow('Limiarizacao - InRange', image)
		
	#image = cv2.dilate(image,None,iterations=2)
	#cv2.imshow('DIlatacao', image)
	
	#image = cv2.bitwise_not(image)
	cv2.imshow('Inversao', image)
	
	#_, cnts, _ = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		
	#for c in cnts:
			#se a area do contorno capturado for pequena, nada acontece
	#	if cv2.contourArea(c) < AreaContornoLimiteMin:
	#		continue						
	#	QtdeContornos = QtdeContornos + 1
			#obtem coordenadas do contorno (na verdade, de um retangulo que consegue abrangir todo ocontorno) e
			#realca o contorno com um retangulo.
	#	(x, y, w, h) = cv2.boundingRect(c)   #x e y: coordenadas do vertice superior esquerdo #w e h: respectivamente largura e altura do retangulo
		#cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)
		#cv2.imshow('image', gray)
	M = cv2.moments(image)
	if M['m00'] > 0:
		CoordenadaXCentroContorno = int(M['m10']/M['m00'])
		CoordenadaYCentroContorno = int(M['m01']/M['m00'])
		print ('Xcenter: ' + str(CoordenadaXCentroContorno))
	else:
		print ('nao foi encontrado')  
	elapsed_time_fl = (time.time() - start)
	fps = 1/elapsed_time_fl
	print('FPS: ' + str(fps))
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		exit(1)

	rawCapture.truncate(0)	


