#!/usr/bin/env python

import RPi.GPIO as GPIO

from led.sequence import Sequence

# Define the delays between changes for each sequence
delay_a = 0.75  # 3/4 of a second
delay_b = 0.1  # 1/10 of a second

# Define pins by color
red = 21
green = 20
yellow = 16
blue = 12

# Create two sequences
seq_a = [yellow, [yellow, blue], blue, []]
seq_b = [red, green]

# Instantiate the Sequence objects
GPIO.setmode(GPIO.BCM)

sequence_a = Sequence(GPIO)  # Dependency injection; we must pass the GPIO module
sequence_a.set_delay(delay_a)
sequence_a.set_pins([yellow, blue])
sequence_a.set_sequence(seq_a)

sequence_b = Sequence(GPIO)  # Dependency injection; we must pass the GPIO module
sequence_b.set_delay(delay_b)
sequence_b.set_pins([red, green])
sequence_b.set_sequence(seq_b)

try:
    # Run both sequences
    sequence_a.start()
    sequence_b.start()
    input("Running sequences A and B simultaneously. Press Enter to go exit ...")

    sequence_a.stop()
    sequence_b.stop()
except KeyboardInterrupt:
    sequence_a.stop()
    sequence_b.stop()

# Clean-up the GPIO module and exit
GPIO.cleanup()
