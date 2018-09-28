# encoding: utf-8
import numpy as np
import cv2 as cv
from util import *
from time import clock

"""
Código para calibração do detector de linhas da pista por Harris corner detection.

Ao executar, mova as janelas porque elas começam em cima uma das outras.

Detecta as regiões consideradas como borda pelo Harris corner detector e desenha retângulos

"""


numeroDeSets = 3
numeroDeImagens = 21
path = './videos/'
video = 'nissan.mp4'


#cria janela para parâmetros
wnd = 'Parametros'
cv.namedWindow(wnd)
cv.resizeWindow(wnd,(800,600))

#cria um slider para cada parâmetro
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

anguloMinBar = 'Angulo minimo'
cv.createTrackbar(anguloMinBar, wnd,0,180,nothing)

anguloMaxBar = 'Angulo maximo'
cv.createTrackbar(anguloMaxBar, wnd,180,180,nothing)

#nomes das janelas
#originalWnd = 'Original'
predetectWnd = 'Binarizada'
harrisWnd = 'Harris Detection'
retanguloWnd = 'Retangulos'

#cria e muda tamanho das janelas
dimensoes = (600,400)
#criaERedimensionaJanelas(originalWnd,dimensoes)
criaERedimensionaJanelas(predetectWnd,dimensoes)
criaERedimensionaJanelas(harrisWnd,dimensoes)
criaERedimensionaJanelas(retanguloWnd,dimensoes)

tempoAtual = clock()

saiDoLoop = False



while(True):
    cap = cv.VideoCapture(path+video)
    
    if saiDoLoop:
        break
    while(True):
        
        #lê parâmetros dos sliders
        thValue = cv.getTrackbarPos(thValueBar, wnd)
        blurKernelSize = 2*cv.getTrackbarPos(blurKernelBar, wnd) - 1
        openingKernelSize = 2*cv.getTrackbarPos(openingKernelBar, wnd) - 1
        
        harris_blockSize = cv.getTrackbarPos(harris_blockSizeBar, wnd)+1
        harris_kSize = 2*cv.getTrackbarPos(harris_kSizeBar, wnd)+1
        harris_k = 1.0*(cv.getTrackbarPos(harris_kBar, wnd)/1000) +0.04

        rectMin = cv.getTrackbarPos(rectMinBar, wnd)
        rectMax = cv.getTrackbarPos(rectMaxBar, wnd)
        anguloMin = cv.getTrackbarPos(anguloMinBar, wnd)
        anguloMax = cv.getTrackbarPos(anguloMaxBar, wnd)
        
        _, image = cap.read()#lê imagem

        #reinicia vídeo ao final
        try:
            gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)#converte para escala de cinza
        except:
            
            break
            
        bl = blur(gray,blurKernelSize)
        
        ope = opening(bl,openingKernelSize)
        
        histImg = cv.equalizeHist(ope)

        _, thresh = cv.threshold(histImg,thValue,255,cv.THRESH_BINARY)
        

        #realiza detecção de bordas por Harris Corner Detection
        harris = cv.cornerHarris(thresh,harris_blockSize,harris_kSize,harris_k)
        imgHarris = thresh.copy()
        
        #pinta de cinza as bordas
        #imgHarris[harris>0.01*harris.max()] = 125 #cantos
        imgHarris[harris<0.01*harris.min()] = 125 #bordas
        
        
        #cria uma imagem que contém apenas a região cinza, ou seja, o que foi detectado pelo blob detector
        imgHarris = cv.inRange(imgHarris,124,126)
        
        #desenha os retângulos em image com o que foi detectado pelo Harris detector, terceiro e quarto argumentos são área mínima e máxima do retângulo
        imgRetangulos = desenhaRetangulos(image,imgHarris,rectMin,rectMax,anguloMin,anguloMax)
        
        
        #mostra imagens desejadas
        #cv.imshow(originalWnd,image)
        cv.imshow(predetectWnd,thresh)
        cv.imshow(harrisWnd, imgHarris)
        cv.imshow(retanguloWnd,imgRetangulos)
        
        if cv.waitKey(1) & 0xFF == ord('q'):#pára código ao apertar 'q'
            saiDoLoop = True
            break
        
        if cv.waitKey(1) & 0xFF == ord('p'):#pausa código ao apertar 'p', continua com 'c'
            while True:
                if cv.waitKey(1) & 0xFF == ord('c'):
                    break    
               
        ultimoTempo = tempoAtual
        tempoAtual = clock()
        mantemFps(tempoAtual,ultimoTempo)
        
cv.destroyAllWindows()
