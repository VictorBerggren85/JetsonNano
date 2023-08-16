import face_recognition as fr
import cv2 as cv

donFace=fr.load_image_file('/home/es017590/Desktop/pyPro/faceRecognizer/demoImages/known/Donald Trump.jpg')
donEncode=fr.face_encodings(donFace)[0]

nanFace=fr.load_image_file('/home/es017590/Desktop/pyPro/faceRecognizer/demoImages/known/Nancy Pelosi.jpg')
nanEncode=fr.face_encodings(nanFace)[0]

mikeFace=fr.load_image_file('/home/es017590/Desktop/pyPro/faceRecognizer/demoImages/known/Mike Pence.jpg')
mikeEncode=fr.face_encodings(mikeFace)[0]

AnthonyFace=fr.load_image_file('/home/es017590/Desktop/pyPro/faceRecognizer/demoImages/known/Anthony Fauci.jpg')
AnthonyEncode=fr.face_encodings(AnthonyFace)[0]

BillFace=fr.load_image_file('/home/es017590/Desktop/pyPro/faceRecognizer/demoImages/known/Bill Barr.jpg')
BillEncode=fr.face_encodings(BillFace)[0]

HestonFace=fr.load_image_file('/home/es017590/Desktop/pyPro/faceRecognizer/demoImages/known/Charleton Heston.jpg')
HestonEncode=fr.face_encodings(HestonFace)[0]

Encodings=[donEncode, nanEncode, mikeEncode, AnthonyEncode, BillEncode, HestonEncode]
Names=['Trump', 'Pelosi', 'Pence', 'Fauci', 'Barr', 'Heston']

font=cv.FONT_HERSHEY_SIMPLEX
testImage=fr.load_image_file('/home/es017590/Desktop/pyPro/faceRecognizer/demoImages/unknown/u11.jpg')
facePositions=fr.face_locations(testImage)
allEncodings=fr.face_encodings(testImage, facePositions)
testImg=cv.cvtColor(testImage, cv.COLOR_RGB2BGR)

for (top,right,bottom,left), face_encoding in zip(facePositions,allEncodings):
    name='unknown person'
    matches=fr.compare_faces(Encodings, face_encoding)
    if True in matches:
        firs_match_index=matches.index(True)
        name=Names[firs_match_index]
    cv.rectangle(testImage, (left,top), (right,bottom), (0,0,255), 2)
    cv.putText(testImage, name, (left, top-6), font, 1, (255,255,255), 2)

cv.imshow('image', testImage)
cv.moveWindow('image', 0, 0)

if cv.waitKey(0)==ord('q'):
    cv.destroyAllWindows()

