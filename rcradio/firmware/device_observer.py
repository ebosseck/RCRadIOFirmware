from threading import Thread, Lock
from time import time, sleep
from typing import List

from rcradio.firmware.rcradio_device import RCRadIODevice


class Observer(Thread):

    def __init__(self, devices=None):
        super(Observer, self).__init__()
        if devices is None:
            devices = []

        self.shouldFinish = None

        self.deviceLock = Lock()
        self.pollFrequency = 0.0 # seconds

        self.devices: List[RCRadIODevice] = devices

    def run(self) -> None:
        startTime = time()
        while not self.shouldFinish:
            with self.deviceLock:
                for device in self.devices:
                    device.pollSerial()
            sleepTime = (startTime + self.pollFrequency) - time()
            if sleepTime > 0:
                sleep(sleepTime)
            startTime = time()
