# encoding: utf-8
import numpy as np
import cv2 as cv

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


def nothing(x):#função que faz nada para passar para os sliders com ação automática
    pass
    
def criaERedimensionaJanelas(nomeJanela,dimensoes):
    cv.namedWindow(nomeJanela,cv.WINDOW_NORMAL)
    cv.resizeWindow(nomeJanela, dimensoes)

#funções abaixo só são realizadas se o tamanho do kernel não for -1
def blur(img,kernelSize):
    if kernelSize == -1:
        return img
    else:
        return cv.GaussianBlur(img,(kernelSize,kernelSize),0)

def opening(img,kernelSize):
    if kernelSize == -1:
        return img
    else:
        kernel = np.ones((kernelSize,kernelSize),np.uint8)
        return cv.morphologyEx(img, cv.MORPH_OPEN, kernel)
    
def sobelXY(img, kernelSize):
    if kernelSize == -1:
        return img
    else:
        sobelx8u = cv.Sobel(img,cv.CV_8U,1,0,ksize=kernelSize)
        sobely8u = cv.Sobel(img,cv.CV_8U,0,1,ksize=kernelSize)
        return sobelx8u+sobely8u

def filtragemBlobParametros(faixaMinPixels,faixaMaxPixels,faixaMinInertia,faixaMaxInertia):
    parametros = cv.SimpleBlobDetector_Params()
    
    parametros.minThreshold = 10
    parametros.minThreshold = 200
    
    parametros.filterByArea = True
    parametros.minArea = faixaMinPixels
    parametros.maxArea = faixaMaxPixels
    
    #taxa de inercia baixo => objeto alongado ; taxa de inercia alto => objeto arredondado 
    parametros.filterByInertia = True
    parametros.minInertiaRatio = faixaMinInertia
    parametros.maxInertiaRatio = faixaMaxInertia
    
    parametros.filterByConvexity = False
    parametros.filterByCircularity = False
    
    return parametros

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
cv.createTrackbar(faixaMinAreaBar, wnd,0,10000,nothing)

faixaMaxAreaBar = 'Area maxima'
cv.createTrackbar(faixaMaxAreaBar, wnd,0,10000,nothing)

faixaMinInertiaBar = 'Inercia minima(%)'
cv.createTrackbar(faixaMinInertiaBar, wnd,0,100,nothing)

faixaMaxInertiaBar = 'Inercia maxima(%)'
cv.createTrackbar(faixaMaxInertiaBar, wnd,0,100,nothing)

#cria e muda tamanho das janelas
#originalWnd = 'Original'
predetectWnd = 'Binarizada'
blobWnd = 'Blob Detector'

dimensoes = (400,300)
#criaERedimensionaJanelas(originalWnd,dimensoes)
criaERedimensionaJanelas(predetectWnd,dimensoes)
criaERedimensionaJanelas(blobWnd,dimensoes)


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
    
    _,thresh = cv.threshold(ope,thValue,255,cv.THRESH_BINARY)
    
    #realiza detecção som o SimpleBlobDetector
    parametrosBlobDtector = filtragemBlobParametros(faixaMinPixels,faixaMaxPixels,faixaMinInertia,faixaMaxInertia)
    detector = cv.SimpleBlobDetector_create(parametrosBlobDtector)
    
    notThresh = cv.bitwise_not(thresh)
    keypoints = detector.detect(notThresh)
    original_mais_deteccao = cv.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    #cv.imshow(originalWnd,image)
    cv.imshow(predetectWnd,thresh)
    cv.imshow(blobWnd,original_mais_deteccao)
    
    
    if cv.waitKey(1) & 0xFF == ord('q'):#pára código ao apertar 'q'
        break

cv.destroyAllWindows()

