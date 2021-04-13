from incich_api import IncichStudent
from api.netease_music_api import query_song, get_163_music
from api.wiki_api import wiki_search
from api.text_html import get_http_text
import time
import os
from easyprocess import EasyProcess
import ffmpy
import random
import json
import logging

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO)

# 命令格式: 方法, 对应指令, 说明
commands = []


def handle(msg, student):

    if msg == 'help':
        res = ''
        for i in commands:
            res += i[1] + " - " + i[2] + "\n"
        student.send_msg(res)
        return

    for i in commands:
        if msg[:len(i[1])] == i[1]:
            i[0](msg, student)
            break
    else:
        student.send_msg("未知的命令: " + msg + " 请输入Help获取更多信息.")

music_vol = 256

def music(msg, student):
    if msg[:13] == 'music search ':
        res = query_song(msg[13:])
        student.send_msg(res)
        return

    if msg[:10] == 'music get ':
        try:
            student.send_msg("正在下载...")
            get_163_music(msg[10:], msg[10:] + ".mp3")
            if music_vol == 256:
                student.send_msg("正在上传...")
                f = open(msg[10:] + ".mp3", "rb")
                student.send_sound_msg(f)
                f.close()
            else:
                student.send_msg("正在更改音量...")
                ff = ffmpy.FFmpeg(
                    inputs={msg[10:] + ".mp3": None},
                    outputs={msg[10:] + "_vol.mp3": "-vol " + str(music_vol)}
                )
                ff.run()
                student.send_msg("正在上传...")
                f = open(msg[10:] + "_vol.mp3", "rb")
                student.send_sound_msg(f)
                f.close()
                os.remove(msg[10:] + "_vol.mp3")
            os.remove(msg[10:] + ".mp3")
            return
        except Exception as e:
            try:
                os.remove(msg[10:] + ".mp3")
            except Exception as e1:
                pass
            raise e

    if msg[:10] == 'music vol ':
        music_vol = int(msg[10:])
        student.send_msg("音量已更改为：" + str(music_vol) + ' (' + str(round(music_vol/2.56)) + '%)')
        return
    raise Exception("未知的子命令.")


def status(msg, student):
    res = "服务器正在正常运行.\n"
    res += "Token:" + stu.token + "\n"
    res += "邀请码信息: " + str(stu.code_info) + "\n"
    res += "绑定学生信息: " + str(stu.stu_info) + "\n"
    res += "已经处理的消息: " + str(stu.msg_processed) + "\n"
    student.send_msg(res)


def search(msg, student):
    student.send_msg("正在搜索...")
    res = wiki_search(msg[msg.find(" ") + 1:])
    student.send_msg("搜索完成! 以下是搜索结果.")
    time.sleep(1)
    student.send_msg(res)


def sendmsg(msg, student):
    msg = msg.split(" ")
    to_code = msg[1]
    to_stu_name = msg[2]
    msg_body = " ".join(msg[3:])
    res = "正在尝试发送消息...\n"

    random_uid = str(hex(random.randint(int("11111111111111111111111111111111", 16), int("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF", 16))))[2:].upper()
    res += "随机Union ID: " + random_uid + "\n"

    to_stu = IncichStudent(random_uid, to_stu_name, to_code)
    res += "邀请码信息: " + str(to_stu.code_info) + "\n"
    res += "绑定学生信息: " + str(to_stu.stu_info) + "\n"
    res += "发送消息Response: " + str(to_stu.send_msg(msg_body))

    student.send_msg(res)


def wget(msg, student):
    student.send_msg("网页内容开始>>>\n" + get_http_text(msg[5:]) + "\n<<<网页内容结束")


def shell_access(msg, student):
    global config

    if not config["shell_enabled"]:
        student.send_msg("默认情况下 shell 访问没有启用. 请到 config.json 启用 shell 访问并修改超时时间.")
        return

    start_t = time.time()
    res = "指令执行返回如下>>>\n"

    shell_command = msg[6:]
    process = EasyProcess(shell_command).call(timeout=config["shell_timeout"])

    end_t = time.time()

    res += "指令运行时间: " + str(end_t - start_t) + "\n"
    res += "指令执行超时: " + str(process.timeout_happened) + "\n"
    res += "指令执行返回值: " + str(process.return_code) + "\n"
    res += "标准输出: " + process.stdout + "\n"
    res += "标准错误输出: " + process.stderr + "\n"

    student.send_msg(res)


commands.append([status, "status", "查询服务器状态"])
commands.append([search, "search", "百度百科搜索 用法: search <关键字>"])
commands.append([music, "music", "网易云音乐 子命令: music search <音乐名> / get <音乐ID> / vol <音量数值>"])
commands.append([sendmsg, "sendmsg", "给指定的学生发送消息 用法: sendmsg <邀请码> <姓名> <消息内容>"])
commands.append([wget, "wget", "以纯文本的方式浏览网站 用法: wget <网址>"])
commands.append([shell_access, "shell", "在运行 Incich School Utilities 的服务器上执行 shell 命令 用法: shell <命令>"])


config = json.loads("{}")

try:
    config = json.load(open("config.json", "r"))
except Exception as e:
    print("读取配置文件时出错: " + str(e))
    print("尝试注册新账号...")
    code = input("请输入你的邀请码(班主任提供, 也可由 get_code.py 获取): ")
    name = input("请输入你的真实姓名: ")
    config['name'] = name
    config['code'] = code
    config['unionid'] = str(hex(random.randint(int("11111111111111111111111111111111", 16), int("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF", 16))))[2:].upper()
    config['shell_enabled'] = False
    config['shell_timeout'] = 30
    json.dump(config, open("config.json", "w"))


stu = IncichStudent(config['unionid'], config['name'], config['code'])
time.sleep(2)
stu.send_msg("Incich School Utilities v2 启动成功. 输入Help以查询更多信息.")


while True:
    print("获取消息...")
    try:
        handle(stu.wait_new_msg().lower(), stu)
    except Exception as e:
        print(e)
        stu.send_msg("服务器内部错误: " + str(e))
        time.sleep(5)
