import face_recognition as fr
import cv2 as cv
import os
import pickle

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

while True:
    _,frame=cam.read()
    frameSmall=cv.resize(frame, (0,0), fx=.33,fy=.33)
    frameRGB=cv.cvtColor(frameSmall,cv.COLOR_BGR2RGB)
    facePositions=fr.face_locations(frameRGB,model='cnn')
    allEncodings=fr.face_encodings(frameRGB, facePositions)
    for (top,right,bottom,left), face_encoding in zip(facePositions, allEncodings): 
        name='Unknown'
        matches=fr.compare_faces(Encodings, face_encoding)
        if True in matches:
            first_match_index=matches.index(True)
            name=Names[first_match_index]
        top=top*3
        right=right*3
        bottom=bottom*3
        left=left*3
        cv.rectangle(frame, (left, top), (right, bottom), (0,0,255), 2)
        cv.putText(frame, name, (left, top-6), font, .5,(245,245,50), 1)    
    cv.imshow('img', frame)
    cv.moveWindow('img',0,0)

    if cv.waitKey(1)==ord('q'):
        break

cam.release()
cv.destroyAllWindows()