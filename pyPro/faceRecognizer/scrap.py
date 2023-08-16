from threading import Thread
import face_recognition as fr
import cv2 as cv
import time as t
import numpy as np
import pickle

###CLASS########################################################
class vStream:
    def __init__(self,src,w,h,sf):
        self.src=src
        self.width=w
        self.height=h
        self.scale=sf
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
    def getSmallFaces(self):
        frameRGB=cv.cvtColor(cv.resize(self.frame, (0,0),fx=self.scale,fy=self.scale),cv.COLOR_BGR2RGB)
        facePos=fr.face_locations(frameRGB,model='cnn')
        return facePos, fr.face_encodings(frameRGB,facePos)
            
###CLASS########################################################

Names=[]
Encodings=[]
with open('/home/es017590/Desktop/pyPro/trainingData.pkl', 'rb') as f:
    Names=pickle.load(f)
    Encodings=pickle.load(f)
print('Trainig data loaded!')

flip=0
dispW=320
dispH=240
scaleFactor=.33
cam1=vStream(1,dispW,dispH,scaleFactor)
cam2=vStream('nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink',dispW,dispH,scaleFactor)
startTime=t.time()
font=cv.FONT_HERSHEY_SIMPLEX
tryNum=0
dtav=0
frame1=[]
frame2=[]

def showFPS(method,fps,frame):
    if method=='box':
        cv.rectangle(combinedFrame,(5,5),(95,35),(0,0,0),-1)
        cv.putText(combinedFrame,str(round(fps,2))+'fps',(8,25), font,.5,(255,255,255),1)
    if method=='print':
        print('Fps:',fps)

def findIdentifyNameEncloce(cam):
    frame=cam.getFrame()
    facePos,allEncodings=cam.getSmallFaces()
    for (top,right,bottom,left), face_encoding in zip(facePos, allEncodings):
        name='unknown'
        matches=fr.compare_faces(Encodings,face_encoding)
        if True in matches:
            first_match_index=matches.index(True)
            name=Names[first_match_index]
        top=top*scaleFactor
        right=right*scaleFactor
        bottom=bottom*scaleFactor
        left=left*scaleFactor
        cv.rectangle(frame,(left,top),(right,bottom),(0,0,255),2)
        cv.putText(frame,name,(left,top-6),font,.5,(200,200,0),1)
    if cam.src==1:
        print('cam1')
        frame2=frame
        print('cam1done')
    else:
        print('cam2')
        frame1=frame
        print('cam2done')


thread1=Thread(target=findIdentifyNameEncloce,args=([cam1]))
thread2=Thread(target=findIdentifyNameEncloce,args=([cam2]))
thread1.daemon=True
thread2.daemon=True
wait=0
while True:
    try:
        print('try')
        thread1.run()
        print('threads')
        thread2.run()
        print('threads')

        while (frame1==[] and frame2==[]):
            wait=wait+1
        print(wait)
        combinedFrame=np.hstack((frame1,frame2))

        frame1=[]
        frame2=[]

        dt=t.time()-startTime
        startTime=t.time()
        dtav=.9*dtav+.1*dt
        fps=1/dtav
        showFPS('print',fps,combinedFrame)

        cv.imshow('img',combinedFrame)
        cv.moveWindow('img',0,0)
    except:
        tryNum=tryNum+1
        print('tryNum:',tryNum)
        if tryNum>=25:
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
