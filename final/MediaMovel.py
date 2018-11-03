#encoding:utf-8
from statistics import mean
from collections import deque

class MediaMovel:
	def __init__(self,size,default):
		self.valueDeque = deque([default]*size,size)
		
	def update(self, newValue):
		self.valueDeque.popleft()#retira valor mais à esquerda
		self.valueDeque.append(newValue)#adiciona valor novo à direita
		return mean(self.valueDeque)#retorna média dos valores

