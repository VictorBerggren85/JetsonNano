import jetson_inference
import jetson_utils
import cv2 as cv
import numpy as np
import time

width = 320
height = 240
flip = 0
camSet = 'nvarguscamerasrc wbmode=3 !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.1 brightness=-.05 saturation=1.25 ! appsink drop=true'
cam1 = cv.VideoCapture(camSet)
net = jetson_inference.imageNet('googlenet')
timeStamp = time.time()
cvFont = cv.FONT_HERSHEY_COMPLEX
fpsFilter = 0

while True:
    _, frame = cam1.read()
    img = jetson_utils.cudaFromNumpy(cv.cvtColor(frame, cv.COLOR_BGR2RGBA).astype(np.float32))
    classID, confidence = net.Classify(img, width, height)
    item = net.GetClassDesc(classID)
    dt = time.time() - timeStamp
    timeStamp = time.time()
    fps = 1 / dt
    fpsFilter = fpsFilter*.95 + fps*.05

    cv.putText(frame, str(round(fpsFilter, 1)) + 'fps ' + item, (0, 30), cvFont, .5, (255, 255, 255), 1)
    cv.imshow('cv test', frame)
    cv.moveWindow('cv test', 0, 0)
    if cv.waitKey(1) == ord('q'):
        break
cam1.release()
cv.destroyAllWindows

