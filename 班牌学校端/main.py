import random

from displayprotocol import IncichProtocol
import logging
import time

server_ip = "47.100.170.31"
server_port = 9209
device_sn = "38a28c6c4ad6"
# device_sn = "38a28c6c45ff"
# device_sn = "38a28c6c4000"

logging.basicConfig(level=logging.DEBUG,
                    format=
                    '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

logging.info("connecting to server " + server_ip + ":" + str(server_port) + " with sn " + device_sn)


# 如果上一次强制退出了程序而没有断开连接
# 再次连接的时候服务器可能会断开连接
# 要等待一段时间再连接

display = None
while True:
    try:
        display = IncichProtocol(server_ip, server_port, device_sn)
        break
    except Exception as e:
        logging.info("connect fail, retry: " + str(e))
        # time.sleep(random.randint(1, 3))

# 发送 json 登录
# display.send_msg('{"guid":"38a28c6c4000","version":"1","versionname":"1.0.0.0@产品型号：TD22-3@Launcher版本：1.1@Face：1.0@inch01"}')

# time.sleep(2)

while True:
    print(display.wait_msg())

