import urllib.request
from urllib.parse import quote
import string
import json


# HTTP Utilities
def send_http_get(url, data=None, headers=None, timeout=5):
    if data is None:
        data = {}
    if headers is None:
        headers = {}

    temp = "?"
    for key in data:
        temp += (key + '=' + str(data[key]) + '&')

    temp = quote(temp, safe=string.printable)
    req = urllib.request.Request(url + temp, headers=headers)
    conn = urllib.request.urlopen(req, timeout=timeout)
    return conn.read().decode('utf-8')


def send_http_post(url, data=None, headers=None, timeout=5):
    if data is None:
        data = {}
    if headers is None:
        headers = {}

    req = urllib.request.Request(quote(url, safe=string.printable), data=urllib.parse.urlencode(data).encode('utf-8'), headers=headers)
    conn = urllib.request.urlopen(req, timeout=timeout)
    return conn.read().decode('utf-8')


def get_163_music(song_id, filename):
    req = urllib.request.Request('https://music.163.com/song/media/outer/url?id=' + song_id + '.mp3', headers={"Cookie": "appver=1.5.0.75771", "Referer": "https://music.163.com/", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_7) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.65 Safari/534.24"})
    f = urllib.request.urlopen(req)
    with open(filename, 'wb') as file:
        file.write(f.read())
    file.close()


def query_song(name):
    query_res = send_http_post("http://music.163.com/api/search/pc", {"s": name, "offset": "1", "limit": "20", "type": "1"}, {"Cookie": "appver=1.5.0.75771", "Referer": "https://music.163.com/", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_7) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.65 Safari/534.24"})
    song_json = json.loads(query_res)
    res_str = ''
    for song in song_json['result']['songs']:
        res_str += str(song['id']) + " - " + str(song['name']) + " - "
        for artist in song['artists']:
            res_str += artist['name'] + '  '
        res_str += '\n'
    return res_str
