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

while True:
    ret, frame=cam.read()
    cv.imshow('piCam', frame)
    if cv.waitKey(1)==ord('q'):
        break
cam.release()
cv.destroyAllWindows()
