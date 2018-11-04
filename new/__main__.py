
#encoding: utf-8
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
# Python versao: 3.5
#
# Arquivo principal que vai instânciar os objetos das classes 
# CarHandler e ImageHandler para mover o carrinho de acordo 
# com as imagens obtidas pela webcam
#
# =============================================================

    
import time
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
from CarHandler import CarHandler
from ImageHandler import ImageHandler as ImageHandler
from ControlHandler import ControlHandler
from constants import *
import pigpio 
import numpy as np
from imutils.video.pivideostream import PiVideoStream
from MediaMovel import MediaMovel
import RPi.GPIO as GPIO
import datetime

def writeRow(csvfile,*args):
    """Escreve uma linha no arquivo csv, separado por vírgula"""
    row = ''
    for arg in args[:-1]:
        #para cada valor menos o último, adiciona vírgula
        row += str(arg) + ','
    #para o último valor, adiciona quebra de linha
    row += str(args[len(args)-1]) + '\n'

    #escreve no arquivo
    csvfile.write(row)

def invert_stayOnMain(x):	
	global stayOnMain
	stayOnMain = not stayOnMain

# INSTANCIANDO OBJETOS DAS CLASSES IMAGEHANDLER E CARHANDLER
objImageHandler = ImageHandler() # Objeto para ImageHandler
objCarHandler = CarHandler()
objControlHandler = ControlHandler()
pi = pigpio.pi()

# LOG DE DADOS
#ARQUIVO_CSV = 'dados_'+str(datetime.datetime.now())+'.csv'
#csvfile = open(DATA_PATH + ARQUIVO_CSV,'w')
#writeRow(csvfile,'x_media','x','y','referencia','ang_control','angulo')#cabeçalho
 
#MEDIA MOVEL
mediaMovelPosicao = MediaMovel(MEDIA_MOVEL_POSICAO_SIZE,MEDIA_MOVEL_VALOR_POSICAO_INICIAL)
mediaMovelAngulo = MediaMovel(MEDIA_MOVEL_ANGULO_SIZE,MEDIA_MOVEL_VALOR_ANGULO_INICIAL)

#OTIMIZACAO
vs = PiVideoStream(CAMERA_RESOLUCAO,CAMERA_FRAMERATE)
vs.start()#roda PiVideoStream em uma thread
time.sleep(1)#espera para que evitar erro da primeira imagem do VideoStream vir vazia

#GRAVACAO DE VIDEO
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#outOriginal = cv2.VideoWriter(DATA_PATH + ARQUIVO_VIDEO,fourcc, 20.0, (ROI_WIDTH,ROI_HEIGTH,))
#outPreProc = cv2.VideoWriter(DATA_PATH + 'binarizado.avi',fourcc, 20.0, (ROI_WIDTH,ROI_HEIGTH,),0)

#CHAVE DE ACESSO 
print("Aguardando liberacao")
GPIO.setmode(GPIO.BOARD)
GPIO.setup(22, GPIO.IN)
stayOnMain = False#mude para falso para esperar apertar botão	
GPIO.add_event_detect(22, GPIO.RISING, callback=invert_stayOnMain, bouncetime=300)
while not stayOnMain:
	continue
	
#INICIA MOVIMENTO
objCarHandler.forward()           
theta_init = (THETA_MAX + THETA_MIN) / 2
error, error_d, error_i = 0, 0, 0
last_error = 0


#CONTAGEM DE TEMPO
last_time = time.time()

#INICIA PARAMETROS de CENTROIDE
x_ROI1, y_ROI1 = (ROI_WIDTH/2.0, (ROI_HEIGTH/8.0)*3.0)
x_ROI2, y_ROI2 = (ROI_WIDTH/2.0, (ROI_HEIGTH/8.0)*5.0)
x_ROI3, y_ROI3 = (ROI_WIDTH/2.0, (ROI_HEIGTH/8.0)*7.0)

