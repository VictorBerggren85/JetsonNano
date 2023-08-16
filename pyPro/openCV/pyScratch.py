import cv2 as cv
import numpy as np

dispW=320
dispH=240
flip=0 #Flip cam

floaterW=64
floaterH=48

BXPos=10
BYPos=10
dx=2
dy=2

floater=cv.imread('pl.jpg')
floater=cv.resize(floater, (floaterW, floaterH))
fGray=cv.cvtColor(floater, cv.COLOR_BGR2GRAY)
cv.imshow('floater gray', fGray)
cv.moveWindow('floater gray', dispW+5, 25)

_,BGMask=cv.threshold(fGray, 220, 255, cv.THRESH_BINARY)
cv.imshow('bg mask', BGMask)
cv.moveWindow('bg mask', int(dispW+(dispW/5+5)), 25)

FGMask=cv.bitwise_not(BGMask)
cv.imshow('fg mask', FGMask)
cv.moveWindow('fg mask', int(dispW+(dispW/5+5)*2), 25)

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

    box=frame[BYPos:BYPos+floaterH, BXPos:BXPos+floaterW]

    #frame=cv.rectangle(frame, (BXPos, BYPos), (BXPos+BW, BYPos+BH), (90, 150, 90), -1)
    BXPos=BXPos+dx
    BYPos=BYPos+dy
    
    if BXPos+int(dispW/5) >= dispW or BXPos <= 0:
        dx=dx*-1
    if BYPos+int(dispH/5) >= dispH or BYPos <= 0:
        dy=dy*-1

    cv.imshow('box', box)
    cv.moveWindow('box', int(dispW+(dispW/5+5)*3), 25)
    BG=cv.bitwise_and(box, box, mask=BGMask)
    cv.imshow('BG', BG)
    cv.moveWindow('BG', int(dispW+(dispW/5+5)*4), 25)    
    FG=cv.bitwise_and(floater, floater, mask=FGMask)
    cv.imshow('FG', FG)
    cv.moveWindow('FG', int(dispW+(dispW/5+5)*5), 25)  
    merge=cv.add(BG, FG)
    cv.imshow('merge', merge)
    cv.moveWindow('merge', int(dispW+(dispW/5+5)*6), 25) 

    frame[BYPos:BYPos+floaterH, BXPos:BXPos+floaterW]=merge

   # blendVal=cv.getTrackbarPos('BlendVal', 'blended')/100
   # blendedVal2=1-blendVal
#
   # Blended=cv.addWeighted(frame, blendVal, cvLogo, blendedVal2, 0)
   # 
   # FG2=cv.bitwise_and(Blended, Blended, mask=FGMask)
   # 
   # compFinale=cv.add(BG, FG2)

    #cv.imshow('compF', compFinale)
    #cv.moveWindow('compF', 0, dispH*3+100)
#
    #cv.imshow('fg2', FG2)
    #cv.moveWindow('fg2', 4*(dispW+5), dispH*2+75)
#
    #cv.imshow('blended', Blended)
    #cv.moveWindow('blended', 3*(dispW+5), dispH*2+75)
#
    cv.imshow('piCam', frame)
    cv.moveWindow('piCam', 0, 0)
#
    #cv.imshow('maskCam', BG)
    #cv.moveWindow('maskCam', 0, dispH+50)    
#
    #cv.imshow('comp', compImg)
    #cv.moveWindow('comp', 0, dispH*2+75) 

    if cv.waitKey(1)==ord('q'):
        break

cam.release()
#outVid.release()
cv.destroyAllWindows()
