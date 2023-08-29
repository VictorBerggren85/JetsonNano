import pyttsx3 as tts
import jetson_inference as ji
import jetson_utils as ju
import time
from threading import Thread


class Talk:
    def __init__(self, e):
        self.engine = e
        self.haveStuffToSay = False
        self.run = True
        self.thread = Thread(target=self.talk, daemon=True)
        self.thread.start()

    def talk(self):
        while self.run:
            if self.haveStuffToSay:
                print('before')
                self.engine.runAndWait()
                print('after')
                self.haveStuffToSay = False

    def setStuffToSay(self, text):
        self.engine.say(text)
        self.haveStuffToSay = True


dW = 320
dH = 240
engine = tts.init()
engine.setProperty('rate', 150)
engine.setProperty('voice', 'english+m2')
voiceBox = Talk(engine)
items = {}
net = ji.imageNet('googlenet')
cam = ju.gstCamera(dW, dH, '0')
disp = ju.glDisplay()
timestamp = time.time()

while disp.IsOpen():
    frame, _, _ = cam.CaptureRGBA()
    ClassID, confidence = net.Classify(frame, dW, dH)
    if confidence >= .8:
        itemName = net.GetClassDesc(ClassID)
        if itemName not in items:
            items[itemName] = True
            voiceBox.setStuffToSay('I can see ' + itemName)
    disp.RenderOnce(frame, dW, dH)
voiceBox.run = False
