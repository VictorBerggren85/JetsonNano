import cv2 as cv

dispW=320
dispH=240
flip=0 #Flip cam
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
goLag=0

def clickNDrag(event, x, y, flag, params):
    global x1, x2, y1, y2
    global goLag
    if (event==cv.EVENT_LBUTTONDOWN):
        x1=x
        y1=y
        goLag=0
        print('click')

    if (event==cv.EVENT_LBUTTONUP):
        x2=x
        y2=y
        goLag=1
        print('release')

cv.namedWindow('piCam')
cv.setMouseCallback('piCam', clickNDrag)

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

    if goLag==1:
        frame=cv.rectangle(frame, (x1, y1), (x2, y2), (200, 150, 50), 2)
        box=frame[y1:y2, x1:x2]
        cv.imshow('Box', box)
        cv.moveWindow('Box', dispW+5, 25)

    cv.imshow('piCam', frame)
    cv.moveWindow('piCam', 0, 0)

    if cv.waitKey(1)==ord('q'):
        break

cam.release()
#outVid.release()
cv.destroyAllWindows()
