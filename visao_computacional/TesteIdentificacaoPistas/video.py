#-*- coding: utf-8 -*-
# =============================================================
#
#                       -- ROBOCAR --
# 
# TIME: CarNotFound
# CARRO: 404
#  
# =============================================================
import cv2;
import numpy as np;


def pintarPista(imagem):
	#cortando a imagem pela metade(estabelecendo um limite superior)
	height, width = imagem.shape[:2]
	imagem = imagem[int(0.25*height):height, 0:width]

	#binarizando a imagem com thresh manual
	thresh = 50
	th, imagem = cv2.threshold(imagem, thresh, 255, cv2.THRESH_BINARY)

	#binarizando a imagem com thresh automatico
	# thresh, imagem  = cv2.threshold(imagem,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	# print thresh

	#invertendo a binarização para que seja possível "pintar" a pista
	#imagem = np.invert(imagem)
	 
	#para continuar o código, é necessário trabalhar com duas imagens. Aqui estou fazendo uma cópia
	copia = imagem.copy()
	 
	#pegando novamente a altura e largura e criando uma nova imagem com zeros
	height, width = copia.shape[:2]
	mask = np.zeros((height+2, width+2), np.uint8)

	#definindo os pontos sementes de onde começará a pintura
	pontoAx = int(width/2 * 0.7)
	pontoAy = int(height * 0.85)
	pontoBx = int(width/2 * 1.3)
	pontoBy = int(height * 0.85)

	#pintando a cópia
	cv2.floodFill(copia, mask, (pontoAx, pontoAy), 255)
	cv2.floodFill(copia, mask, (pontoBx, pontoBy), 255)
	 
	#combinando a cópia com a imagem normal para gerar o resultado esperado
	imagem = imagem | copia

	#retornando 
	return imagem


#captura de vídeo
cap = cv2.VideoCapture('nissan.mp4')
cap.set(cv2.CAP_PROP_FPS,60)
while(1):
   ret, frame = cap.read()

   #converte video para gray scale
   gray_vid = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

   imagem = pintarPista(gray_vid)

   #exibe os frames
   cv2.imshow('Original',frame)
   cv2.imshow("Resultado", imagem)

   if cv2.waitKey(1) & 0xFF == ord('q'):
       break

cap.release()
cv2.destroyAllWindows()