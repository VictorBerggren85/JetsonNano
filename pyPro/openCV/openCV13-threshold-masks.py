import cv2 as cv
import numpy as np

dispW=320
dispH=240
flip=0 #Flip cam

def nothing(x):
    pass
cv.namedWindow('blended')
cv.createTrackbar('BlendVal', 'blended', 50, 100, nothing)

cvLogo=cv.imread('cv.jpg')
cvLogo=cv.resize(cvLogo, (dispW, dispH))
cvLogoGray=cv.cvtColor(cvLogo, cv.COLOR_BGR2GRAY)
cv.imshow('cv logo gray', cvLogoGray)
cv.moveWindow('cv logo gray', dispW+5, 25)

_,BGMask=cv.threshold(cvLogoGray, 220, 255, cv.THRESH_BINARY)

cv.imshow('logo mask', BGMask)
cv.moveWindow('logo mask', dispW+5, dispH+50)

FGMask=cv.bitwise_not(BGMask)
cv.imshow('logo fg mask', FGMask)
cv.moveWindow('logo fg mask', dispW+5, dispH*2+75)

FG=cv.bitwise_and(cvLogo, cvLogo, mask=FGMask)
cv.imshow('FG', FG)
cv.moveWindow('FG', 2*(dispW+5), dispH*2+75)

camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cv.namedWindow('piCam')

#launch camera
## RpiCamera
cam=cv.VideoCapture(camSet)    
## RpiCamera

## USBCamera
#cam=cv.VideoCapture(1)        
#cam.set(cv.CAP_PROP_FRAME_WIDTH, dispW/2)
#cam.set(cv.CAP_PROP_FRAME_HEIGHT, dispH/2)
## USBCamera

#cam=cv.VideoCapture('videos/myCam.avi') 
#outVid=cv.VideoWriter('videos/myCam.avi', cv.VideoWriter_fourcc(*'XVID'), 21, (dispW, dispH))

while True:
    ret, frame=cam.read()

    BG=cv.bitwise_and(frame, frame, mask=BGMask)
    compImg=cv.add(BG, FG)

    blendVal=cv.getTrackbarPos('BlendVal', 'blended')/100
    blendedVal2=1-blendVal

    Blended=cv.addWeighted(frame, blendVal, cvLogo, blendedVal2, 0)
    
    FG2=cv.bitwise_and(Blended, Blended, mask=FGMask)
    
    compFinale=cv.add(BG, FG2)

    cv.imshow('compF', compFinale)
    cv.moveWindow('compF', 0, dispH*3+100)

    cv.imshow('fg2', FG2)
    cv.moveWindow('fg2', 4*(dispW+5), dispH*2+75)

    cv.imshow('blended', Blended)
    cv.moveWindow('blended', 3*(dispW+5), dispH*2+75)

    cv.imshow('piCam', frame)
    cv.moveWindow('piCam', 0, 0)

    cv.imshow('maskCam', BG)
    cv.moveWindow('maskCam', 0, dispH+50)    

    cv.imshow('comp', compImg)
    cv.moveWindow('comp', 0, dispH*2+75) 

    if cv.waitKey(1)==ord('q'):
        break

cam.release()
#outVid.release()
cv.destroyAllWindows()
