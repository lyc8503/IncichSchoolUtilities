import socket
import logging
import struct


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
        print(self.sock.send(bytes.fromhex(data)))

    def recv(self):
        header = ""
        while len(header) < 12:
            header += self.sock.recv(1).hex()
        # 包长度
        pack_len = struct.unpack('<L', bytes.fromhex(header[4:]))[0]
        body = self.sock.recv(pack_len).hex()

        content = header + body
        logging.debug("RECV: " + content)
        return content
