from typing import Callable, Optional

import serial

from rcradio.structs.ringbuffer import RingBuffer


class RCRadIODevice:

    def __init__(self, port: str = '/dev/ttyUSB0'):
        self.ser = serial.Serial(port)

        self._senderBuffer = RingBuffer()
        self._volumeBuffer = RingBuffer()
        self._brightnessBuffer = RingBuffer()

        self.bluetoothButtonState = 0
        self.tmhRotaryState = 0
        self.front1ButtonState = 0
        self.front2ButtonState = 0
        self.front3ButtonState = 0
        self.front4ButtonState = 0
        self.front5ButtonState = 0
        self.front6ButtonState = 0

        self.senderRotaryState = 0
        self.volumeRotaryState = 0
        self.brightnessRotaryState = 0

        self.bluetoothButtonStateCB = None
        self.tmhRotaryStateCB = None
        self.front1ButtonStateCB = None
        self.front2ButtonStateCB = None
        self.front3ButtonStateCB = None
        self.front4ButtonStateCB = None
        self.front5ButtonStateCB = None
        self.front6ButtonStateCB = None

        self.senderRotaryStateCB = None
        self.volumeRotaryStateCB = None
        self.brightnessRotaryStateCB = None

        self.ser.readline()

    def close(self):
        self.ser.close()

    def pollSerial(self):
        line = self.ser.readline()
        elements = line.strip().split(b',')
        values = []
        for element in elements:
            values.append(int(element))

        self.updateControlStates(*values)

    def updateState(self, oldVal, newVal, callback: Optional[Callable[[int], None]]) -> int:
        if oldVal != newVal:
            if callback is not None:
                callback(newVal)
        return newVal

    def updateControlStates(self, bluetooth_button, tmh_rotary,
                              frnt1_button, frnt2_button, frnt3_button, frnt4_button, frnt5_button, frnt6_button,
                              sndr_rotary, volume_rotary, brightnes_rotary):

        self._senderBuffer.putValue(sndr_rotary)
        self._volumeBuffer.putValue(volume_rotary)
        self._brightnessBuffer.putValue(brightnes_rotary)

        self.bluetoothButtonState = self.updateState(self.bluetoothButtonState, bluetooth_button, self.bluetoothButtonStateCB)
        self.tmhRotaryState = self.updateState(self.tmhRotaryState, tmh_rotary, self.tmhRotaryStateCB)

        self.front1ButtonState = self.updateState(self.front1ButtonState, frnt1_button, self.front1ButtonStateCB)
        self.front2ButtonState = self.updateState(self.front2ButtonState, frnt2_button, self.front2ButtonStateCB)
        self.front3ButtonState = self.updateState(self.front3ButtonState, frnt3_button, self.front3ButtonStateCB)
        self.front4ButtonState = self.updateState(self.front4ButtonState, frnt4_button, self.front4ButtonStateCB)
        self.front5ButtonState = self.updateState(self.front5ButtonState, frnt5_button, self.front5ButtonStateCB)
        self.front6ButtonState = self.updateState(self.front6ButtonState, frnt6_button, self.front6ButtonStateCB)

        self.senderRotaryState = self.updateState(self.senderRotaryState, round(self._senderBuffer.getAverage()) >> 2,
                                                  self.senderRotaryStateCB)
        self.volumeRotaryState = self.updateState(self.volumeRotaryState, round(self._volumeBuffer.getAverage()) >> 2,
                                                  self.volumeRotaryStateCB)
        self.brightnessRotaryState = self.updateState(self.brightnessRotaryState,
                                                      round(self._brightnessBuffer.getAverage()) >> 2,
                                                      self.brightnessRotaryStateCB)