x_ROI1_a, y_ROI1_a = (ROI_WIDTH/2.0, (ROI_HEIGTH/8.0)*3.0)
x_ROI2_a, y_ROI2_a = (ROI_WIDTH/2.0, (ROI_HEIGTH/8.0)*5.0)
x_ROI3_a, y_ROI3_a = (ROI_WIDTH/2.0, (ROI_HEIGTH/8.0)*7.0)


while(True):		
	try:
		start = time.time()
		image = vs.read()#lê frame da VideoStream		
		image = image[ROI_Y1:ROI_Y2,ROI_X1:ROI_X2]#pega região de interesse
		
		#PARA SALVAR O VIDEO ORIGINAL
		#outOriginal.write(image)#salva frame em vídeo
		
		#PRE PROCESSAMENTO
		image = objImageHandler.preProcessamento(image)		

		#PARA SALVAR O VIDEO BINARIZADO
		#outPreProc.write(image)
		
		#CORTA ROIS
		roiUP, roiMID, roiDOWN = objImageHandler.criaRois(image)

		#DETECTA CENTROIDES
		x_ROI1, y_ROI1, qt_ROI1 = objImageHandler.deteccaoDeCentroide(roiUP)
		x_ROI2, y_ROI2, qt_ROI2 = objImageHandler.deteccaoDeCentroide(roiMID)
		x_ROI3, y_ROI3, qt_ROI3 = objImageHandler.deteccaoDeCentroide(roiDOWN)	
		
		#GARANTE QUE SEMPRE TEREMOS 3 VALORES DE CENTROIDE
		if qt_ROI1==0:
			x_ROI1, y_ROI1 = x_ROI1_a, y_ROI1_a
		if qt_ROI2==0:
			x_ROI2, y_ROI2 = x_ROI2_a, y_ROI2_a
		if qt_ROI3==0:
			x_ROI3, y_ROI3 = x_ROI3_a, y_ROI3_a
		
		#ARMAZENA CENTROIDE ANTERIOR
		x_ROI1_a, y_ROI1_a = x_ROI1, y_ROI1
		x_ROI2_a, y_ROI2_a = x_ROI2, y_ROI2
		x_ROI3_a, y_ROI3_a = x_ROI3, y_ROI3

		#COMPUTA ARRAYS
		xi = np.array([x_ROI1, x_ROI2, x_ROI3])
		yi = np.array([y_ROI1, y_ROI2, y_ROI3])

		#LINEARIZACAO DOS CENTOIDES a1*x + a2
		coef = objControlHandler.Linearizacao(xi, yi)
		a2 = coef[0]
		a1 = coef[1]
		angle = int(180.0 - np.degrees(np.arctan(a1)))
		print('angle ' + str(angle))

		#ENVIA ANGULO AO MOTOR
		objCarHandler.Direcao(angle,pi)#enviando ângulo detectado por imageHandler diretamente
	
		#ESCREVE DADOS
		#writeRow(csvfile,x_contorno,x_contorno_original,y_contorno,x_target,angle,angle)

		#COMPUTA TEMPO DE PROCESSAMENTO
		elapsed_time_fl = (time.time() - start)

		#CALCULO DE FPS
		fps = 1/elapsed_time_fl
		print('FPS: ' + str(fps))
		
	#SAIDA DO LOOP	
	except(KeyboardInterrupt):
		csvfile.close()#fecha arquivo ao sair do loop
		objCarHandler.Direcao(90,pi) #retorna rodas
		objCarHandler.stop()
		objCarHandler.cleanupPins()
		vs.stop()#pára execução da thread
		exit(1)

#ENCERRA TUDO
csvfile.close()#fecha arquivo ao sair do loop
objCarHandler.Direcao(90, pi) #retorna rodas
objCarHandler.stop()
objCarHandler.cleanupPins()
vs.stop()#pára execução da thread
objCarHandler.cleanupPins()
