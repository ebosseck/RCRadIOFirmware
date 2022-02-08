from threading import Thread, Lock
import socket
from typing import Optional



class TCPClient(Thread):

    def __init__(self, address="127.0.0.1", port=4300):
        super().__init__()

        self.address = address
        self.port = port

        self.sock = None
        self.timeout: Optional[float] = None
        self.running = False

        self.sendLock = Lock()

    def __str__(self):
        return "TCP Client connected to {}:{}".format(self.address, str(self.port))

    def setTimeout(self, timeout: Optional[float]):
        self.timeout = timeout
        if self.sock is not None:
            self.sock.settimeout(timeout)

    def requestStop(self):
        self.running = False

    def run(self) -> None:
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)

        self.sock.connect((self.address, self.port))
        try:
            while self.running:
                try:
                    data = bytearray()
                    while len(data) < 2:
                        data += self.sock.recv(2 - len(data))
                    self.onMessageRecv(data)
                except:
                    pass

        except ConnectionAbortedError:
            pass # Socket closed by another thread
        finally:
            self.sock.close()

    def onMessageRecv(self, message: bytes):
        pass

    def sendMessage(self, message: bytes):
        if self.sock is not None:
            self.sendLock.acquire()
            try:
                self.sock.sendall(message)
            finally:
                self.sendLock.release()

    def closeConnection(self):
        self.sock.close()
