from incich_api import IncichStudent
from api.netease_music_api import query_song, get_163_music
from api.wiki_api import wiki_search
import time
import os
import ffmpy
import random
import json


# 命令格式: 方法, 对应指令, 说明
commands = []

def send(msg):
    global stu

    if msg[:10] == 'send test ':
        if os.path.isfile(msg[10:]):
            stu.send_msg("正在发送测试文件至班牌...")
            f = open(msg[10:], "rb")
            stu.send_test_msg(f)
            f.close()
        else:
            stu.send_msg("错误：" + msg[10:] + "不存在")
        return

    if msg[:10] == 'send view ':
        if os.path.exists(msg[10:]):
            if os.path.isfile(msg[10:]):
                stu.send_msg("错误：路径" + msg[10:] + "指向一个文件")
            else:
                for res in os.listdir(msg[10:]):
                    stu.send_msg("正在查看服务器目录：" + msg[10:])
                    stu.send_msg(res)
        else:
            stu.send_msg("错误：目录" + msg[10:] + "不存在")
        return

    if msg[:13] == 'send message ':
        stu.send_msg("正在发送消息至班牌...")
        stu.send_msg(msg[13:])
        return

    if msg[:10] == 'send text ':
        if os.path.isfile(msg[10:]):
            stu.send_msg("正在发送文本至班牌...")
            f = open(msg[10:])
            stu.send_msg(f.read())
            f.close()
        else:
            stu.send_msg("错误：文本文件" + msg[10:] + "不存在")
        return

    if msg[:11] == 'send sound ':
        if os.path.isfile(msg[11:]):
            stu.send_msg("正在发送音频至班牌...")
            f = open(msg[11:], "rb")
            stu.send_sound_msg(f)
            f.close()
        else:
            stu.send_msg("错误：音频文件" + msg[10:] + "不存在")
        return

    if msg[:11] == 'send image ':
        if os.path.isfile(msg[11:]):
            stu.send_msg("正在发送图片至班牌...")
            f = open(msg[11:], "rb")
            stu.send_image_msg(f)
            f.close()
        else:
            stu.send_msg("错误：图片文件" + msg[10:] + "不存在")
        return

    if msg[:11] == 'send video ':
        if os.path.isfile(msg[11:]):
            stu.send_msg("正在发送视频至班牌...")
            f = open(msg[11:], "rb")
            stu.send_video_msg(f)
            f.close()
        else:
            stu.send_msg("错误：视频文件" + msg[10:] + "不存在")
        return

    raise Exception("未知的子命令.")

def handle(msg):
    global stu

    if msg == 'help':
        res = ''
        for i in commands:
            res += i[1] + " - " + i[2] + "\n"
        stu.send_msg(res)
        return

    for i in commands:
        if msg[:len(i[1])] == i[1]:
            i[0](msg)
            break
    else:
        stu.send_msg("未知的命令: " + msg + " 请输入Help获取更多信息.")


music_vol = 100


def music(msg):
    global stu
    global music_vol
    if msg[:13] == 'music search ':
        res = query_song(msg[13:])
        stu.send_msg(res)
        return

    if msg[:10] == 'music get ':
        try:
            stu.send_msg("正在下载音乐至服务器...")
            get_163_music(msg[10:], msg[10:] + ".mp3")
            global music_vol
            stu.send_msg("正在发送音乐至班牌...")
            f = open(msg[10:] + ".mp3", "rb")
            stu.send_sound_msg(f)
            f.close()
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
        stu.send_msg("音量更改成功.")
        return
    raise Exception("未知的子命令.")


def status(msg):
    global stu
    res = "服务器正在正常运行.\n"
    res += "Token:" + stu.token + "\n"
    res += "邀请码信息: " + str(stu.code_info) + "\n"
    res += "绑定学生信息: " + str(stu.stu_info) + "\n"
    res += "已经处理的消息: " + str(stu.msg_processed) + "\n"
    stu.send_msg(res)
    f=os.popen("screenfetch")
    stu.send_msg(f.read())


def search(msg):
    global stu
    stu.send_msg("正在搜索...")
    res = wiki_search(msg[msg.find(" ") + 1:])
    stu.send_msg("搜索完成! 以下是搜索结果.")
    time.sleep(1)
    stu.send_msg(res)


commands.append([status, "status", "查询服务器状态"])
commands.append([search, "search", "百度百科搜索"])
commands.append([music, "music", "网易云音乐 子命令: search & get & vol"])
commands.append([send, "send", "[DEBUG] 发送文件至班牌 子命令：view & message & text & sound & image & video（正在进行测试，测试命令：test）"])

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
    json.dump(config, open("config.json", "w"))


stu = IncichStudent(config['unionid'], config['name'], config['code'])
time.sleep(2)
stu.send_msg("Incich School Utilities v3-Beta 启动成功. 输入Help以查询更多信息.")


while True:
    print("获取消息...")
    try:
        handle(stu.wait_new_msg().lower())
    except Exception as e:
        print(e)
        stu.send_msg("服务器内部错误: " + str(e))
        time.sleep(5)
