import face_recognition as fr
import cv2 as cv
print(cv.__version__)

image=fr.load_image_file('/home/es017590/Desktop/pyPro/faceRecognizer/demoImages/unknown/u3.jpg')
face_locations=fr.face_locations(image)
print(face_locations)

image=cv.cvtColor(image, cv.COLOR_RGB2BGR)

for (row1,col1,row2,col2) in face_locations:
    cv.rectangle(image, (col1,row1), (row2,row2), (0,0,255), 2)

cv.imshow('image', image)
cv.moveWindow('image', 0, 0)

if cv.waitKey(0)==ord('q'):
    cv.destroyAllWindows()