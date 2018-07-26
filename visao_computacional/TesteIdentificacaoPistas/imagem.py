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

#Lendo a imagem em tons de cinza
imagem = cv2.imread("e.jpg", cv2.IMREAD_GRAYSCALE)
cv2.imshow("Imagem Cinza", imagem)

#cortando a imagem pela metade(estabelecendo um limite superior)
height, width = imagem.shape
imagem = imagem[int(0.50*height):height, 0:width]
cv2.imshow("Imagem Cortada", imagem)

#binarizando a imagem com thresh manual
thresh = 240
th, imagem = cv2.threshold(imagem, thresh, 255, cv2.THRESH_BINARY)

#binarizando a imagem com thresh automatico
# thresh, imagem  = cv2.threshold(imagem,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# print thresh
cv2.imshow("Imagem Binarizada", imagem)

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

#mostrando o resultado
cv2.imshow("Resultado", imagem)
cv2.waitKey(0)