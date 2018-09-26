import cv2
import numpy as np
import RPi.GPIO as GPIO
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

LimiarBinarizacao = 125       #este valor eh empirico. Ajuste-o conforme sua necessidade 
AreaContornoLimiteMin = 5000  #este valor eh empirico. Ajuste-o conforme sua necessidade 

#Funcao: trata imagem e retorna se o robo seguidor de linha deve ir para a esqueda ou direita
#Parametros: frame capturado da webcam e primeiro frame capturado
#Retorno: < 0: robo deve ir para a direita
#         > 0: robo deve ir para a esquerda
#         0:   nada deve ser feito
def TrataImagem(img):
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

#Programa principal

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
print("camera\n")

camera.resolution = (640, 480)
print("resolution\n")

camera.framerate = 32
print("framerate\n")

rawCapture = PiRGBArray(camera, size=(640, 480))
print("rawCapture\n")
 
# allow the camera to warmup
time.sleep(0.1)
print("sleep\n")
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	print("capture_continuous\n")
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
	print("image\n")

	# clear the stream in preparation for the next frame	
	print("truncate\n")
 
	# if the `q` key was pressed, break from the loop
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

	try:
		# (grabbed, image) = camera.read()
		Direcao,QtdeLinhas = TrataImagem(image)

		if (QtdeLinhas == 0):
			print("Nenhuma linha encontrada. O robo ira parar.")
			# GPIO.output(GPIOMotor1, GPIO.LOW)
			# GPIO.output(GPIOMotor2, GPIO.LOW) 
			continue
	
		if (Direcao > 0):
			print("Distancia da linha de referencia: "+str(abs(Direcao))+" pixels a direita")
			# GPIO.output(GPIOMotor1, GPIO.HIGH)
			# GPIO.output(GPIOMotor2, GPIO.LOW)
		if (Direcao < 0):
			print("Distancia da linha de referencia: "+str(abs(Direcao))+" pixels a esquerda")
			# GPIO.output(GPIOMotor1, GPIO.LOW)
			# GPIO.output(GPIOMotor2, GPIO.HIGH)
		if (Direcao == 0):
			print("Exatamente na linha de referencia!")
			# GPIO.output(GPIOMotor1, GPIO.HIGH)
			# GPIO.output(GPIOMotor2, GPIO.HIGH)
	except (KeyboardInterrupt):
		exit(1)   

	rawCapture.truncate(0)
