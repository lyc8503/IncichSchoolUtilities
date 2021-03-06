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
        self.sock.sendall(bytes.fromhex(data))

    def recv(self):

        # 读取包头获得包长度
        header = ""
        while len(header) < 12:
            tmp = self.sock.recv(1)
            if tmp.hex() == "":
                raise Exception("Server returned an empty response. (Connection closed?)")
            header += tmp.hex()
        # 包长度
        pack_len = struct.unpack('<L', bytes.fromhex(header[4:]))[0]
        body = self.sock.recv(pack_len).hex()

        content = header + body
        logging.debug("RECV: " + content)
        return content
