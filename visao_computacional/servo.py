# =============================================================
#
#                       -- ROBOCAR --
# 
# TIME: CarNotFound
# CARRO: 404
#  
# =============================================================
#
# DESCRICAO: servo.py 
# Python versao: 3.6.6
#
# Controla o servo motor via GPIO
# 
# =============================================================

# Pacotes para gerir os pinos GPIO e habilitar o Sleep
import RPi.GPIO as GPIO
from time import sleep

# Configura a porta GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
pwm=GPIO.PWM(3, 50)
pwm.start(0)

# Função que "posiciona" o servo segundo o ângulo fornecido
def SetAngle(angle):
        duty = angle / 18 + 2
        GPIO.output(3, True)
        pwm.ChangeDutyCycle(duty)
        sleep(1)
        GPIO.output(3, False)
        pwm.ChangeDutyCycle(0)

# Loop de teste para girar o servo de 0 a 180 graus 3 vezes
print('inicio')
for i in range(3):
        print('0 graus')
        SetAngle(0)
        print('180 graus')
        SetAngle(180)

# Retorno ao centro de alinhamento do servo
print('retornando ao centro...')
SetAngle(90)

# Fim do processo
print('fim')
pwm.stop()
GPIO.cleanup()
