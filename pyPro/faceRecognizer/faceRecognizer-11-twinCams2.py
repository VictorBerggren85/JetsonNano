from threading import Thread
import cv2 as cv
import time as t
import numpy as np

###CLASS########################################################
scaleFactor=.33
class vStream:
    def __init__(self,src,w,h):
        self.width=w
        self.height=h
        self.capture=cv.VideoCapture(src)
        if src==1:
            self.capture.set(cv.CAP_PROP_FRAME_WIDTH, w)
            self.capture.set(cv.CAP_PROP_FRAME_HEIGHT, h)
        self.thread=Thread(target=self.update,args=())
        self.thread.daemon=True
        self.thread.start()
    def update(self):
        while True:
            _,self.frame=self.capture.read()
    def getFrame(self):
        return self.frame
###CLASS########################################################

flip=0
dispW=320
dispH=240
cam1=vStream(1,dispW,dispH)
cam2=vStream('nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink',dispW,dispH)
startTime=t.time()
font=cv.FONT_HERSHEY_SIMPLEX
dtav=0

def showFPS(method,fps,frame):
    if method=='box':
        cv.rectangle(combinedFrame,(5,5),(95,35),(0,0,0),-1)
        cv.putText(combinedFrame,str(round(fps,2))+'fps',(8,25), font,.5,(255,255,255),1)
    if method=='print':
        print('Fps:',fps)

tryNum=0
while True:
    try:
        frame1=cam1.getFrame()
        frame2=cam2.getFrame()
        combinedFrame=np.hstack((frame1,frame2))
        
        dt=t.time()-startTime
        startTime=t.time()
        dtav=.9*dtav+.1*dt
        fps=1/dtav
        showFPS('box',fps,combinedFrame)

        cv.imshow('img',combinedFrame)
        cv.moveWindow('img',0,0)
    except:
        tryNum=tryNum+1
        print('tryNum:',tryNum)
        if tryNum>=50:
            cam1.capture.release()
            cam2.capture.release()
            cv.destroyAllWindows()
            exit(1)
            break    

    if cv.waitKey(1)==ord('q'):
        cam1.capture.release()
        cam2.capture.release()
        cv.destroyAllWindows()
        exit(1)
        break
