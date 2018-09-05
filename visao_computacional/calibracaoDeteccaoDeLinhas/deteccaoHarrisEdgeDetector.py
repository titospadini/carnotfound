# encoding: utf-8
import numpy as np
import cv2 as cv
from util import *

"""
Código para calibração do detector de linhas da pista por Harris corner detection.

Ao executar, mova as janelas porque elas começam em cima uma das outras.

Detecta as regiões consideradas como borda pelo Harris corner detector e desenha retângulos

"""


numeroDeSets = 3
numeroDeImagens = 21



#cria janela para parâmetros
wnd = 'Parametros'
cv.namedWindow(wnd)
cv.resizeWindow(wnd,(800,600))
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

harris_blockSizeBar = 'harris block size'
cv.createTrackbar(harris_blockSizeBar, wnd,0,10,nothing)

harris_kSizeBar = 'harris k size'
cv.createTrackbar(harris_kSizeBar, wnd,0,10,nothing)

harris_kBar = 'harris free parameter(0,04 - 0,06)'
cv.createTrackbar(harris_kBar, wnd,0,20,nothing)

rectMinBar = 'Area minima do retangulo'
cv.createTrackbar(rectMinBar, wnd,80,5000,nothing)

rectMaxBar = 'Area maxima do retangulo'
cv.createTrackbar(rectMaxBar, wnd,2000,5000,nothing)

#nomes das janelas
#originalWnd = 'Original'
predetectWnd = 'Binarizada'
harrisWnd = 'Harris Detection'
retanguloWnd = 'Retangulos'

#cria e muda tamanho das janelas
dimensoes = (400,300)
#criaERedimensionaJanelas(originalWnd,dimensoes)
criaERedimensionaJanelas(predetectWnd,dimensoes)
criaERedimensionaJanelas(harrisWnd,dimensoes)
criaERedimensionaJanelas(retanguloWnd,dimensoes)

while(True):

    #lê parâmetros dos sliders
    indexSet = cv.getTrackbarPos(indexSetBar, wnd)
    indexFoto = cv.getTrackbarPos(indexFotoBar, wnd)
    thValue = cv.getTrackbarPos(thValueBar, wnd)
    blurKernelSize = 2*cv.getTrackbarPos(blurKernelBar, wnd) - 1
    openingKernelSize = 2*cv.getTrackbarPos(openingKernelBar, wnd) - 1
    
    harris_blockSize = cv.getTrackbarPos(harris_blockSizeBar, wnd)+1
    harris_kSize = 2*cv.getTrackbarPos(harris_kSizeBar, wnd)+1
    harris_k = 1.0*(cv.getTrackbarPos(harris_kBar, wnd)/1000) +0.04

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
    

    #realiza detecção de bordas por Harris Corner Detection
    harris = cv.cornerHarris(gray,harris_blockSize,harris_kSize,harris_k)
    imgHarris = thresh.copy()
    
    #pinta de cinza as bordas
    #imgHarris[harris>0.01*harris.max()] = 125 #cantos
    imgHarris[harris<0.01*harris.min()] = 125 #bordas
    
    
    #cria uma imagem que contém apenas a região cinza, ou seja, o que foi detectado pelo blob detector
    imgHarris = cv.inRange(imgHarris,124,126)
    
    #desenha os retângulos em image com o que foi detectado pelo Harris detector, terceiro e quarto argumentos são área mínima e máxima do retângulo
    imgRetangulos = desenhaRetangulos(image,imgHarris,rectMin,rectMax)
    
    
    #mostra imagens desejadas
    #cv.imshow(originalWnd,image)
    cv.imshow(predetectWnd,thresh)
    cv.imshow(harrisWnd, imgHarris)
    cv.imshow(retanguloWnd,imgRetangulos)
    
    if cv.waitKey(1) & 0xFF == ord('q'):#pára código ao apertar 'q'
        break
        
cv.destroyAllWindows()
