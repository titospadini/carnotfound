# encoding: utf-8
import numpy as np
import cv2 as cv
from util import *

"""
Código para calibração do detector de linhas da pista por blob detector.

Ao executar, mova as janelas porque elas começam em cima uma das outras

O blob detector separa regiões de pixels por algumas propriedades, esclohendo valores de mínimo e máximo para estas. Foram usados área e inércia.

A inércia se refere ao quão alongado um objeto é. Valores baixos são objetos mais alongados e os altos são objetos mais arredondados. Com isso já dá para separar um pouco o que é uma faixa e o que é brilho do sol
"""


numeroDeSets = 3
numeroDeImagens = 21



#cria janela para parâmetros
wnd = 'Parametros'
cv.namedWindow(wnd)

#cria um slider para cada parâmetro
indexSetBar = 'Set escolhido'
cv.createTrackbar(indexSetBar, wnd,0,numeroDeSets-1,nothing)

indexFotoBar = 'Foto escolhida'
cv.createTrackbar(indexFotoBar, wnd,2,numeroDeImagens-1,nothing)

thValueBar = 'valor Threshold'
cv.createTrackbar(thValueBar, wnd,199,255,nothing)

blurKernelBar = 'tamanho do kernel para blur(2k-1)'
cv.createTrackbar(blurKernelBar, wnd,0,10,nothing)

openingKernelBar = 'tamanho do kernel para opening(2k-1)'
cv.createTrackbar(openingKernelBar, wnd,0,10,nothing)

faixaMinAreaBar = 'Area minima'
cv.createTrackbar(faixaMinAreaBar, wnd,56,10000,nothing)

faixaMaxAreaBar = 'Area maxima'
cv.createTrackbar(faixaMaxAreaBar, wnd,1771,10000,nothing)

faixaMinInertiaBar = 'Inercia minima(%)'
cv.createTrackbar(faixaMinInertiaBar, wnd,0,100,nothing)

faixaMaxInertiaBar = 'Inercia maxima(%)'
cv.createTrackbar(faixaMaxInertiaBar, wnd,23,100,nothing)

rectMinBar = 'Area minima do retangulo'
cv.createTrackbar(rectMinBar, wnd,80,5000,nothing)

rectMaxBar = 'Area maxima do retangulo'
cv.createTrackbar(rectMaxBar, wnd,2000,5000,nothing)


#nomes das janelas
#originalWnd = 'Original'
predetectWnd = 'Binarizada'
blobWnd = 'Blob Detector'
#harrisWnd = 'Harris Detection'
imgLimpaWnd = 'Imagem limpa'
retanguloWnd = 'Retangulos'

#cria e muda tamanho das janelas
dimensoes = (400,300)
#criaERedimensionaJanelas(originalWnd,dimensoes)
criaERedimensionaJanelas(predetectWnd,dimensoes)
criaERedimensionaJanelas(blobWnd,dimensoes)
#criaERedimensionaJanelas(harrisWnd,dimensoes)
criaERedimensionaJanelas(retanguloWnd,dimensoes)
criaERedimensionaJanelas(imgLimpaWnd,dimensoes)

while(True):

    #lê parâmetros dos sliders
    indexSet = cv.getTrackbarPos(indexSetBar, wnd)
    indexFoto = cv.getTrackbarPos(indexFotoBar, wnd)
    thValue = cv.getTrackbarPos(thValueBar, wnd)
    blurKernelSize = 2*cv.getTrackbarPos(blurKernelBar, wnd) - 1
    openingKernelSize = 2*cv.getTrackbarPos(openingKernelBar, wnd) - 1
        
    faixaMinPixels = cv.getTrackbarPos(faixaMinAreaBar, wnd)
    faixaMaxPixels = cv.getTrackbarPos(faixaMaxAreaBar, wnd)
    faixaMinInertia = 1.0*cv.getTrackbarPos(faixaMinInertiaBar, wnd)/100
    faixaMaxInertia = 1.0*cv.getTrackbarPos(faixaMaxInertiaBar, wnd)/100

    rectMin = cv.getTrackbarPos(rectMinBar, wnd)
    rectMax = cv.getTrackbarPos(rectMaxBar, wnd)
    
    image = cv.imread('./images%i'%(indexSet)+ '/imagem%i'%(indexFoto) + '.jpg')#lê imagem

    #caso se tenha menos imagens que numeroDeImagens, é possível pedir que se leia uma imagem que não existe. Caso isso ocorra, o programa gera um erro e pára ao tentar se converter para escala de cinza, então o tratamento de exceção abaixo cria uma imagem cinza vazia para evitar que o programa trave
    try:
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)#converte para escala de cinza
    except:
        y,x = dimensoes
        #por algum motivo, tentar criar uma imagem em escala de cinza direto está dando erro, então estou criando uma colorida e convertendo
        image = np.zeros((x,y,3),np.uint8)
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        
    bl = blur(gray,blurKernelSize)
    
    ope = opening(bl,openingKernelSize)
    
    histImg = cv.equalizeHist(ope)

    _, thresh = cv.threshold(histImg,thValue,255,cv.THRESH_BINARY)
    
    #cria parâmetros do blob detector
    parametrosBlobDtector = filtragemBlobParametros(faixaMinPixels,faixaMaxPixels,faixaMinInertia,faixaMaxInertia)
    
    #cria detector com os parâmetros escolhidos
    detector = cv.SimpleBlobDetector_create(parametrosBlobDtector)
    
    #blob detector detecta regiões escuras então imagem binarizada é invertida
    notThresh = cv.bitwise_not(thresh)
    
    #realiza detecção som o SimpleBlobDetector
    keypoints = detector.detect(notThresh)
    
    #indica os pontos detectados com um círculo vermelho
    original_mais_deteccao = cv.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    #pinta toda região detectada pelo blob detector de cinza
    newThresh = thresh.copy()
    for kp in keypoints:
        y,x = kp.pt
        if thresh[(int)(x),(int)(y)]==255:#evita acidentalmente pintar fora da área desejada
            cv.floodFill(newThresh, None, ((int)(y),(int)(x)), 125)
    
    #cria uma imagem que contém apenas a região cinza, ou seja, o que foi detectado pelo blob detector
    newThresh = cv.inRange(newThresh,124,126)
    
    #desenha os retângulos em image com o que foi detectado em newTrhesh, terceiro e quarto argumentos são área mínima e máxima do retângulo
    imgRetangulos = desenhaRetangulos(image,newThresh,rectMin,rectMax)
    
    
    #mostra imagens desejadas
    #cv.imshow(originalWnd,image)
    cv.imshow(predetectWnd,thresh)
    cv.imshow(blobWnd,original_mais_deteccao)
    cv.imshow(retanguloWnd,imgRetangulos)
    cv.imshow(imgLimpaWnd,newThresh)
    
    if cv.waitKey(1) & 0xFF == ord('q'):#pára código ao apertar 'q'
        break
        
cv.destroyAllWindows()
