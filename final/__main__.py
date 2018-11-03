
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

ARQUIVO_CSV = 'dados_'+str(datetime.datetime.now())+'.csv'

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
    
# INSTANCIANDO OBJETOS DAS CLASSES IMAGEHANDLER E CARHANDLER
objImageHandler = ImageHandler() # Objeto para ImageHandler
objCarHandler = CarHandler()
objControlHandler = ControlHandler()

mediaMovelPosicao = MediaMovel(MEDIA_MOVEL_POSICAO_SIZE,MEDIA_MOVEL_VALOR_POSICAO_INICIAL)
#mediaMovelPosicaoY = MediaMovel(MEDIA_MOVEL_POSICAOY_SIZE, MEDIA_MOVEL_VALOR_POSICAOY_INICIAL)
mediaMovelAngulo = MediaMovel(MEDIA_MOVEL_ANGULO_SIZE,MEDIA_MOVEL_VALOR_ANGULO_INICIAL)
#PREPARANDO A CAMERA
#camera = PiCamera() # Objeto para a Pi Camera
#camera.resolution = CAMERA_RESOLUCAO
#camera.framerate = CAMERA_FRAMERATE
#rawCapture = PiRGBArray(camera, size=CAMERA_RESOLUCAO)
#camera.framerate = 90
#print(camera.resolution)
time.sleep(0.1)

#abre arquivo(sobrescreve o último arquivo criado com mesmo nome)
csvfile = open(DATA_PATH + ARQUIVO_CSV,'w')
writeRow(csvfile,'x_media','x','y','referencia','ang_control','angulo')#cabeçalho

#objCarHandler.rotinaDeTestes()

vs = PiVideoStream(CAMERA_RESOLUCAO,CAMERA_FRAMERATE)
vs.start()#roda PiVideoStream em uma thread
time.sleep(2)#espera para que evitar erro da primeira imagem do VideoStream vir vazia
#vs.camera.sensor_mode = CAMERA_MODE
#Constantes
x_target = ROI_WIDTH//2
pi = pigpio.pi()

#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#outOriginal = cv2.VideoWriter(DATA_PATH + ARQUIVO_VIDEO,fourcc, 20.0, (ROI_WIDTH,ROI_HEIGTH,))
#outPreProc = cv2.VideoWriter(DATA_PATH + 'binarizado.avi',fourcc, 20.0, (ROI_WIDTH,ROI_HEIGTH,),0)
print("Aguardo liberacao")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(22, GPIO.IN)
#GPIO.wait_for_edge(22, GPIO.RISING)
stayOnMain = False#mude para falso para esperar apertar botão
def invert_stayOnMain(x):
	
	global stayOnMain
	stayOnMain = not stayOnMain
	
GPIO.add_event_detect(22, GPIO.RISING, callback=invert_stayOnMain, bouncetime=300)



while not stayOnMain:
	continue
	



#def stop_program(x):
#	print("Saindo")
#	stop_race = True
	
#GPIO.add_event_detect(22, GPIO.FALLING, callback=stop_program, bouncetime=300)
#GPIO.wait_for_edge(22,GPIO.RISING)
#PEGANDO FRAME POR FRAME PARA TRATAR E TOMAR UMA DECISAO
#for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
#time.sleep(0.5)

#GPIO.remove_event_detect(22)


#GPIO.add_event_detect(22, GPIO.RISING, callback=invert_stayOnMain, bouncetime=300)


objCarHandler.forward()

#===========================
#last_time = time.time()
#mean_h = 0                
#THETA_MAX = 120
#THETA_MIN = 60
#theta_init = (THETA_MAX + THETA_MIN) / 2
#error, error_d, error_i = 0, 0, 0
#last_error = 0
#Kp_turn = 20
#Kp_line = 10
#Kd = 0
#Ki = 0
#===========================


