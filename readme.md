# LED Experiments for the Raspberry Pi

This project allows you to play with LEDs on the Raspberry Pi. It is
written in Python and requires the installation of the RPi.GPIO library
for Python. In-depth information for this project may be found in my
[Raspberry Pi Blog](https://blogs.mypals.org/pi/). It came about during
my initial tinkering with a Raspberry Pi Zero to learn about the GPIO
pins in Python.

This project is divided into different parts, with each part building on
each other. Each part has its own branch so you may easily view the code
for each part by doing `git checkout partX`.

## Part 1

In [Part 1](https://blogs.mypals.org/pi/post/Raspberry-Pi-GPIO-Programming-Part-1)
(`git checkout part1`) I wrote a simple Python script to turn on an LED
for 10 seconds. The pin number of the output GPIO is configurable via
the `pinNumber` variable. The script also handles a keyboard interrupt
(Ctrl-C).

## Part 2

In [Part 2](https://blogs.mypals.org/pi/post/raspberry-pi-gpio-programming-part-2)
(`git checkout part2`) I wrote an LED sequence class that allows you to run an
LED sequence asynchronously. Because the class instances are fully isolated,
I can run more than one sequence at a time. And since I am no longer just
writing sequential code, I can create unit tests to test my class. Testability
is important since I can develop on my laptop, mock the GPIO library (since my
laptop doesn't have GPIO pins) and I know my code will work once I transfer it
to the Raspberry Pi.
