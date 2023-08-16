import face_recognition as fr
import cv2 as cv
import os
import pickle
import time

FPSReport=0
scaleFactor=.33

dispW=320
dispH=240

Encodings=[]
Names=[]

with open('/home/es017590/Desktop/pyPro/trainingData.pkl', 'rb') as f:
    Names=pickle.load(f)
    Encodings=pickle.load(f)
print('Trainig data loaded!')

font=cv.FONT_HERSHEY_SIMPLEX
cam=cv.VideoCapture(1)
cam.set(cv.CAP_PROP_FRAME_WIDTH, dispW)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, dispH)

timeStamp=time.time()

while True:
    _,frame=cam.read()
    frameSmall=cv.resize(frame, (0,0), fx=scaleFactor,fy=scaleFactor)
    frameRGB=cv.cvtColor(frameSmall,cv.COLOR_BGR2RGB)
    facePositions=fr.face_locations(frameRGB,model='cnn')
    allEncodings=fr.face_encodings(frameRGB, facePositions)
    for (top,right,bottom,left), face_encoding in zip(facePositions, allEncodings): 
        name='Unknown'
        matches=fr.compare_faces(Encodings, face_encoding)
        if True in matches:
            first_match_index=matches.index(True)
            name=Names[first_match_index]
        top=int(top/scaleFactor)
        right=int(right/scaleFactor)
        bottom=int(bottom/scaleFactor)
        left=int(left/scaleFactor)
        cv.rectangle(frame, (left, top), (right, bottom), (0,0,255), 2)
        cv.putText(frame, name, (left, top-6), font, .5,(245,245,50), 1)
    dt=time.time()-timeStamp
    timeStamp=time.time()
    fps=1/dt
    FPSReport=.90*FPSReport+.1*fps
    cv.rectangle(frame, (5,10), (80, 40), (0,0,0), -1)
    cv.putText(frame, str(round(FPSReport, 3))+'fps', (8,30), font, .5, (255,255,255),1)   
    cv.imshow('img', frame)
    cv.moveWindow('img',0,0)

    if cv.waitKey(1)==ord('q'):
        break

cam.release()
piCam.release()
cv.destroyAllWindows()