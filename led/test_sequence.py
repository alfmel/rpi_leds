import time
from led.sequence import Sequence
from unittest import TestCase
from unittest.mock import Mock, call


class TestSequence(TestCase):
    class _GPIOMock:  # Mock GPIO class
        HIGH = 21
        LOW = 20
        OUT = 12345
        setup = Mock(return_value=None)
        output = Mock(return_value=None)

    _sequence = None

    def setUp(self):
        self._sequence = Sequence(self._GPIOMock)
        self._GPIOMock.setup.reset_mock()
        self._GPIOMock.output.reset_mock()

    def test_sequence_single_elements(self):
        delay = 0.01
        pins = [1, 2, 3]
        sequence = [3, 2, 1]

        self._sequence.set_delay(delay)
        self._sequence.set_pins(pins)
        self._sequence.set_sequence(sequence)

        self._sequence.start()
        time.sleep(delay * len(sequence))
        self._sequence.stop()

        self._GPIOMock.setup.assert_has_calls([call(pins[0], self._GPIOMock.OUT),
                                               call(pins[1], self._GPIOMock.OUT),
                                               call(pins[2], self._GPIOMock.OUT)])
        self._GPIOMock.output.assert_has_calls([call(pins[0], self._GPIOMock.LOW),  # First sequence element
                                                call(pins[1], self._GPIOMock.LOW),
                                                call(pins[2], self._GPIOMock.HIGH),
                                                call(pins[0], self._GPIOMock.LOW),  # Second sequence element
                                                call(pins[1], self._GPIOMock.HIGH),
                                                call(pins[2], self._GPIOMock.LOW),
                                                call(pins[0], self._GPIOMock.HIGH),  # Third sequence element
                                                call(pins[1], self._GPIOMock.LOW),
                                                call(pins[2], self._GPIOMock.LOW)])

    def test_sequence_multiple_elements(self):
        delay = 0.1
        pins = [1, 2, 3]
        sequence = [[1, 3], 2]

        self._sequence.set_delay(delay)
        self._sequence.set_pins(pins)
        self._sequence.set_sequence(sequence)

        self._sequence.start()
        time.sleep(delay * len(sequence))
        self._sequence.stop()

        self._GPIOMock.setup.assert_has_calls([call(pins[0], self._GPIOMock.OUT),
                                               call(pins[1], self._GPIOMock.OUT),
                                               call(pins[2], self._GPIOMock.OUT)])
        self._GPIOMock.output.assert_has_calls([call(pins[0], self._GPIOMock.HIGH),  # First sequence element
                                                call(pins[1], self._GPIOMock.LOW),
                                                call(pins[2], self._GPIOMock.HIGH),
                                                call(pins[0], self._GPIOMock.LOW),  # Second sequence element
                                                call(pins[1], self._GPIOMock.HIGH),
                                                call(pins[2], self._GPIOMock.LOW)])

    def test_sequence_with_empty_list(self):
        delay = 0.1
        pins = [1, 2]
        sequence = [[1, 2], []]

        self._sequence.set_delay(delay)
        self._sequence.set_pins(pins)
        self._sequence.set_sequence(sequence)

        self._sequence.start()
        time.sleep(delay * len(sequence))
        self._sequence.stop()

        self._GPIOMock.setup.assert_has_calls([call(pins[0], self._GPIOMock.OUT),
                                               call(pins[1], self._GPIOMock.OUT)])
        self._GPIOMock.output.assert_has_calls([call(pins[0], self._GPIOMock.HIGH),  # First sequence element
                                                call(pins[1], self._GPIOMock.HIGH),
                                                call(pins[0], self._GPIOMock.LOW),  # Second sequence element
                                                call(pins[1], self._GPIOMock.LOW)])
