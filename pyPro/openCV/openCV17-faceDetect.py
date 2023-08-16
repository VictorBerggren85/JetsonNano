import cv2 as cv

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

face_cascade=cv.CascadeClassifier('/home/es017590/Desktop/pyPro/cascade/haarcascade_frontalface_default.xml')
eye_cascade=cv.CascadeClassifier('/home/es017590/Desktop/pyPro/cascade/haarcascade_eye.xml')

while True:
    ret, frame=cam.read()

    gray=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray, 1.3,5)
    eyes=eye_cascade.detectMultiScale(gray, 1.3,5)

    for x,y,w,h in faces:
        cv.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
    for x,y,w,h in eyes:
        cv.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

    cv.imshow('piCam', frame)
    if cv.waitKey(1)==ord('q'):
        break
cam.release()
cv.destroyAllWindows()