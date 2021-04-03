from sock import IncichSock
import logging
import json
import time
import struct

# 一些固定的常量
packet_start = "4e4d"
packet_sep_1 = "01000001ffffffffffffffff"
packet_sep_2_heartbeat = "1b00000000"
packet_sep_2_data = "0100000000"
packet_end = "00"


# 获取包的长度标识
def get_packet_len(content):
    return hex(struct.unpack('<L', struct.pack('>L', len(bytes.fromhex(content))))[0])[2:]


# 获取时间
def get_packet_time():
    buf = ""
    t = time.localtime()
    buf += hex(struct.unpack('<H', struct.pack('>H', t.tm_year))[0])[2:]
    buf += struct.pack('>B', t.tm_mon).hex()
    buf += struct.pack('>B', t.tm_mday).hex()
    buf += struct.pack('>B', t.tm_hour).hex()
    buf += struct.pack('>B', t.tm_min).hex()
    buf += struct.pack('>B', t.tm_sec).hex()
    return buf


class IncichConn:

    def __init__(self, ip, port, sn, debug_output):
        self.sn = sn
        self.packet_time_start = None

        if debug_output:
            self.debug_f = open(sn + "_" + str(round(time.time())) + "_stream", "w")
        else:
            self.debug_f = None

        sock = IncichSock(ip, port)

        sock.send(packet_start + "25000000" + packet_sep_1 + get_packet_time() + packet_sep_2_heartbeat + sn.encode("ascii").hex() + packet_end, self.debug_f)
        data = sock.recv(self.debug_f)
        if data[:36] == "4e4d2500000001000001ffffffffffffffff":
            logging.info("handshake ok!")
            # self.packet_time_start = int(data[36:][:14], 16) - int(time.time())
            # logging.debug("server time got: " + str(self.packet_time_start))
        else:
            raise ConnectionError("error while handshake. unexpected behaviour.")
        self.sock = sock

    # def get_packet_time(self):
    #     return str(hex(self.packet_time_start + int(time.time())))[2:]

    def fetch(self):

        data = self.sock.recv(self.debug_f)
        #
        # # 更新服务器时间
        # # 此处服务器时间不是 unix 时间戳, 而是16进制表示的日期 + 小时分钟
        # # 可是年份上的编码规则还没有猜出来
        # # 干脆就用直接从服务器获取, 然后修正的方法好了
        #
        # # update: 后来猜出来了 年份是用小端储存的 故修改一下
        # server_time = int(data[36:][:14], 16) - int(time.time())
        # if server_time - self.packet_time_start > 5:
        #     logging.debug("server time update: " + str(server_time))
        #     self.packet_time_start = server_time

        res = data[60:]

        # 如果没有返回 sn 码, 就是有数据返回, 数据是 json 格式的.
        if res[:24] != self.sn.encode("ascii").hex():
            logging.info("data got.")
            data = json.loads(bytes.fromhex(res[:-2]))
            logging.info("json read ok: " + str(data))
            return data
        else:
            logging.debug("nothing.")
            return None

    def send(self, content, heartbeat):

        # 心跳包和数据包有不同的标识符
        if heartbeat:
            sep_2 = packet_sep_2_heartbeat
        else:
            sep_2 = packet_sep_2_data

        packet_body = packet_sep_1 + get_packet_time() + sep_2 + content.encode("utf-8").hex() + packet_end
        self.sock.send(packet_start + get_packet_len(packet_body) + packet_body, self.debug_f)
