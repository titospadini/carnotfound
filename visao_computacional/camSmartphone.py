from urllib import request
import cv2
import numpy as np
import time

# Substitua pela URL obtida pelo aplicativo IP Webcam (Android), 
# com IP:porta e mantendo o '/shot.jpg' ao final.
url='http://192.168.1.30:8080/shot.jpg'

while True:
    # Obtém a imagem a partir da câmera IP
    imgResp = request.urlopen(url)
    
    # Converte a imagem para um array de números 
    # inteiros de 0 a 255.
    imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
    
    # Converte o array da imagem para um formato
    # mais comumente usado pelo OpenCV
    img = cv2.imdecode(imgNp,-1)
	
	# Exibe a imagem capturada
    cv2.imshow('IPWebcam',img)

    #Utilize isto para dar um "descanso" ao processador
    #time.sleep(0.1) 

    # Encerra o programa se precionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break