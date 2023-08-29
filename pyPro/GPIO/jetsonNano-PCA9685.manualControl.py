from adafruit_servokit import ServoKit as sk
from threading import Thread
import time
import numpy as np
import json
import cv2 as cv

dW = 320
dH = 240
pHome = 90
tHome = 105

# cam = cv.VideoCapture(1)
# cam.set(cv.CAP_PROP_FRAME_WIDTH, dW)
# cam.set(cv.CAP_PROP_FRAME_HEIGHT, dH)

myKit = sk(channels=16)
servo = {}
servo['pan'] = myKit.servo[0]
servo['tilt'] = myKit.servo[1]

servo['pan'].angle = pHome
servo['tilt'].angle = tHome


def panServo(angle):
    servo['pan'].angle = angle
def tiltServo(angle):
    servo['tilt'].angle = angle


cv.namedWindow('Servo Trackbars')
cv.moveWindow('Servo Trackbars', 0, dH*2+(100))
cv.createTrackbar('pan', 'Servo Trackbars', 90, 179, panServo)
cv.createTrackbar('tilt', 'Servo Trackbars', 90, 179, tiltServo)

while True:
    # ret, frame = cam.read()

#     cv.imshow('nanoCam', frame)
#     cv.moveWindow('nanoCam', 0, 0)

    if cv.waitKey(1) == ord('q'):
        break

cv.destroyAllWindows()
# cam.release()
servoPan.angle = pHome
servoTilt.angle = tHome
