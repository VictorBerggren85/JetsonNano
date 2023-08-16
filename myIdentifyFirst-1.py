import jetson_inference
import jetson_utils

dispW=320
dispH=240
flip=0 #Flip cam
net=jetson_inference.detectNet('ssd-mobilenet-v2',threshold=.5)

#launch camera
## RpiCamera
#cam=jetson_utils.gstCamera(0)

## USBCamera
cam=jetson_utils.gstCamera(dispW,dispH,'dev/video1')

disp=jetson_utils.glDisplay()
font=jetson_utils.cudaFont()

while disp.IsOpen():
    frame,width,height=cam.CaptureRGBA()
    classID,confident=net.Classify(frame,width,height)
    item=net.GetClassDesc(classID)
    font.OverlayText(frame,width,height,item,5,5,font.Magenta,font.Blue)
    disp.RenderOnce(frame,width,height)