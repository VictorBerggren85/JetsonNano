import cv2 as cv

dispW=320
dispH=240
flip=0 #Flip cam
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

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

    #geometrics 
    frame=cv.rectangle(frame, (120, 200), (220, 120), (90, 150, 90), 2)
    frame=cv.circle(frame, (160, 120), 50, (0, 150, 255), 1)
    #text
    fnt=cv.FONT_HERSHEY_DUPLEX
    frame=cv.putText(frame, 'Test text', (150, 150), fnt, 2, (255, 255, 255), 1)
    #line
    frame=cv.line(frame, (10, 10), (310, 230), (0, 0, 0), 2)
    #Arrow
    frame=cv.arrowedLine(frame, (50, 50), (100, 100), (255, 255, 255), 2)

    cv.imshow('piCam', frame)
    cv.moveWindow('piCam', 0, 0)

    if cv.waitKey(1)==ord('q'):
        break

cam.release()
#outVid.release()
cv.destroyAllWindows()
