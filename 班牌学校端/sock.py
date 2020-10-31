import socket
import logging


class IncichSock:

    def __init__(self, ip, port):
        sock = socket.socket()
        sock.connect((ip, port))
        sock.settimeout(10)
        self.sock = sock

    def disconnect(self):
        self.sock.close()

    def send(self, data):
        logging.debug("SEND: " + data)
        self.sock.send(bytes.fromhex(data))

    def recv(self):
        res = self.sock.recv(409600).hex()
        logging.debug("RECV: " + res)
        return res
