from incich_api import IncichStudent
from api.netease_music_api import query_song, get_163_music
from api.wiki_api import wiki_search
import time
import os
# import ffmpy
import random
import json


# 命令格式: 方法, 对应指令, 说明
commands = []


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
            stu.send_msg("正在下载...")
            get_163_music(msg[10:], msg[10:] + ".mp3")

            # 测试转码是否可以省略
            # stu.send_msg("正在转码...")
            # global music_vol
            # ff = ffmpy.FFmpeg(
            #     inputs={msg[10:] + ".mp3": None},
            #     outputs={msg[10:] + ".amr": "-ab 23.85k -acodec amr_wb -ac 1 -ar 16000 -vol " + str(music_vol)}
            # )
            # ff.run()

            stu.send_msg("正在上传...")
            # f = open(msg[10:] + ".amr", "rb")
            f = open(msg[10:] + ".mp3", "rb")
            stu.send_sound_msg(f)
            f.close()
            # os.remove(msg[10:] + ".amr")
            os.remove(msg[10:] + ".mp3")
            return
        except Exception as e:
            try:
                os.remove(msg[10:] + ".mp3")
                # os.remove(msg[10:] + ".amr")
            except Exception as e1:
                pass
            raise e

    if msg[:10] == 'music vol ':
        music_vol = int(msg[10:])
        # stu.send_msg("音量更改成功.")
        stu.send_msg("本命令已经弃用, 可通过班牌设置更改音量.")
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
stu.send_msg("Incich School Utilities v2 启动成功. 输入Help以查询更多信息.")


while True:
    print("获取消息...")
    try:
        handle(stu.wait_new_msg().lower())
    except Exception as e:
        print(e)
        stu.send_msg("服务器内部错误: " + str(e))
        time.sleep(5)
