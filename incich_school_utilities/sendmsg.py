# 可供第三方程序回调直接发送消息
import json
from incich_api import IncichStudent
import sys
import logging

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.CRITICAL)

config = json.load(open("config.json", "r"))
stu = IncichStudent(config['unionid'], config['name'], config['code'])

msg_body = sys.argv[1]
print(stu.send_msg(msg_body))
