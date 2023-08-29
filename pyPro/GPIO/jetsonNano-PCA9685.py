from adafruit_servokit import ServoKit as sk
from threading import Thread
import time
import numpy as np
import json
import cv2 as cv

dW = 320
dH = 240

cam = cv.VideoCapture(1)
cam.set(cv.CAP_PROP_FRAME_WIDTH, dW)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, dH)

run = True
started = False
home = 90
data = {}
hueLower = 0
hueUpper = 0
hue2Lower = 0
hue2Upper = 0
satLow = 0
satHigh = 0
valLow = 0
valHigh = 0
visionCenter = (int(dW*0.5), int(dH*0.5))
targetCenter = visionCenter


def nothing(x):
    pass


def saveTB():
    data["hueLower"] = hueLow
    data["hueUpper"] = hueUp
    data["hue2Lower"] = hue2Low
    data["hue2Upper"] = hue2Up
    data["satLow"] = Ls
    data["satHigh"] = Us
    data["valLow"] = Lv
    data["valHigh"] = Uv
    with open('trackbardata.json', 'w') as f:
        json.dump(data, f, indent=4, sort_keys=False)


def targetTrackingX():
    pan = 0
    oldPan = 0
    while run:
        pan = round(180-(targetCenter[0]/(dW/180)))
        if pan != oldPan and pan > 0 and pan < 180:
            # servoPan.angle = pan
            print('pan', pan, ', targetX', targetCenter[0])
        oldPan = pan
        time.sleep(5)


def targetTrackingY():
    tilt = 0
    oldTilt = 0
    while run:
        tilt = round(180-(targetCenter[1]/(dH/180)))
        if tilt != oldTilt and tilt > 0 and tilt < 180:
            # servoTilt.angle = tilt
            print('tilt', tilt, 'targetY', targetCenter[1])
        oldTilt = tilt
        time.sleep(5)


threadTargetTrackingX = Thread(target=targetTrackingX, daemon=True)
threadTargetTrackingY = Thread(target=targetTrackingY, daemon=True)

cv.namedWindow('Trackbars')
cv.moveWindow('Trackbars', 0, dH*2+(100))

with open('trackbardata.json') as tbData:
    loaded = json.load(tbData)
    hueLower = loaded["hueLower"]
    hueUpper = loaded["hueUpper"]
    hue2Lower = loaded["hue2Lower"]
    hue2Upper = loaded["hue2Upper"]
    satLow = loaded["satLow"]
    satHigh = loaded["satHigh"]
    valLow = loaded["valLow"]
    valHigh = loaded["valHigh"]

    cv.createTrackbar('hueLower', 'Trackbars', hueLower, 179, nothing)
    cv.createTrackbar('hueUpper', 'Trackbars', hueUpper, 179, nothing)
    cv.createTrackbar('hue2Lower', 'Trackbars', hue2Lower, 179, nothing)
    cv.createTrackbar('hue2Upper', 'Trackbars', hue2Upper, 179, nothing)
    cv.createTrackbar('satLow', 'Trackbars', satLow, 255, nothing)
    cv.createTrackbar('satHigh', 'Trackbars', satHigh, 255, nothing)
    cv.createTrackbar('valLow', 'Trackbars', valLow, 255, nothing)
    cv.createTrackbar('valHigh', 'Trackbars', valHigh, 255, nothing)

ref = cv.imread(
    'color-colors-wheel-names-degrees-rgb-hsb-hsv-hue-78027630.jpg')
cv.imshow('HSV-reference', ref)
cv.moveWindow('HSV-reference', dW+5, 0)

myKit = sk(channels=16)
servoPan = myKit.servo[0]
servoTilt = myKit.servo[1]

servoPan.angle = home
servoTilt.angle = home

while True:
    ret, frame = cam.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    hueLow = cv.getTrackbarPos('hueLower', 'Trackbars')
    hueUp = cv.getTrackbarPos('hueUpper', 'Trackbars')

    hue2Low = cv.getTrackbarPos('hue2Lower', 'Trackbars')
    hue2Up = cv.getTrackbarPos('hue2Upper', 'Trackbars')

    Ls = cv.getTrackbarPos('satLow', 'Trackbars')
    Us = cv.getTrackbarPos('satHigh', 'Trackbars')

    Lv = cv.getTrackbarPos('valLow', 'Trackbars')
    Uv = cv.getTrackbarPos('valHigh', 'Trackbars')

    l_b = np.array([hueLow, Ls, Lv])
    u_b = np.array([hueUp, Us, Uv])

    l_b2 = np.array([hue2Low, Ls, Lv])
    u_b2 = np.array([hue2Up, Us, Uv])

    FGmask = cv.inRange(hsv, l_b, u_b)
    FGmask2 = cv.inRange(hsv, l_b2, u_b2)
    FGmaskComp = cv.add(FGmask, FGmask2)
    cv.imshow('FGmaskComp', FGmaskComp)
    cv.moveWindow('FGmaskComp', 0, 1*(dH+25))

    contours, _ = cv.findContours(
        FGmaskComp, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        if not started:
            threadTargetTrackingX.start()
            threadTargetTrackingY.start()
            started = True
        contours = sorted(contours,
        key=lambda x: cv.contourArea(x),
        reverse=True)
        area = cv.contourArea(contours[0])
        (x, y, w, h) = cv.boundingRect(contours[0])
        if area >= 50:
            targetCenter = ((x+int(w*0.5)), (y+int(h*0.5)))
            cv.line(
                frame,
                (x+int(w*0.5), 0),
                (x+int(w*0.5), dH),
                (0, 255, 0),
                2)
            cv.line(
                frame,
                (0, y+(int(h*0.5))),
                (dW, y+(int(h*0.5))),
                (0, 255, 0),
                2)

    cv.imshow('nanoCam', frame)
    cv.moveWindow('nanoCam', 0, 0)

    if cv.waitKey(1) == ord('q'):
        break
cv.destroyAllWindows()
cam.release()
run = False
servoTilt.angle = home
servoPan.angle = home
saveTB()