while(True):
		
	try:
		start = time.time()
		image = vs.read()#lê frame da VideoStream
		
		image = image[ROI_Y1:ROI_Y2,ROI_X1:ROI_X2]#pega região de interesse
		#outOriginal.write(image)#salva frame em vídeo
		
		#tempoStartPreProc = time.time()
		image = objImageHandler.preProcessamento(image)
		#print('Pre-proc: ' + str(time.time() - tempoStartPreProc))
#		outPreProc.write(image)
		
		x_contorno, y_contorno, qtdeContornos = objImageHandler.deteccaoDeCurvas(image)	
		x_contorno_original = x_contorno
		x_contorno = mediaMovelPosicao.update(x_contorno)
		print('x contorno: '+ str(x_contorno))
		#angle = objControlHandler.Controle(x_contorno, x_target)
		
		#Novo calculo
		#try:
	#		angle = np.degrees(np.arctan((ROI_HEIGTH)/(x_contorno-x_target)))
	#		print('angle c: '+ str(angle))
	#	except:
	#		angle = 90.0	
	#	if (x_contorno<=x_target):
	#		angle = abs(angle)
	#	else:
	#		angle = 180.0 - angle
		
		#angle = (2.0/3.0)*angle + 60

		#angle = objImageHandler.tratarImagem(image)
		
		
		
		#x_contorno, y_contorno, QtdeLinhas = objImageHandler.tratarImagem(image)
		#x_original = x_contorno #armazena antes de pegar média móvel para comparação
		#atualiza posição por média móvel
		#x_contorno = mediaMovelPosicao.update(x_contorno)
		#angle = 180.0-(np.arctan((-y_contorno) / x_contorno))
		
		
		#===========================
#		max_error_px=x_target
#		error = (x_target - x_contorno) / max_error_px
#		error = (90 - angle)/90 #alteramos aqui
#		h = np.clip(error, 0,1)
#		t = h
#		mean_h += (h - mean_h)
#		h = mean_h
#		Kp = h*Kp_turn + (1-h)*Kp_line
#		error_d = error - last_error
#		last_error = error                
		#PID control
#		dt = time.time()-last_time
#		u_angle = Kp*error + Kd*(error_d/dt) + Ki*(error_i*dt)
#		error_i += error
#		last_time = time.time()
#		angle = (theta_init - u_angle)
		u_angle=0
		#===========================
		
		
		#método por interpolação de 3 centróides
		
		#const = 0.9
		if(0<=x_contorno<=30):
			angle = 70
		elif x_contorno<=70:
			angle = 75
		elif x_contorno<=110:
			angle = 80
		elif x_contorno<=150:
			angle=85
		elif x_contorno<=170:
			angle=90
		elif x_contorno<=210:
			angle = 95
		elif x_contorno<=250:
			angle = 100
		elif x_contorno<=290:
			angle=105
		else:
			angle = 110
		
		#angle = objImageHandler.tratarImagem(image)
		objCarHandler.Direcao(angle,pi)#enviando ângulo detectado por imageHandler diretamente
		
		writeRow(csvfile,x_contorno,x_contorno_original,y_contorno,x_target, u_angle,angle)
		elapsed_time_fl = (time.time() - start)
		fps = 1/elapsed_time_fl
		print('FPS: ' + str(fps))
		
		#if not stayOnMain:
		#	break
		
		#rawCapture.truncate(0)	
	except(KeyboardInterrupt):
		csvfile.close()#fecha arquivo ao sair do loop
		objCarHandler.Direcao(90,pi) #retorna rodas
		objCarHandler.stop()
		objCarHandler.cleanupPins()
		vs.stop()#pára execução da thread
		#objImageHandler.salvaImagemAtual()
		#objImageHandler.salvaDadosAtuais()
		exit(1)
# Libera os pinos

csvfile.close()#fecha arquivo ao sair do loop
objCarHandler.Direcao(90, pi) #retorna rodas
objCarHandler.stop()
objCarHandler.cleanupPins()
vs.stop()#pára execução da thread
#objImageHandler.salvaImagemAtual()
#objImageHandler.salvaDadosAtuais()
objCarHandler.cleanupPins()
