import face_recognition as fr
import numpy as np
import cv2 as cv
import time

FPSReport=0
scaleFactor=.33

flip=0 #Flip cam

dispW=320
dispH=240

camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
piCam=cv.VideoCapture(camSet)

font=cv.FONT_HERSHEY_SIMPLEX
cam=cv.VideoCapture(1)
cam.set(cv.CAP_PROP_FRAME_WIDTH, dispW)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, dispH)

timeStamp=time.time()

while True:
    _,frame=cam.read()
    _,piFrame=piCam.read()

    dt=time.time()-timeStamp
    timeStamp=time.time()
    fps=1/dt
    FPSReport=.90*FPSReport+.1*fps
    
    cv.rectangle(frame, (5,10), (80, 40), (0,0,0), -1)
    cv.putText(frame, str(round(FPSReport, 1))+'fps', (8,30), font, .5, (255,255,255),1)   
    frameCombined=np.hstack((frame,piFrame))
    cv.imshow('img', frameCombined)
    cv.moveWindow('img',0,0) 

    if cv.waitKey(1)==ord('q'):
        break

cam.release()
piCam.release()
cv.destroyAllWindows()