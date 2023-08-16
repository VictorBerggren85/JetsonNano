from threading import Thread
import time

def BigBox(col):
    while True:
        print(col, 'box open!')
        time.sleep(5)
        print(col, 'box closed!')
        time.sleep(5)

def SmallBox(col):
    while True:
        print(col, 'box open!')
        time.sleep(1)
        print(col, 'box closed!')
        time.sleep(1)

bigBoxThread=Thread(target=BigBox, args=(['red']))
smallBoxThread=Thread(target=SmallBox, args=(['black']))
smallBoxThread.daemon=True
bigBoxThread.daemon=True
bigBoxThread.start()
smallBoxThread.start()

while True:
    pass
