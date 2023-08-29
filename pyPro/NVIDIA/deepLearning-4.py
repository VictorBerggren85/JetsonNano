import jetson_inference as ji
import jetson_utils as ju
import time
# import cv2 as cv

timeStamp = time.time()
fpsFilter = 0
net = ji.detectNet('ssd-mobilenet-v2', threshold=.5)
dispW = 320
dispH = 240
# cam = ju.gstCamera(dispW, dispH, '0')
cam = ju.gstCamera(dispW, dispH, '/dev/video1')
disp = ju.glDisplay()
while disp.IsOpen():
    img, width, height = cam.CaptureRGBA()
    detections = net.Detect(img, width, height)
    disp.RenderOnce(img, width, height)
    dt = time.time() - timeStamp
    timeStamp = time.time()
    fps = 1 / dt
    fpsFilter = fpsFilter * .95 + fps * .05
    print(str(round(fpsFilter, 2))+'fps')
