import cv2 as cv

camName='nanoCam'
titleH=25
dispW=320
dispH=240
flip=0 #Flip cam
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

#launch camera
cam=cv.VideoCapture(camSet)    ## RpiCamera
#cam=cv.VideoCapture(1)        ## USBCamera

while True:
    ret, frame=cam.read()
    cv.imshow(camName, frame)
    cv.moveWindow(camName, 0, 0)

    gray=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('greyScale', gray)
    cv.moveWindow('greyScale', 0, dispH+titleH*2)

    gray2=cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    cv.imshow('RGB', gray2)
    cv.moveWindow('RGB', 0, (dispH*2)+titleH*3)

    gray3=cv.cvtColor(frame, cv.COLOR_BGR2LUV)
    cv.imshow('LUV', gray3)
    cv.moveWindow('LUV', 0, (dispH*3)+titleH*4)

    if cv.waitKey(1)==ord('q'):
        break
        
cam.release()
cv.destroyAllWindows()
