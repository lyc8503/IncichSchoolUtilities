from displayprotocol import IncichProtocol
import logging
import time

server_ip = "47.100.170.31"
server_port = 9209
device_sn = "38a28c6c4ad6"

logging.basicConfig(level=logging.DEBUG,
                    format=
                    '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

logging.info("connecting to server " + server_ip + ":" + str(server_port) + " with sn " + device_sn)

display = IncichProtocol(server_ip, server_port, device_sn)

display.send_msg('{"guid":"38a28c6c4ad6","version":"7","versionname":"3.3.2.2@产品型号：TD22-3@Launcher版本：4.1@Face：3.0@inch03"}')

while True:
    print(display.wait_msg())