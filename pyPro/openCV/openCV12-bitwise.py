import cv2 as cv
import numpy as np

dispW=320
dispH=240
flip=0 #Flip cam

img1=np.zeros((dispH, dispW, 1), np.uint8)
img1[0:dispH, 0:160]=225

img2=np.zeros((dispH, dispW, 1), np.uint8)
img2[90:130, 150:190]=255

bitAnd=cv.bitwise_and(img1, img2)
bitOr=cv.bitwise_or(img1, img2)
bitXor=cv.bitwise_xor(img1, img2)

camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cv.namedWindow('piCam')

#launch camera
## RpiCamera
cam=cv.VideoCapture(camSet)    
## RpiCamera

## USBCamera
#cam=cv.VideoCapture(1)        
#cam.set(cv.CAP_PROP_FRAME_WIDTH, dispW/2)
#cam.set(cv.CAP_PROP_FRAME_HEIGHT, dispH/2)
## USBCamera

#cam=cv.VideoCapture('videos/myCam.avi') 
#outVid=cv.VideoWriter('videos/myCam.avi', cv.VideoWriter_fourcc(*'XVID'), 21, (dispW, dispH))

while True:
    ret, frame=cam.read()

    cv.imshow('img1', img1)
    cv.moveWindow('img1', 0, dispH+50)
    cv.imshow('img2', img2)
    cv.moveWindow('img2', dispW+5, 25)  
    cv.imshow('and', bitAnd)
    cv.moveWindow('and', dispW+5, dispH+50)
    cv.imshow('or', bitOr)
    cv.moveWindow('or', 0, dispH*2+75) 
    cv.imshow('xor', bitXor)
    cv.moveWindow('xor', dispW+5, dispH*2+75)    

    frame=cv.bitwise_and(frame, frame, mask=bitXor)
    cv.imshow('piCam', frame)
    cv.moveWindow('piCam', 0, 0)

    if cv.waitKey(1)==ord('q'):
        break

cam.release()
#outVid.release()
cv.destroyAllWindows()
