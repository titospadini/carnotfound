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
	def __init__(self):
		# Essas variáveis precisam ser globais pq serão usadas 
		# nas outras funções.
		# Estou definindo de forma fixa a pinagem, pois não é 
		# a intenção que isso mude depois
		# Pino de controle da ponte HH:
		self.IN1 = 12 
		self.IN2 = 16

		# Pino para PWM do servomotor de direção:
		self.dir = 8

		# Configurando o GPIO e definindo os pinos de saída:
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.IN1, GPIO.OUT)
		GPIO.setup(self.IN2, GPIO.OUT)
		GPIO.setup(self.dir, GPIO.OUT)
		self.pwm = GPIO.PWM(self.dir, 50)
		self.pwm.start(0)

	# Vira o servomotor em um ângulo específico dado em graus
	def setAngle(self, angle):
		print("Virando", angle)
		duty = angle / 18.0 + 2.0
		GPIO.output(self.dir, GPIO.HIGH)
		self.pwm.ChangeDutyCycle(duty)

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