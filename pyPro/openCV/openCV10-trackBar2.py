import cv2 as cv

dispW=320
dispH=240
flip=0 #Flip cam
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cv.namedWindow('piCam')

def nothing(x):
    pass

cv.createTrackbar('xVal', 'piCam', 0, dispW, nothing)
cv.createTrackbar('yVal', 'piCam', 0, dispH, nothing)
cv.createTrackbar('xSize', 'piCam', 0, 150, nothing)
cv.createTrackbar('ySize', 'piCam', 0, 100, nothing)

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

    xVal=cv.getTrackbarPos('xVal', 'piCam')
    yVal=cv.getTrackbarPos('yVal', 'piCam')
    xSize=cv.getTrackbarPos('xSize', 'piCam')
    ySize=cv.getTrackbarPos('ySize', 'piCam')

    cv.rectangle(frame, (xVal, yVal), (xVal+xSize, yVal+ySize), (225, 150, 175), 2)

    cv.imshow('piCam', frame)
    cv.moveWindow('piCam', 0, 0)

    keyEvent=cv.waitKey(1)
    if keyEvent==ord('q'):
        break

    
cam.release()
#outVid.release()
cv.destroyAllWindows()
