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
GPIO.setup(03, GPIO.OUT)
pwm=GPIO.PWM(03, 50)
pwm.start(0)

# Função que "posiciona" o servo segundo o ângulo fornecido
def SetAngle(angle):
        duty = angle / 18 + 2
        GPIO.output(03, True)
        pwm.ChangeDutyCycle(duty)
        sleep(1)
        GPIO.output(03, False)
        pwm.ChangeDutyCycle(0)

# Loop de teste para girar o servo de 0 a 180 graus 3 vezes
for i in range(3):
        SetAngle(0)
        SetAngle(180)

# Fim do processo
pwm.stop()
GPIO.cleanup()