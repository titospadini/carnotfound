import numpy as np
import cv2 as cv

cap = cv.VideoCapture('video1.mp4')
#cap = cv.VideoCapture('ROBORACE_pista.mp4')

ret, frame = cap.read()
rows,cols = frame.shape[:2]

dstCols = 600
dstRows = 800

rowHigh = dstRows
colHigh = dstCols - (int)(dstRows*0.2)
rowLow = (int)(dstRows*0.6)
colLow = 0 + (int)(dstRows*0.2)

pts1 = np.float32([[110,80],[20,130],[220,80],[319,138]])
pts2 = np.float32([[colLow,rowLow],[colLow,rowHigh],[colHigh,rowLow],[colHigh,rowHigh]])

matrizVisaoTopo = cv.getPerspectiveTransform(pts1,pts2)

while(cap.isOpened()):
    
    ret, frame = cap.read()
    
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    blur = cv.GaussianBlur(gray,(5,5),0)
    kernel = np.ones((3,3),np.uint8)
    opening = cv.morphologyEx(blur, cv.MORPH_OPEN, kernel)
    ret,thresh = cv.threshold(opening,180,255,cv.THRESH_BINARY)


    #dst = cv.warpPerspective(thresh,matrizVisaoTopo,(dstCols,dstRows))
    dst = cv.warpPerspective(frame,matrizVisaoTopo,(dstCols,dstRows))
    
    cv.imshow('frame',frame)
    cv.imshow('dst',dst)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
        
    if cv.waitKey(1) & 0xFF == ord('p'):#pausa com 'p' e continua com 'c'
        while(True):
            if cv.waitKey(1) & 0xFF == ord('c'):
                break
        
        


cap.release()
cv.destroyAllWindows()



'''
pts1 = np.float32([[118,146],[79,238],[218,147],[272,239]])
pts2 = np.float32([[colLow,rowLow],[colLow,rowHigh],[colHigh,rowLow],[colHigh,rowHigh]])

pts1 = np.float32([[85,146],[54,238],[218,147],[315,239]])
pts2 = np.float32([[colLow,rowLow],[colLow,rowHigh],[colHigh,rowLow],[colHigh,rowHigh]])

pts1 = np.float32([[134,61],[14,134],[197,60],[319,136]])
pts2 = np.float32([[colLow,rowLow],[colLow,rowHigh],[colHigh,rowLow],[colHigh,rowHigh]])

pts1 = np.float32([[132,80],[66,239],[165,80],[256,239]])
pts2 = np.float32([[colLow,rowLow],[colLow,rowHigh],[colHigh,rowLow],[colHigh,rowHigh]])
'''
