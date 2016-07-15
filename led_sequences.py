#!/usr/bin/env python

import RPi.GPIO as GPIO

from collections import OrderedDict
from led.sequence import Sequence

# Define the delay between changes
delay = 0.25  # 1/4 of a second

# Define pins by color
red = 21
green = 20
yellow = 16
blue = 12

# Define different sequences
sequences = OrderedDict([
    ("simple", [red, green, yellow, blue]),
    ("back and forth", [red, green, yellow, blue, yellow, green]),
    ("walking", [[red, yellow], [green, blue]]),
    ("walking in 2", [red, [red, green], [green, yellow], [yellow, blue], blue, []]),
    ("walking in 3", [red, [red, green], [red, green, yellow], [green, yellow, blue], [yellow, blue], blue, []]),
    ("grow and shrink", [red, [red, green], [red, green, yellow], [red, green, yellow, blue], [red, green, yellow],
                         [red, green], red, []])
])

# Set up the Sequence object
GPIO.setmode(GPIO.BCM)
sequence = Sequence(GPIO)  # Dependency injection; we must pass the GPIO module
sequence.set_delay(delay)
sequence.set_pins([red, green, yellow, blue])

try:
    # Run through each sequence
    for seq_name in sequences:
        sequence.set_sequence(sequences[seq_name])
        sequence.start()
        input("Running {} sequence. Press Enter to go to the next sequence ...".format(seq_name))
        sequence.stop()
except KeyboardInterrupt:
    sequence.stop()

# Clean-up the GPIO module and exit
GPIO.cleanup()
