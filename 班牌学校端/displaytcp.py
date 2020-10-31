from sock import IncichSock
import logging
import json
import time

# 一些固定的常量
packet_header = "4e4d2500000001000001ffffffffffffffff"
packet_sep = "1b00000000"
packet_end = "00"


class IncichConn:

    def __init__(self, ip, port, sn):
        self.sn = sn
        self.packet_time_start = None

        sock = IncichSock(ip, port)
        sock.send(packet_header + "23333333333333" + packet_sep + sn.encode("ascii").hex() + packet_end)
        data = sock.recv()
        if data[:36] == packet_header:
            logging.info("handshake ok!")

            self.packet_time_start = int(data[36:][:14], 16) - int(time.time())
            logging.debug("server time got: " + str(self.packet_time_start))
        else:
            raise ConnectionError("error while handshake.")
        self.sock = sock

    def get_packet_time(self):
        return str(hex(self.packet_time_start + int(time.time())))[2:]

    def fetch(self):
        self.sock.send(packet_header + self.get_packet_time() + packet_sep + self.sn.encode("ascii").hex() + packet_end)
        data = self.sock.recv()

        # 更新服务器时间
        # 此处服务器时间不是 unix 时间戳, 而是16进制表示的日期 + 小时分钟
        # 可是年份上的编码规则还没有猜出来
        # 干脆就用直接从服务器获取, 然后修正的方法好了
        server_time = int(data[36:][:14], 16) - int(time.time())
        if server_time - self.packet_time_start > 5:
            logging.debug("server time update: " + str(server_time))
            self.packet_time_start = server_time

        res = data[60:]

        # 如果没有返回 sn 码, 就是有数据返回, 数据是 json 格式的.
        if res[:24] != self.sn.encode("ascii").hex():
            logging.info("data got.")
            data = res[:24][:-2]
            data = json.loads(data.decode("utf-8"))
            logging.info("json read ok: " + str(data))
        else:
            logging.debug("nothing.")
