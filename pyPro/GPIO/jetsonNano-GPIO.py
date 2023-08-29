import RPi.GPIO as GPIO

# # Use default board GPIO numbering.
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
readPin = 15
# outPin = ...

# # Set pin outPin to output
# GPIO.setup(outPin, GPIO.OUT)
# # Set pin outPin to active
# GPIO.output(outPin, True)

# # Set several pins at the same time
# channels = [outPin, 13, 14]
# GPIO.setup(channels, GPIO.OUT)

# # Set pin readPin to input
GPIO.setup(readPin, GPIO.IN)
button = GPIO.input(readPin)
if button == 1:
    print('Button NOT down')
elif button == 0:
    print('Button IS down')

# Release set GPIO
GPIO.cleanup()

