import cv2
import numpy as np

# Activating Web Cam

framewidth = 640
frameheight = 480

cap = cv2.VideoCapture(0)
cap.set(3,framewidth)
cap.set(4,frameheight)


myColors = [[155,115,62,175,255,255],
            [30,55,88,73,254,255],
            [87,43,93,120,255,255]]

mycolorsVal = [[102,0,255],
                [0,255,0],
                [255,102,0]]  #BGR

myPoints = []  # [x , y , colorId ]

# Code for detecting colors.q
def findColor(img,myColors,mycolorsVal):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints=[]
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        x,y=getContours(mask)
        cv2.circle(imgResult,(x,y),10,mycolorsVal[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        #cv2.imshow(str(color[0]), mask)
        count+=1
    return newPoints


# Code for detecting shape

def getContours(img):
    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) #RETR_EXTERNAL --> Finds the contour by external method.
    x,y,w,h =0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt) #Gets the area of the contour.
        if area > 500:
            #cv2.drawContours(imgResult,cnt,-1,(0,0,255),4)  #draws contour over the image. {-1} is for_all objects.
            peri = cv2.arcLength(cnt,True) # Calculates the perimeter of the objects.
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True) # Calulates the position point of the contour
            x, y, w, h = cv2.boundingRect(approx) #gets the values of x,y,w,h.
    return x+w//2, y

def drawonCanvas(myPoints,mycolorsVal):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, mycolorsVal[point[2]], cv2.FILLED)


while(True):
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img,myColors,mycolorsVal)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints)!=0:
        drawonCanvas(myPoints,mycolorsVal)

    cv2.imshow("imgshow", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break