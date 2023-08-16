import cv2 as cv

dispW=320
dispH=240
flip=0 #Flip cam
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

    roi=frame[50:150, 50:150]
    roiGray=cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
    roiGray=cv.cvtColor(roiGray, cv.COLOR_GRAY2BGR)
    cv.imshow('ROI', roi)
    cv.moveWindow('ROI', dispW+5, 25)
    cv.imshow('ROI Gray', roiGray)
    cv.moveWindow('ROI Gray', dispW+110, 25)
    frame[50:150, 50:150]=roiGray
    cv.imshow('piCam', frame)
    cv.moveWindow('piCam', 0, 0)

    keyEvent=cv.waitKey(1)
    if keyEvent==ord('q'):
        break

    
cam.release()
#outVid.release()
cv.destroyAllWindows()
