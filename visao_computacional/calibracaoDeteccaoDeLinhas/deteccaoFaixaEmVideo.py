# encoding: utf-8
import numpy as np
import cv2 as cv
from util import *

"""
Código para calibração do detector de linhas da pista.

Ao executar, mova as janelas porque elas começam em cima uma das outras

Valores bons:
Theshold = 155
Área mínima = 0
Área máxima = 2100
Inércia mínima = 0
Inércia máxima = 34

A inércia se refere ao quão alongado um objeto é. Valores baixos são objetos mais alongados e os altos são objetos mais arredondados. Com isso já dá para separar um pouco o que é uma faixa e o que é brilho do sol
"""


numeroDeSets = 3
numeroDeImagens = 21
path = './videos/'
video = 'ironcar.mp4'

#tamanho da imagem com perspectiva BEV
dstCols = 400
dstRows = 600
#margens da imagem com perspectiva BEV
margemCols = 0.2
margemRows = 0.6


#cria janela para parâmetros
wnd = 'Parametros'
cv.namedWindow(wnd)

#cria um slider para cada parâmetro
indexSetBar = 'Set escolhido'
cv.createTrackbar(indexSetBar, wnd,0,numeroDeSets-1,nothing)

indexFotoBar = 'Foto escolhida'
cv.createTrackbar(indexFotoBar, wnd,0,numeroDeImagens-1,nothing)

thValueBar = 'valor Threshold'
cv.createTrackbar(thValueBar, wnd,0,255,nothing)

blurKernelBar = 'tamanho do kernel para blur(2k-1)'
cv.createTrackbar(blurKernelBar, wnd,0,10,nothing)

openingKernelBar = 'tamanho do kernel para opening(2k-1)'
cv.createTrackbar(openingKernelBar, wnd,0,10,nothing)

faixaMinAreaBar = 'Area minima'
cv.createTrackbar(faixaMinAreaBar, wnd,200,10000,nothing)

faixaMaxAreaBar = 'Area maxima'
cv.createTrackbar(faixaMaxAreaBar, wnd,2000,10000,nothing)

faixaMinInertiaBar = 'Inercia minima(%)'
cv.createTrackbar(faixaMinInertiaBar, wnd,0,100,nothing)

faixaMaxInertiaBar = 'Inercia maxima(%)'
cv.createTrackbar(faixaMaxInertiaBar, wnd,25,100,nothing)

harris_blockSizeBar = 'harris block size'
cv.createTrackbar(harris_blockSizeBar, wnd,0,10,nothing)

harris_kSizeBar = 'harris k size'
cv.createTrackbar(harris_kSizeBar, wnd,0,10,nothing)

harris_kBar = 'harris free parameter(0,04 - 0,06)'
cv.createTrackbar(harris_kBar, wnd,0,20,nothing)


#cria e muda tamanho das janelas
#originalWnd = 'Original'
predetectWnd = 'Binarizada'
blobWnd = 'Blob Detector'
harrisWnd = 'Harris Detection'
#BEV_Wnd = 'Bird Eye View'
retangulosWnd = 'Retangulos'


dimensoes = (400,300)
#criaERedimensionaJanelas(originalWnd,dimensoes)
criaERedimensionaJanelas(predetectWnd,dimensoes)
criaERedimensionaJanelas(blobWnd,dimensoes)
criaERedimensionaJanelas(harrisWnd,dimensoes)
criaERedimensionaJanelas(retangulosWnd,dimensoes)

matrizVisaoTopo = calculaMatrizBEV(dstCols,dstRows,margemCols,margemRows)

saiDoLoop = False

while(True):
    cap = cv.VideoCapture(path+video)
    #cap = cv.VideoCapture('ROBORACE_pista.mp4')
    
    if saiDoLoop:
        break
    
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
        
        harris_blockSize = cv.getTrackbarPos(harris_blockSizeBar, wnd)+1
        harris_kSize = 2*cv.getTrackbarPos(harris_kSizeBar, wnd)+1
        harris_k = 1.0*(cv.getTrackbarPos(harris_kBar, wnd)/1000) +0.04
        

        _, image = cap.read()
        
        #reinicia vídeo
        try:
            gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)#converte para escala de cinza
        except:
            
            break
            
        bl = blur(gray,blurKernelSize)
        
        ope = opening(bl,openingKernelSize)
        
        _,thresh = cv.threshold(ope,thValue,255,cv.THRESH_BINARY)
        
        #_,thresh = cv.threshold(ope,thValue,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
        
        #realiza detecção som o SimpleBlobDetector
        parametrosBlobDtector = filtragemBlobParametros(faixaMinPixels,faixaMaxPixels,faixaMinInertia,faixaMaxInertia)
        detector = cv.SimpleBlobDetector_create(parametrosBlobDtector)
        
        notThresh = cv.bitwise_not(thresh)
        keypoints = detector.detect(notThresh)
        #coords = [keypoint.pt for keypoint in keypoints]
        
        original_mais_deteccao = cv.drawKeypoints(thresh, keypoints, np.array([]), (0,0,255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        #original_mais_deteccao = cv.warpPerspective(original_mais_deteccao,matrizVisaoTopo,(dstCols,dstRows))
        
        
        #realiza detecção de bordas por Harris Corner Detection
        harris = cv.cornerHarris(gray,harris_blockSize,harris_kSize,harris_k)
        imgHarris = image.copy()
        #imgHarris[harris>0.01*harris.max()] = [255,0,255] #cantos
        imgHarris[harris<0.01*harris.min()] = [255,0,255] #bordas
        imgHarris = cv.warpPerspective(imgHarris,matrizVisaoTopo,(dstCols,dstRows))
        
        
        
        for kp in keypoints:
            y,x = kp.pt
            cv.floodFill(thresh, None, ((int)(y),(int)(x)), 120)
        
        
        #desenha retângulos
        roiRetangulos = ROIporPorcentagem(image,30,100,0,100)
        roiRetangulosThresh = ROIporPorcentagem(thresh,30,100,0,100)
        imgRetangulos = desenhaRetangulos(roiRetangulos,roiRetangulosThresh,20,500)
        
        
        #cv.imshow(originalWnd,image)
        cv.imshow(predetectWnd,thresh)
        cv.imshow(blobWnd,original_mais_deteccao)
        cv.imshow(harrisWnd, imgHarris)
        cv.imshow(retangulosWnd, imgRetangulos)
        
        if cv.waitKey(1) & 0xFF == ord('q'):#pára código ao apertar 'q'
            saiDoLoop = True
            break
cv.destroyAllWindows()

