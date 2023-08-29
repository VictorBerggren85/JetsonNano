# Requires internet connection!!
import os 
from gtts import gTTS

text = 'this is a test'
output = gTTS(text=text, lang='en', slow=False)
output.save('talk.mp3')
os.system('mpg123 talk.mp3')