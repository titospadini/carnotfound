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
# =============================================================

import sys
import time
import RPi.GPIO as GPIO

class CarHandler():

	#o construtor da classe recebe quais serão os pinos que vão acionar o GPIO
	def __init__(self, fa, fb, ba, bb, d):
		#essas variáveis precisam ser globais pq serão usadas nas outras funções
		self.forwardA = fa
		self.forwardB = fb
		self.backwardA = ba
		self.backwardB = bb
		self.direction = d
		#configurando o GPIO e definindo os pinos de saída
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.forwardA, GPIO.OUT)
		GPIO.setup(self.backwardA, GPIO.OUT)
		GPIO.setup(self.forwardB, GPIO.OUT)
		GPIO.setup(self.backwardB, GPIO.OUT)
		GPIO.setup(self.direction, GPIO.OUT)
		self.pwm = GPIO.PWM(self.direction, 50)
		self.pwm.start(0)

	#função para virar as rodas da frente do carrinho
	def setAngle(self, angle):
		print "Virando ", angle
		duty = angle / 18.0 + 2.0
		GPIO.output(self.direction, GPIO.HIGH)
		self.pwm.ChangeDutyCycle(duty)

	#função para mover o carrinho pra frente
	def forward(self):
		print "Andando para frente"
		GPIO.output(self.forwardA, GPIO.HIGH)
		GPIO.output(self.forwardB, GPIO.HIGH)

	#função para mover o carrinho pra trás
	def backward(self):
		print "Andando para trás"
		GPIO.output(self.backwardA, GPIO.HIGH)
		GPIO.output(self.backwardB, GPIO.HIGH)

	#função para parar o carrinho
	def stop(self):
		print "Parando o carro"
		GPIO.output(self.forwardA, GPIO.LOW)
		GPIO.output(self.forwardB, GPIO.LOW)
		GPIO.output(self.backwardA, GPIO.LOW)
		GPIO.output(self.backwardB, GPIO.LOW)
		GPIO.output(self.direction, GPIO.LOW)
		
