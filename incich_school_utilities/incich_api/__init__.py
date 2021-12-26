import requests
import logging
import hashlib
import time
import random
from urllib.parse import unquote_plus


class IncichStudent:

    api_url = "http://school.incich.com:9208/display-rest"

    # POST 请求(包括inch_sign)
    def post(self, url, params=None, headers=None, data=None, timeout=3):
        try:
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
            headers['User-Agent'] = "okhttp/3.12.0"

            req = requests.post(url, params=params, headers=headers, data=data, timeout=timeout)

            if req.status_code != 200:
                logging.warning("HTTP状态码" + str(req.status_code) + ": " + str(req.content.decode("utf-8")))
                time.sleep(0.5)
                self.token = self.get_token()
                return self.post(url, params=params, headers=headers, timeout=timeout)

            return req
        except Exception as e:
            logging.warning(e)
            time.sleep(0.5)
            self.token = self.get_token()
            return self.post(url, params=params, headers=headers, data=data, timeout=timeout)

    # GET 请求(包括inch_sign)
    def get(self, url, params=None, headers=None, timeout=3):
        try:
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
            headers['User-Agent'] = "okhttp/3.12.0"

            req = requests.get(url, params=params, headers=headers, timeout=timeout)

            if req.status_code != 200:
                logging.warning("HTTP状态码" + str(req.status_code) + ": " + str(req.content.decode("utf-8")))
                time.sleep(0.5)
                self.token = self.get_token()
                return self.get(url, params=params, headers=headers, timeout=timeout)

            return req
        except Exception as e:
            logging.warning(e)
            time.sleep(0.5)
            self.token = self.get_token()
            return self.get(url, params=params, headers=headers, timeout=timeout)

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
            "nickname": str(random.randint(10000, 1000000)),
            "source": "QQ"
        }).json()
        logging.info(req)

        req = self.post(self.api_url + "/ThirdLogin/saveToken.json", params={
            "unionid": self.union_id,
        }).json()
        logging.info(req)

    # 绑定学生
    def bind(self, class_id, grade_id, school_id, relation_name, phone):
        req = self.post(self.api_url + "/bindStudent/bind.json", params={
            "unionid": self.union_id,
            "name": self.student_name,
            "classid": class_id,
            "schoolid": school_id,
            "gradeid": grade_id,
            "relationname": relation_name,
            "phone": phone
        }).json()
        logging.info(req)
        return req

    # 获取邀请码信息
    def get_class_by_code(self, code):
        req = self.get(self.api_url + "/bindStudent/getClass.json", params={
            "unionid": self.union_id,
            "invitecode": code
        }).json()
        logging.info(req)
        return req

    # 获取已绑定的学生
    def get_student(self):
        logging.info("获取账号信息...")
        req = self.get(self.api_url + "/bindStudent/getBindInfo.json", params={
            "unionid": self.union_id
        }).json()
        logging.info(req)
        return req

    # 发送一条文本消息
    def send_msg(self, msg):
        if len(msg) > 800:
            self.send_msg(msg[:800])
            time.sleep(3)
            self.send_msg(msg[800:])
            return None

        logging.info("发送的消息: " + msg)

        req = self.post(self.api_url + "/message/save", params={
            "classid": self.class_id,
            "schoolid": self.school_id,
            "gradeid": self.grade_id,
            "adduser": self.union_id,
            "addusername": "IncichRobot",
            "type": 1,
            "stuname": self.student_name,
            "stuguid": self.student_guid,
            "url": "",
            "voicelen": 0,
            "msg": msg
        }).json()
        logging.info(req)
        self.msg_processed.append(req['guid'])
        return req

    # 读取所有消息
    def read_msg_all(self):
        req = self.post(self.api_url + "/getInfo/getNotice.json", params={
            "unionid": self.union_id,
            "classid": self.class_id,
            "name": self.student_name,
            "pageno": 1,
            "length": 20
        }).json()
        # logging.info(req)
        return req

    # 获取最新消息(阻塞式等待)
    def wait_new_msg(self):
        while True:
            try:
                for i in self.read_msg_all()['data']:
                    if self.student_name in i['addusername'] and i['guid'] not in self.msg_processed:
                        self.msg_processed.append(i['guid'])
                        logging.info("收到新消息: " + str(unquote_plus(i['title'])))
                        return unquote_plus(i['title'])
                time.sleep(2)
            except Exception as e:
                logging.warning("获取消息时出错: " + str(e))

    # 发送一条语音消息
    def send_sound_msg(self, input_file):
        res = requests.post('http://school.incich.com:9207/UploadImageServlet', files={
            "file": input_file
        }).json()
        logging.info(res)
        req = self.post(self.api_url + "/message/save", params={
            "classid": self.class_id,
            "schoolid": self.school_id,
            "gradeid": self.grade_id,
            "adduser": self.union_id,
            "addusername": "IncichRobot",
            "type": 2,
            "stuname": self.student_name,
            "stuguid": self.student_guid,
            "url": res['url'],
            "voicelen": 666666,
            "msg": ""
        }).json()
        logging.info(req)
        self.msg_processed.append(req['guid'])
        return req

    # 发送一条视频消息
    def send_video_msg(self, input_file):
        res = requests.post('http://school.incich.com:9207/UploadImageServlet', files={
            "file": input_file
        }).json()
        logging.info(res)
        req = self.post(self.api_url + "/message/save", params={
            "classid": self.class_id,
            "schoolid": self.school_id,
            "gradeid": self.grade_id,
            "adduser": self.union_id,
            "addusername": "IncichRobot",
            "type": 3,
            "stuname": self.student_name,
            "stuguid": self.student_guid,
            "aspectratio": 1.5,
            "url": res['url'],
            "msg": ""
        }).json()
        logging.info(req)
        self.msg_processed.append(req['guid'])
        return req

    # 发送一条图片消息
    def send_image_msg(self, input_file):
        res = requests.post('http://school.incich.com:9207/UploadImageServlet', files={
            "file": input_file
        }).json()
        logging.info(res)
        req = self.post(self.api_url + "/message/save", params={
            "classid": self.class_id,
            "schoolid": self.school_id,
            "gradeid": self.grade_id,
            "adduser": self.union_id,
            "addusername": "IncichRobot",
            "type": 4,
            "stuname": self.student_name,
            "stuguid": self.student_guid,
            "aspectratio": 1.5,
            "url": res['url'],
            "msg": ""
        }).json()
        logging.info(req)
        self.msg_processed.append(req['guid'])
        return req

    def __init__(self, union_id, student_name, invite_code):
        logging.info("正在初始化...")
        self.union_id = union_id
        self.student_name = student_name
        self.invite_code = invite_code
        self.token = ''
        self.token = self.get_token()
        self.register()
        self.stu_info = self.get_student()['data']

        # 获取邀请码信息
        code_info = self.get_class_by_code(invite_code)['data'][0]
        self.code_info = code_info
        self.school_id = code_info['schoolid']
        self.grade_id = code_info['gradeid']
        self.class_id = code_info['classid']

        for i in self.stu_info:
            if i['name'] == self.student_name:
                self.student_guid = i['guid']
                break
        else:
            logging.info("学生未绑定.正在尝试绑定.")

            # 随机生成手机号
            # 第二位数字
            second = [3, 4, 5, 7, 8][random.randint(0, 4)]

            # 第三位数字
            third = {
                3: random.randint(0, 9),
                4: [5, 7, 9][random.randint(0, 2)],
                5: [i for i in range(10) if i != 4][random.randint(0, 8)],
                7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
                8: random.randint(0, 9),
            }[second]

            # 最后八位数字
            suffix = random.randint(9999999, 100000000)

            bind_res = self.bind(self.class_id, self.grade_id, self.school_id,
                                 "IncichRobot", "1{}{}{}".format(second, third, suffix))
            if not bind_res['success']:
                raise Exception("绑定学生失败: " + str(bind_res))
            self.student_guid = bind_res['guid']

            # 绑定后刷新 stu_info
            self.stu_info = self.get_student()['data']


        logging.info("学生GUID: " + self.student_guid)

        logging.info("尝试读取所有消息...")
        all_msg = self.read_msg_all()

        self.msg_processed = []
        for i in all_msg['data']:
            if self.student_name in i['addusername']:
                self.msg_processed.append(i['guid'])
        logging.info("消息GUID: " + str(self.msg_processed))

        logging.info("尝试发送文本消息...")
        msg_res = self.send_msg("Incich School v2 API 初始化成功.")
        if not msg_res['success']:
            raise Exception("发送消息失败: " + str(msg_res))

        logging.info("初始化完成!")
