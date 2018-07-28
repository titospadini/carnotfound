import sys
import time
import RPi.GPIO as GPIO

GPIO.cleanup()

GPIO.setmode(GPIO.BOARD)



mode = GPIO.getmode()
print(" mode ="+str(mode))

ForwardA = 8
ForwardB = 16
BackwardA = 10
BackwardB = 18
Direction = 12
sleeptime = 1

#GPIO.setmode(GPIO.BOARD)
GPIO.setup(ForwardA, GPIO.OUT)
GPIO.setup(BackwardA, GPIO.OUT)
GPIO.setup(ForwardB, GPIO.OUT)
GPIO.setup(BackwardB, GPIO.OUT)
GPIO.setup(Direction, GPIO.OUT)

pwm = GPIO.PWM(Direction, 50)
pwm.start(0)

def setAngle(angle):
	duty = angle / 18.0 + 2.0
	GPIO.output(Direction, GPIO.HIGH)
	pwm.ChangeDutyCycle(duty)
	time.sleep(1)
	GPIO.output(Direction, GPIO.LOW)
	pwm.ChangeDutyCycle(0)

def forward(x):
	GPIO.output(ForwardA, GPIO.HIGH)
	GPIO.output(ForwardB, GPIO.HIGH)
	print("Moving Forward")
	time.sleep(x)
	GPIO.output(ForwardA, GPIO.LOW)
	GPIO.output(ForwardB, GPIO.LOW)

def backward(x):
	GPIO.output(BackwardA, GPIO.HIGH)
	GPIO.output(BackwardB, GPIO.HIGH)
	print("Moving Backward")
	time.sleep(x)
	GPIO.output(BackwardA, GPIO.LOW)
	GPIO.output(BackwardB, GPIO.LOW)

setAngle(90)
time.sleep(2)
while(1):
	print("<<< Iniciando !!!!!!!!! >>>")	
	forward(3)
	backward(3)
	setAngle(80)
	time.sleep(2)
	setAngle(100)
	time.sleep(2)
	setAngle(90)
	time.sleep(2)
	print("<<< Iniciando a limpeza !!!!!!!!! >>>")
GPIO.cleanup()
