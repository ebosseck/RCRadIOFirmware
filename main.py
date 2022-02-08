from rcradio.firmware.device_observer import Observer
from rcradio.firmware.rcradio_device import RCRadIODevice
from rcradio.net.tcpclient import TCPClient

SERVER_ADDRESS = "192.168.0.235"
SERVER_PORT = 3019


CONTROL_ID_BLUETOOTH_BUTTON = 0x00
CONTROL_ID_TMH_ROTARY = 0x01

CONTROL_ID_FRONT1_BUTTON = 0x02
CONTROL_ID_FRONT2_BUTTON = 0x03
CONTROL_ID_FRONT3_BUTTON = 0x04
CONTROL_ID_FRONT4_BUTTON = 0x05
CONTROL_ID_FRONT5_BUTTON = 0x06
CONTROL_ID_FRONT6_BUTTON = 0x07

CONTROL_ID_SENDER_ROTARY = 0x08
CONTROL_ID_VOLUME_ROTARY = 0x09
CONTROL_ID_BRIGHTNESS_ROTARY = 0x0a


def generatePrintCallback(tcpClient: TCPClient, controlID: int):
    def cb (value: int) -> None:
        tcpClient.sendMessage(bytes([controlID, value&0xff]))
    return cb


def run():

    tcpClient = TCPClient(SERVER_ADDRESS, SERVER_PORT)
    tcpClient.start()
    rcRadIO = RCRadIODevice()

    rcRadIO.bluetoothButtonStateCB = generatePrintCallback(tcpClient, CONTROL_ID_BLUETOOTH_BUTTON)
    rcRadIO.tmhRotaryStateCB = generatePrintCallback(tcpClient, CONTROL_ID_TMH_ROTARY)
    rcRadIO.front1ButtonStateCB = generatePrintCallback(tcpClient, CONTROL_ID_FRONT1_BUTTON)
    rcRadIO.front2ButtonStateCB = generatePrintCallback(tcpClient, CONTROL_ID_FRONT2_BUTTON)
    rcRadIO.front3ButtonStateCB = generatePrintCallback(tcpClient, CONTROL_ID_FRONT3_BUTTON)
    rcRadIO.front4ButtonStateCB = generatePrintCallback(tcpClient, CONTROL_ID_FRONT4_BUTTON)
    rcRadIO.front5ButtonStateCB = generatePrintCallback(tcpClient, CONTROL_ID_FRONT5_BUTTON)
    rcRadIO.front6ButtonStateCB = generatePrintCallback(tcpClient, CONTROL_ID_FRONT6_BUTTON)

    rcRadIO.senderRotaryStateCB = generatePrintCallback(tcpClient, CONTROL_ID_SENDER_ROTARY)
    rcRadIO.volumeRotaryStateCB = generatePrintCallback(tcpClient, CONTROL_ID_VOLUME_ROTARY)
    rcRadIO.brightnessRotaryStateCB = generatePrintCallback(tcpClient, CONTROL_ID_BRIGHTNESS_ROTARY)

    observer = Observer([rcRadIO])
    observer.start()


if __name__ == "__main__":
    run()