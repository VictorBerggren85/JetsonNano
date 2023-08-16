import face_recognition as fr
import cv2 as cv
import os

Encodings=[]
Names=[]
j=0

#Learning
image_dir='/home/es017590/Desktop/pyPro/faceRecognizer/demoImages/known'
for root, dirs, imgs in os.walk(image_dir):
    for img in imgs:
        path=os.path.join(root,img)
        name=os.path.splitext(img)[0]
        face=fr.load_image_file(path)
        Encodings.append(fr.face_encodings((face))[0])
        Names.append(name)
        print("Learned what " + name + " looks like!")
print('Training DONE!')
#Load Test img
font=cv.FONT_HERSHEY_SIMPLEX

image_dir='/home/es017590/Desktop/pyPro/faceRecognizer/demoImages/unknown'
for root, dirs, imgs in os.walk(image_dir):
    for img in imgs:
        testImagePath=os.path.join(root,img)
        testImg=fr.load_image_file(testImagePath)
        facePositions=fr.face_locations(testImg)
        allEncodings=fr.face_encodings(testImg,facePositions)
        testImg=cv.cvtColor(testImg, cv.COLOR_RGB2BGR)

        for (top,right,bottom,left), face_encoding in zip(facePositions, allEncodings):
            name='Unknown'
            matches=fr.compare_faces(Encodings, face_encoding)
            if True in matches:
                first_match_index=matches.index(True)
                name=Names[first_match_index]
                print('Match found: '+name)
            cv.rectangle(testImg, (left, top), (right, bottom), (0,0,255), 2)
            cv.putText(testImg, name, (left, top-6), font, 1, (255, 255, 255), 2)

        cv.imshow('img', testImg)
        cv.moveWindow('img', 0, 0)

        if cv.waitKey(0)==ord('q'):
            cv.destroyAllWindows()
