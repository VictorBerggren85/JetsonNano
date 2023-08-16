import cv2 as cv
import numpy as np

evt=-1
pnt=(0,0)
coord=[]

img=np.zeros((250, 250, 3), np.uint8)

def click(event, x, y, flag, params):
    global pnt
    global evt
    pnt=(x, y)
    evt=event
    if event==cv.EVENT_LBUTTONDOWN:
        coord.append(pnt)
    if event==cv.EVENT_RBUTTONDOWN:
        print(x, ', ', y)
        blue=frame[y, x, 0]
        green=frame[y, x, 1]
        red=frame[y, x, 2]
        print(blue, ', ', green, ',', red)
        colorString=str(blue)+','+str(green)+','+str(red)
        img[:]=[blue,green,red]
        fnt=cv.FONT_HERSHEY_PLAIN
        r=255-int(red)
        g=255-int(green)
        b=255-int(blue)
        tp=(b,g,r)
        cv.putText(img, colorString, (10, 25), fnt, 1, tp, 2)

dispW=320
dispH=240
flip=0 #Flip cam
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'


cv.namedWindow('piCam')
cv.setMouseCallback('piCam', click)

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
    font=cv.FONT_HERSHEY_PLAIN

  #  if evt==1:
    for p in coord:
        frame=cv.circle(frame, p, 1, (255, 150, 255), -1)
        newP=str(p)
        cv.putText(frame, newP, p, font, 1, (0, 255, 0))

    frame=cv.circle(frame, pnt, 5, (0, 150, 255), 1)
    myStr=str(pnt)
    cv.putText(frame, myStr, pnt, font, 1, (0, 0, 255))
    cv.imshow('piCam', frame)
    cv.imshow('myColor', img)
    cv.moveWindow('piCam', 0, 0)

    keyEvent=cv.waitKey(1)
    if keyEvent==ord('q'):
        break
    if keyEvent==ord('c'):
        coord=[]
    
cam.release()
#outVid.release()
cv.destroyAllWindows()
