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
# Python versao: 2
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

class CarHandler():

	# O construtor da classe recebe quais serão os pinos que vão 
	# acionar o GPIO
	def __init__(self, fa, fb, ba, bb, d):
		# Essas variáveis precisam ser globais pq serão usadas 
		# nas outras funções.
		# Estou definindo de forma fixa a pinagem, pois não é 
		# a intenção que isso mude depois
		self.IN1 = 12
		self.IN2 = 16
		# self.direction = d # Not defined yet

		# Configurando o GPIO e definindo os pinos de saída:
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.IN1, GPIO.OUT)
		GPIO.setup(self.IN2, GPIO.OUT)
		#GPIO.setup(self.direction, GPIO.OUT)
		#self.pwm = GPIO.PWM(self.direction, 50)
		#self.pwm.start(0)

	# Vira o servomotor em um ângulo específico
	#def setAngle(self, angle):
#		print "Virando ", angle
#		duty = angle / 18.0 + 2.0
#		GPIO.output(self.direction, GPIO.HIGH)
#		self.pwm.ChangeDutyCycle(duty)

	# Função para mover o carrinho pra frente
	def forward(self):
		print "Andando para frente"
		GPIO.output(self.IN1, GPIO.HIGH)
		GPIO.output(self.IN2, GPIO.LOW)

	# Função para mover o carrinho pra trás
	def backward(self):
		print "Andando para trás"
		GPIO.output(self.IN1, GPIO.LOW)
		GPIO.output(self.IN2, GPIO.HIGH)

	# Função para parar o carrinho
	def stop(self):
		print "Parando o carro"
		GPIO.output(self.IN1, GPIO.HIGH)
		GPIO.output(self.IN2, GPIO.HIGH)

	# Função para colocar o carrinho em ponto-morto
	def neutral(self):
		print "Ponto Morto"
		GPIO.output(self.IN1, GPIO.LOW)
		GPIO.output(self.IN2, GPIO.LOW)
