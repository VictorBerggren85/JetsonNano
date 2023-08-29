import os
import pyttsx3 as x3

engine = x3.init()
engine.setProperty('rate', 150)
engine.setProperty('voice', 'english+m2')
text = 'This is a test'
engine.say(text)
engine.runAndWait()