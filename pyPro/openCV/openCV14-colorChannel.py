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

blank=np.zeros([dispH, dispW, 1], np.uint8)

while True:
    ret, frame=cam.read()
#    print(frame[50,45,1])
#    print(frame.shape)
#    print(frame.size)
#
#    fGray=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
#    print(fGray.shape)
#    print(fGray.size)

#    b=cv.split(frame)[0]
#    g=cv.split(frame)[1]
#    r=cv.split(frame)[2]

    b,g,r=cv.split(frame)

    blue=cv.merge((b,blank,blank))
    green=cv.merge((blank, g, blank)) 
    red=cv.merge((blank, blank, r))

    merge=cv.merge((b,g,r))

#colour split channels (gray)
    cv.imshow('grey blue', b)
    cv.moveWindow('grey blue', dispW+5, 25)
    cv.imshow('grey green', g)
    cv.moveWindow('grey green', 2*(dispW+5), 25)
    cv.imshow('grey red', r)
    cv.moveWindow('grey red', 3*(dispW+5), 25)        

#colour split channels
    cv.imshow('blue', blue)
    cv.moveWindow('blue', dispW+5, dispH+50)
    cv.imshow('green', green)
    cv.moveWindow('green', 2*(dispW+5), dispH+50)
    cv.imshow('red', red)
    cv.moveWindow('red', 3*(dispW+5), dispH+50)        

    cv.imshow('merge', merge)
    cv.moveWindow('merge', 0, dispH+50)

    cv.imshow('piCam', frame)
    if cv.waitKey(1)==ord('q'):
        break
cam.release()
cv.destroyAllWindows()
