import cv2 as cv

dispW=320
dispH=240
flip=0 #Flip cam
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

BW=int(.10*dispW)
BH=int(.10*dispH)
BXPos=10
BYPos=10
dx=2
dy=2

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

    frame=cv.rectangle(frame, (BXPos, BYPos), (BXPos+BW, BYPos+BH), (90, 150, 90), -1)
    BXPos=BXPos+dx
    BYPos=BYPos+dy

    if BXPos+BW >= dispW or BXPos <= 0:
        dx=dx*-1
    if BYPos+BH >= dispH or BYPos <= 0:
        dy=dy*-1

    cv.imshow('piCam', frame)
    cv.moveWindow('piCam', 0, 0)

    if cv.waitKey(1)==ord('q'):
        break

cam.release()
#outVid.release()
cv.destroyAllWindows()
