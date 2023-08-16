import cv2
import numpy as np
import json

print(cv2.__version__)

data={}
hueLower=0
hueUpper=0
hue2Lower=0
hue2Upper=0
satLow=0
satHigh=0
valLow=0
valHigh=0

def nothing(x):
    pass


def saveTB():
    data["hueLower"]=hueLow 
    data["hueUpper"]=hueUp
    data["hue2Lower"]=hue2Low
    data["hue2Upper"]=hue2Up
    data["satLow"]=Ls
    data["satHigh"]=Us
    data["valLow"]=Lv
    data["valHigh"]=Uv 
    with open('trackbardata.json', 'w') as f:
        json.dump(data,f,indent=4,sort_keys=False)

dispW=320
dispH=240

cv2.namedWindow('Trackbars')
cv2.moveWindow('Trackbars',4*(dispW+5),25) 

with open('trackbardata.json') as tbData:
    loaded=json.load(tbData)
    hueLower=loaded["hueLower"]
    hueUpper=loaded["hueUpper"]
    hue2Lower=loaded["hue2Lower"]
    hue2Upper=loaded["hue2Upper"]
    satLow=loaded["satLow"]
    satHigh=loaded["satHigh"]
    valLow=loaded["valLow"]
    valHigh=loaded["valHigh"]

    cv2.createTrackbar('hueLower', 'Trackbars',hueLower,179,nothing)
    cv2.createTrackbar('hueUpper', 'Trackbars',hueUpper,179,nothing)
    cv2.createTrackbar('hue2Lower', 'Trackbars',hue2Lower,179,nothing)
    cv2.createTrackbar('hue2Upper', 'Trackbars',hue2Upper,179,nothing)
    cv2.createTrackbar('satLow', 'Trackbars',satLow,255,nothing)
    cv2.createTrackbar('satHigh', 'Trackbars',satHigh,255,nothing)
    cv2.createTrackbar('valLow','Trackbars',valLow,255,nothing)
    cv2.createTrackbar('valHigh','Trackbars',valHigh,255,nothing)


#flip=2

cam=cv2.VideoCapture(1)        
cam.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)

while True:
    ret, frame = cam.read()
    #frame=cv2.imread('smarties.png')

    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    hueLow=cv2.getTrackbarPos('hueLower', 'Trackbars')
    hueUp=cv2.getTrackbarPos('hueUpper', 'Trackbars')

    hue2Low=cv2.getTrackbarPos('hue2Lower', 'Trackbars')
    hue2Up=cv2.getTrackbarPos('hue2Upper', 'Trackbars')

    Ls=cv2.getTrackbarPos('satLow', 'Trackbars')
    Us=cv2.getTrackbarPos('satHigh', 'Trackbars')

    Lv=cv2.getTrackbarPos('valLow', 'Trackbars')
    Uv=cv2.getTrackbarPos('valHigh', 'Trackbars')

    l_b=np.array([hueLow,Ls,Lv])
    u_b=np.array([hueUp,Us,Uv])

    l_b2=np.array([hue2Low,Ls,Lv])
    u_b2=np.array([hue2Up,Us,Uv])

    FGmask=cv2.inRange(hsv,l_b,u_b)
    FGmask2=cv2.inRange(hsv,l_b2,u_b2)
    FGmaskComp=cv2.add(FGmask,FGmask2)
    cv2.imshow('FGmaskComp',FGmaskComp)
    cv2.moveWindow('FGmaskComp',0,1*(dispH+25)+25)

    contours, _=cv2.findContours(FGmaskComp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours=sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    
    for cnt in contours:
        area=cv2.contourArea(cnt)
        (x,y,w,h)=cv2.boundingRect(cnt)
        if area>=50:
        #    cv2.drawContours(frame, [cnt], 0, (0,0,255),2)
        #    cv2.rectangle(frame, (x,y), (x+w, y+w), (0, 0, 255),1)
            cv2.line(frame, (x+int(w/2),0), (x+int(w/2),dispH), (0,255,0), 2)
            cv2.line(frame, (0, y+(int(h/2))), (dispW, y+(int(h/2))), (0,255,0), 2)
    

    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCam',0,0)

    if cv2.waitKey(1)==ord('q'):
        break

saveTB()        
cam.release()
cv2.destroyAllWindows()
