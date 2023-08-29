import cv2 as cv

width = 1280
height = 720
flip = 0
#gst-inspect-1.0  videobalance
#gst-inspect-1.0  nvarguscamerasrc
camSet = 'nvarguscamerasrc wbmode=3 !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.1 brightness=-.05 saturation=1.25 ! appsink'
cam1 = cv.VideoCapture(camSet)

while True:
    _, frame = cam1.read()
    cv.imshow('cv test', frame)
    cv.moveWindow('cv test', 0, 0)
    if cv.waitKey(1) == ord('q'):
        break
cam1.release()
cv.destroyAllWindows
