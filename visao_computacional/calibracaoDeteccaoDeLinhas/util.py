# encoding: utf-8
import numpy as np
import cv2 as cv
import math

def ROIporPorcentagem(img,y1,y2,x1,x2):
    """Recebe intervalos dados em porcentagens da ROI desejada e retorna a ROI 
    Por exemplo a metade superior da imagem seria (img,0,50,0,100)
    """
    yMax, xMax = img.shape[0:2]
    return img[(yMax*y1)//100:(yMax*y2)//100,(xMax*x1)//100:(xMax*x2)//100]

class roiObject:
    """recebe a imagem da qual se quer fazer uma roi e as coordenadas dadas em porcentagem e cria um objeto
    """
    def _init_(self,img,y1,y2,x1,x2):
        yMax, xMax = img.shape[0:2]
        self.roi = img[(yMax*y1)//100:(yMax*y2)//100,(xMax*x1)//100:(xMax*x2)//100]
        self.yRoi = (yMax*y1)//100
        self.xRoi = (xMax*x1)//100
        self.height = (yMax*y2)//100 - self.yRoi
        self.width = (xMax*x2)//100 - self.xRoi
    
    def getRoi(self):
        return self.roi
    
    def getAbsCoord(self,y,x):
        """retorna as coordenadas em relação à imagem original dadas as coordenadas em relação à região de interesse
        """
        return (self.yRoi+y,self.xRoi+x)

def nothing(x):#função que faz nada para passar para os sliders com ação automática
    pass
    
def distanciaEntrePontos(x1,y1,x2,y2):
    dx = x2-x1
    dy = y2-y1
    return math.sqrt(dx**2+dy**2)

def desenhaLinhas(img,cnt):
    rows,cols = img.shape[:2]
    [vx,vy,x,y] = cv.fitLine(cnt, cv.DIST_L2,0,0.01,0.01)
    lefty = int((-x*vy/vx) + y)
    righty = int(((cols-x)*vy/vx)+y)
    try:
        cv.line(img,(cols-1,righty),(0,lefty),(0,255,0),2)
    except:
        pass

def anguloDoRetangulo(retangulo):
    #retângulo armazena ângulos de uma forma que é necessário fazer uns ajustes para conseguir o àngulo corretamente
    largura = retangulo[1][0]
    altura = retangulo[1][1]
    angulo = retangulo[2]
    if largura < altura:
        angulo = 90-angulo
    if angulo<0:
        angulo = abs(angulo)
    return round(angulo,2)
        
def escreveTexto(img,texto,coord):
	"""escreve texto na imagem"""
	fonte = cv.FONT_HERSHEY_PLAIN
	escala = 2
	cor = (0,255,0)
	linha = 2

	cv.putText(img,texto, coord, fonte, escala, cor, linha)
        
def desenhaRetangulos(imgOriginal,thresh,contourAreaMin,contourAreaMax):
    """Recebe a imgem original e uma 
    """
    img = imgOriginal.copy()
    
    #lida com problemas de versao
    try:
        _, contours, _ = cv.findContours(thresh,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    except:
        contours, _ = cv.findContours(thresh,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    
    
    cor = (0,0,255)#cor do retangulo que encompassa semaforo 
    
    #para cada contorno detectado encontra um bounding box
    for contour in contours:
        areaContour = cv.contourArea(contour)
        if areaContour>contourAreaMin and areaContour<contourAreaMax:
            retangulo = cv.minAreaRect(contour)
            coordY = (int)(retangulo[0][0])
            coordX = (int)(retangulo[0][1])
            escreveTexto(img,(str)(anguloDoRetangulo(retangulo)),(coordY,coordX))
            #lida com problemas de versao
            try:
                caixa = cv.boxPoints(retangulo)
            except:
                caixa = cv.cv.BoxPoints(retangulo)
            
            caixa = np.int0(caixa)
            cv.drawContours(img,[caixa],0,cor,3)

    return img

def calculaMatrizBEV(dstCols,dstRows,margemCols,margemRows):

    rowHigh = dstRows
    colHigh = dstCols - (int)(dstRows*margemCols)
    rowLow = (int)(dstRows*margemCols)
    colLow = 0 + (int)(dstRows*margemCols)

    pts1 = np.float32([[110,80],[20,130],[220,80],[319,138]])
    pts2 = np.float32([[colLow,rowLow],[colLow,rowHigh],[colHigh,rowLow],[colHigh,rowHigh]])

    return cv.getPerspectiveTransform(pts1,pts2)


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
        
def imagemVazia(img):
    """retorna uma imagem vazia (todos os pixels pretos) com as mesmas dimensoes de img
    """
    return np.zeros((img.shape[0],img.shape[1]),np.uint8)
    
def desenhaHoughLines(thresh):
    imgLines = imagemVazia(thresh)
    imgLines = cv.bitwise_not(imgLines)
    lines = cv.HoughLines(thresh,1,np.pi/180,150,200)
    try:
        for line in lines:
            for rho, theta in line:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
        
                cv.line(imgLines,(x1,y1),(x2,y2),(0,0,255),2)
    except:
        pass
        
    return imgLines
    
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

