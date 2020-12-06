import threading
import time
from displaytcp import IncichConn


class IncichProtocol():

    def __init__(self, ip, port, sn):
        super().__init__()

        self.msg_list = []
        self.res_list = []

        # 连接状态
        self.connected = True

        self.ip = ip
        self.port = port
        self.sn = sn
        main_self = self
        self.conn = IncichConn(ip, port, sn)

        # 发送消息线程
        class SendThread(threading.Thread):
            def __init__(self):
                super().__init__()
                self.start()

            def run(self):
                try:
                    while True:

                        if not main_self.connected:
                            raise ConnectionError("Connection aborted.")

                        if main_self.msg_list:
                            # 有消息时发送消息
                            main_self.conn.send(main_self.msg_list.pop(0), False)
                        else:
                            # 无消息即发送心跳包
                            main_self.conn.send(main_self.sn, True)
                            # 无消息则多等待一段时间
                            time.sleep(0.8)
                        time.sleep(0.2)
                except Exception as e:
                    main_self.connected = False
                    raise e

        SendThread()

        # 接收消息线程
        class RecvThread(threading.Thread):
            def __init__(self):
                super().__init__()
                self.start()

            def run(self):
                try:
                    while True:

                        if not main_self.connected:
                            raise ConnectionError("Connection aborted.")

                        # 如果有消息就添加到 res_list
                        res = main_self.conn.fetch()
                        if res:
                            main_self.res_list.append(res)
                        else:
                            # 没有消息则多等待一段时间
                            time.sleep(0.8)
                        time.sleep(0.2)
                except Exception as e:
                    main_self.connected = False
                    raise e

        RecvThread()

    # 发送消息
    def wait_msg(self):
        if not self.connected:
            raise ConnectionError("error while connecting to the server.")

        while True:
            if self.res_list:
                return self.res_list.pop(0)
            time.sleep(0.1)

    # 接收消息
    def send_msg(self, content):
        if not self.connected:
            raise ConnectionError("error while connecting to the server.")

        self.msg_list.append(content)
