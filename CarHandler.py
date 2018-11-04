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
# DESCRICAO: CarHandler.py 
# Python versao: 3
#
# Classe que inicia e manipula o GPIO do Rapsberry.
# Aqui é possível mover o carrinho para frente, para trás e 
# ajustar o ângulo das rodas da frente.
# 
# A seguinte tabela, referente ao driver LM298, foi usada para
# definir os níveis de saídas:
#
#	Motor			IN1		IN2
#	Horário 		5v		GND
#	Anti-horário 	GND 	5v
#	Ponto-morto 	GND 	GND
#	Freio 			5v 		5v
# =============================================================

import sys
import time
import RPi.GPIO as GPIO
import pigpio 

class CarHandler():
	# O construtor da classe recebe quais serão os pinos que vão 
	# acionar o GPIO
	def __init__(self):
		# Essas variáveis precisam ser globais pq serão usadas 
		# nas outras funções.
		# Estou definindo de forma fixa a pinagem, pois não é 
		# a intenção que isso mude depois
		# Pino de controle da ponte HH:
		self.IN1 = 16 # GPIO23
		self.IN2 = 18 # GPIO22		
		self.dir = 13
		self.angle_max = 110
		self.angle_min = 70
		# Configurando o GPIO e definindo os pinos de saída:
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.IN1, GPIO.OUT)
		GPIO.setup(self.IN2, GPIO.OUT)
		GPIO.output(self.IN1, GPIO.LOW)
		GPIO.output(self.IN2, GPIO.LOW)
		

	# Vira o servomotor em um ângulo específico dado em graus
	def setAngle(self, angle):
		print("Virando", angle)
		duty = angle / 18.0 + 2.0
		GPIO.output(self.dir, GPIO.HIGH)
		self.pwm.ChangeDutyCycle(duty)
		#self.hpi.hardware_PWM(self.dir, 60, 90*10000)

	# Função para mover o carrinho pra frente
	def forward(self):
		print("Andando para frente")
		GPIO.output(self.IN1, GPIO.HIGH)
		GPIO.output(self.IN2, GPIO.LOW)

	# Função para mover o carrinho pra trás
	def backward(self):
		print("Andando para trás")
		GPIO.output(self.IN1, GPIO.LOW)
		GPIO.output(self.IN2, GPIO.HIGH)

	# Função para parar o carrinho
	def stop(self):
		print("Parando o carro")
		GPIO.output(self.IN1, GPIO.HIGH)
		GPIO.output(self.IN2, GPIO.HIGH)

	# Função para colocar o carrinho em ponto-morto
	def neutral(self):
		print("Ponto Morto")
		GPIO.output(self.IN1, GPIO.LOW)
		GPIO.output(self.IN2, GPIO.LOW)

	def cleanupPins(self):
		GPIO.cleanup()

	def rotinaDeTestes(self):
		print("Executando rotina de teste dos motores.")

		self.setAngle(90)
		time.sleep(10) # Espera 10 segundos antes de sair andando para dar tempo de eu sair lá fora
		self.forward()
		time.sleep(2)
		self.setAngle(60)
		time.sleep(2)
		self.setAngle(90)
		time.sleep(2)
		self.setAngle(115)
		time.sleep(2)
		self.setAngle(90)
		time.sleep(2)
		self.stop()
		time.sleep(2)
		self.backward()
		time.sleep(2)
		self.neutral()
		
		print("Fom da rotina de teste dos motores.")
		time.sleep(0.5)
		
	def Direcao(self, angle, pi):
		
		pi.hardware_PWM(13, 50, 0)
		#print(pi.get_PWM_frequency(13))
		if (angle <= self.angle_min):
			angle = self.angle_min
		elif (angle >= self.angle_max):
			angle = self.angle_max
		print('angle_final = ' + str(angle))
		self.comPWM = int((angle / 18.0 + 2.0)*10000)
		#print (self.comPWM/10000)
		pi.hardware_PWM(13,50,self.comPWM)
		
