
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
#writeRow(csvfile,'y_c', 'x_c', 'beta', 'alfa','erro','Sinal Controle','FPS')#cabeçalho
 
 
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


while(True):		
	try:
		start = time.time()
		image = vs.read()#lê frame da VideoStream		
		
		
		#PARA SALVAR O VIDEO ORIGINAL
		#outOriginal.write(image)#salva frame em vídeo
		
		#PRE PROCESSAMENTO
		image = objImageHandler.preProcessamento(image)		

		#PARA SALVAR O VIDEO BINARIZADO
		#outPreProc.write(image)
		
		#DETECTA CONTORNO
		x_contorno, y_contorno= objImageHandler.deteccaoDeCurvas(image)	
		
		#MEDIA MOVEL DE X
		#x_contorno = mediaMovelPosicao.update(x_contorno)
		#print('x contorno: '+ str(x_contorno))
		
		#UTILIZA A LINEARIZACAO DA CLASSE CONTROLE
		erro, beta, alfa, sinal_controle = objControlHandler.Controle(x_contorno)
		
		#ENVIA ANGULO AO MOTOR
		objCarHandler.Direcao(sinal_controle,pi)#enviando ângulo detectado por imageHandler diretamente
	
		
		
		#ESCREVE DADOS
		#writeRow(csvfile,y_contorno,x_contorno,beta,alfa,erro,sinal_controle)

		#COMPUTA TEMPO DE PROCESSAMENTO
		elapsed_time_fl = (time.time() - start)
		print('y_c:  ' + str(y_contorno))
		print('x_c:  ' + str(x_contorno))
		print('beta: ' + str(beta))
		print('alfa: ' + str(alfa))
		print('erro: ' + str(erro))
		print('Controle: '+str(sinal_controle))
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
#csvfile.close()#fecha arquivo ao sair do loop
objCarHandler.Direcao(90, pi) #retorna rodas
objCarHandler.stop()
objCarHandler.cleanupPins()
vs.stop()#pára execução da thread
objCarHandler.cleanupPins()
