from displaytcp import IncichConn
import logging
import time

server_ip = "47.100.170.31"
server_port = 9209
device_sn = "38a28c6c4c60"

logging.basicConfig(level=logging.DEBUG,
                    format=
                    '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

logging.info("connecting to server " + server_ip + ":" + str(server_port) + " with sn " + device_sn)

conn = IncichConn(server_ip, server_port, device_sn)

while True:
    conn.fetch()
    time.sleep(0.1)
