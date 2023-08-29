import RPi.GPIO as GPIO

# # Use default board GPIO numbering.
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
readPin = 15
outPin = 23
light = False
switchOld = True
# outPin = ...

# # Set pin outPin to output
GPIO.setup(outPin, GPIO.OUT)
# # Set pin outPin to active
# GPIO.output(outPin, True)

# # Set several pins at the same time
# channels = [outPin, 13, 14]
# GPIO.setup(channels, GPIO.OUT)

# # Set pin readPin to input
GPIO.setup(readPin, GPIO.IN)

while True:
    switch = GPIO.input(readPin)
    if switchOld == True and switch == 0:
        light = not light
        GPIO.output(outPin, light)
    switchOld = switch

# Release set GPIO
GPIO.cleanup()

