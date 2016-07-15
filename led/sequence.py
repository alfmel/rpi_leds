import threading
import time


class Sequence:
    """A class for turning LEDs on and off in a repeating sequence."""

    _gpio = None  # We do this so we can mock the object during tests

    _delay = 0.25
    _pins = []
    _sequence = []

    __thread = None

    def __init__(self, gpio):
        """ Initializes the object with the given GPIO implementation. (This is the Dependency Injection pattern which
            will facilitate testing.)
        """
        self._gpio = gpio

    def set_delay(self, delay):
        """ Set the delay between elements in the sequence in seconds (you may use decimal values for subsecond delay
            values). The smaller the delay, the faster the LED sequence will change. The bigger the value the slower the
            sequence will change.
        """
        if delay > 0:
            self._delay = delay
        else:
            raise Exception('Delay must be greater than 0')

    def set_pins(self, pins):
        """ Set the pins that are connected to LEDs on your board. This should be a list of numbers corresponding to the
            pins you are using. For example, if you have LEDs connected to GPIO pins 16, 17 and 21 you would pass
            [16, 17, 21] for the pins.
        """
        if isinstance(pins, list):
            self._pins = pins
        else:
            raise Exception('Pins must be a list')
    
    def set_sequence(self, sequence):
        """ Set the sequence of which LEDs should be turned on in order. For example, to make the pins "walk," you would
            pass the following as the sequence: [16, 17, 21]. This sequence would do the following:
            
                16  17  21
                ON  off off
                off ON  off
                off off ON
                ... repeats
            
            If you want to turn on multiple LEDs at a time, enter a list of LEDs that should be turned on instead of a
            single number. For example, [ [16, 21], 17 ] would create the following result:
            
                16  17  21
                ON  off ON
                off ON  off
                ... repeats
            """
        if isinstance(sequence, list):
            self._sequence = sequence
        else:
            raise Exception('Sequence must be a list')

    def start(self):
        """ Starts the sequence in a separate thread. To stop the sequence and turn off all the LEDs, call
            stop_sequence().
        """
        # Set all the pins to output
        for pin in self._pins:
            self._gpio.setup(pin, self._gpio.OUT)

        # Start the thread
        self.__thread = self._SequenceThread(self._gpio, self._delay, self._pins, self._sequence)
        self.__thread.start()

    def stop(self):
        """ Stops the sequence and turns off all LEDs. """
        # Stop the thread
        if self.__thread is not None:
            self.__thread.stop()
            self.__thread.join()
            self.__thread = None

        # Turn off all the LEDs
        for pin in self._pins:
            self._gpio.output(pin, self._gpio.LOW)

    class _SequenceThread (threading.Thread):
        """ This class is the actual thread that turns LEDs on and off. """

        _gpio = None  # We will receive our mock object in the constructor
        __delay = 0.25
        __pins = []
        __sequence = []
        __stop = False

        def __init__(self, gpio, delay, pins, sequence):
            threading.Thread.__init__(self)
            self._gpio = gpio
            self.__delay = delay
            self.__pins = pins
            self.__sequence = sequence

        def run(self):
            while not self.__stop:
                # Go through the sequence
                for element in self.__sequence:
                    # Go through the LED pins and see if they need to be turned on or off
                    for pin in self.__pins:
                        pin_state = self._gpio.LOW  # Turn off the LED
                        if isinstance(element, list):
                            if pin in element:
                                pin_state = self._gpio.HIGH
                        else:
                            if pin == element:
                                pin_state = self._gpio.HIGH

                        # Set the pin to its given state
                        self._gpio.output(pin, pin_state)

                    # Sleep for the given interval
                    time.sleep(self.__delay)

                    # Exit if sequence has been stopped
                    if self.__stop:
                        break

        def stop(self):
            self.__stop = True
