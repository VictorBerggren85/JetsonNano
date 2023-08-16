import cv2 as cv
import numpy as np

dispW=320
dispH=240
flip=0 #Flip cam
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

#launch camera
## RpiCamera
#cam=cv.VideoCapture(camSet)    
## RpiCamera

## USBCamera
cam=cv.VideoCapture(1)        
cam.set(cv.CAP_PROP_FRAME_WIDTH, dispW)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, dispH)
## USBCamera

def nothing(x):
    pass

cv.namedWindow('TB')
cv.moveWindow('TB', (dispW+5)*4, 25)

cv.createTrackbar('hueLower', 'TB', 50, 179, nothing)
cv.createTrackbar('hueHigher', 'TB', 100, 179, nothing)
cv.createTrackbar('hueLower2', 'TB', 50, 179, nothing)
cv.createTrackbar('hueHigher2', 'TB', 100, 179, nothing)
cv.createTrackbar('saturationLower', 'TB', 100, 225, nothing)
cv.createTrackbar('saturationHigher', 'TB', 255, 225, nothing)
cv.createTrackbar('valueLower', 'TB', 100, 255, nothing)
cv.createTrackbar('valueHigher', 'TB', 225, 255, nothing)


while True:
    ret, smarties=cam.read()
    cv.imshow('piCam', smarties)

   # smarties=cv.imread('smarties.png')
   # cv.imshow('smarties', smarties)

    hsv=cv.cvtColor(smarties, cv.COLOR_BGR2HSV)
    hueLow=cv.getTrackbarPos('hueLower', 'TB')
    hueHi=cv.getTrackbarPos('hueHigher', 'TB')
    hueLow2=cv.getTrackbarPos('hueLower2', 'TB')
    hueHi2=cv.getTrackbarPos('hueHigher2', 'TB')
    satLow=cv.getTrackbarPos('saturationLower', 'TB')
    satHi=cv.getTrackbarPos('saturationHigher', 'TB')
    valLow=cv.getTrackbarPos('valueLower', 'TB')
    valHi=cv.getTrackbarPos('valueHigher', 'TB')

    l_b=np.array([hueLow, satLow, valLow])
    u_b=np.array([hueHi, satHi, valHi])
    l_b2=np.array([hueLow2, satLow, valLow])
    u_b2=np.array([hueHi2, satHi, valHi])

    FGmask=cv.inRange(hsv, l_b, u_b)
    cv.imshow('FGMask', FGmask)
    cv.moveWindow('FGMask', 0, 430)

    FGmask2=cv.inRange(hsv, l_b2, u_b2)
    cv.imshow('FGMask2', FGmask2)
    cv.moveWindow('FGMask2', 0, 600)

    FGcOMP=cv.add(FGmask, FGmask2)
    cv.imshow('fgcomp', FGmask2)
    cv.moveWindow('fgcomp', 0, 860)

    FG=cv.bitwise_and(smarties, smarties, mask=FGmask)
    cv.imshow('FG', FG)
    cv.moveWindow('FG', 430, 430)

    BGmask=cv.bitwise_not(FGcOMP)
    cv.imshow('BGmask', BGmask)
    cv.moveWindow('BGmask', 430, 25) 

    BG=cv.cvtColor(BGmask, cv.COLOR_GRAY2BGR)

    final=cv.add(FG, BG)

    cv.imshow('final', final)
    cv.moveWindow('final', 860, 430)   

    if cv.waitKey(1)==ord('q'):
        break
cam.release()
cv.destroyAllWindows()
