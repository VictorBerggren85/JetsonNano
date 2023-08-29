import jetson_inference as ji
import jetson_utils as ju
import time
import cv2 as cv
import numpy as np

timeStamp = time.time()
fpsFilter = 0
net = ji.detectNet('ssd-mobilenet-v2', ['--model=/home/es017590/Downloads/jetson-inference/python/training/classification/myModel/resnet18.onnx', '--input_blob=input_0', '--output_blob=output_0', '--labels=/home/es017590/Downloads/jetson-inference/myTrainingData/labels.txt'])
dispW = 320
dispH = 240
flip = 2
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
# cam = ju.gstCamera(dispW, dispH, '0')
# cam = ju.gstCamera(dispW, dispH, '/dev/video1')
cam = cv.VideoCapture(camSet)
# disp = ju.glDisplay()
# cam = cv.VideoCapture(1)        
# cam.set(cv.CAP_PROP_FRAME_WIDTH, dispW)
# cam.set(cv.CAP_PROP_FRAME_HEIGHT, dispH)
font = cv.FONT_HERSHEY_COMPLEX

while True:  # disp.IsOpen():
    # img, width, height = cam.CaptureRGBA()
    _, img = cam.read()
    height = img.shape[0]
    width = img.shape[1]
    frame = cv.cvtColor(img, cv.COLOR_BGR2RGBA).astype(np.float32)
    frame = ju.cudaFromNumpy(frame)
    detections = net.Detect(frame, width, height)
    for detect in detections:
        id = detect.ClassID
        item = net.GetClassDesc(id)
        top = int(detect.Top)
        left = int(detect.Left)
        bottom = int(detect.Bottom)
        right = int(detect.Right)
        cv.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
        cv.putText(img, item, (left, top+10), font, .5, (255, 255, 255), 1)
        print(item)
    if detections == []:
        print('nothing found...')
    # disp.RenderOnce(img, width, height)
    dt = time.time() - timeStamp
    timeStamp = time.time()
    fps = 1 / dt
    fpsFilter = fpsFilter * .95 + fps * .05
    # print(str(round(fpsFilter, 2))+'fps')
    cv.putText(img, str(round(fpsFilter, 1))+'fps', (0, 30), font, 1, (0, 0, 255), 1)
    cv.imshow('image', img)
    cv.moveWindow('image', 0, 0)
    if cv.waitKey(1) == ord('q'):
        break
cam.release()
cv.destroyAllWindows()
