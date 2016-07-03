#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

# Use Raspberry Pi pin labels
GPIO.setmode(GPIO.BCM)

# OR use Raspberry Pi board pin numbers
# GPIO.setmode(GPIO.BOARD)

# Choose the pin number you want to use
pinNumber = 21

try:
    # Set up GPIO pin as outout
    GPIO.setup(pinNumber, GPIO.OUT)

    # Turn on the LED
    print("Turning on LED...")
    GPIO.output(pinNumber, GPIO.HIGH)

    # Sleep for 10 seconds
    time.sleep(10)

    # Turn off LED
    print("Turning off LED...")
    GPIO.output(pinNumber, GPIO.LOW)
except KeyboardInterrupt:
    print("Keyboard interrupt... exiting.")

GPIO.cleanup()
