from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
import string
import re


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


def wiki_search(keyword):
    res = ""
    try:
        res = send_http_get("https://baike.baidu.com/search/word", data={"word": keyword}, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36", "Referer": "https://baike.baidu.com/"}, timeout=10)
    except Exception as e:
        print(e)
        res = send_http_get("https://baike.baidu.com/search/word", data={"word": keyword}, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36", "Referer": "https://baike.baidu.com/"}, timeout=10)
    bs = BeautifulSoup(res, features="html.parser")
    has_branch = False
    counter = 1
    result = ""
    for item in bs.find_all("li", class_="item"):
        try:
            has_branch = True
            result += "搜索结果 - " + str(counter) + " " + str(item.contents[1].string + "\n") + "\n"
            if counter == 1:
                for content in bs.find_all("div", class_="para"):
                    if content.string is not None:
                        result += content.string + "\n"
                counter += 1
            else:
                res_2 = ""
                try:
                    res_2 = send_http_get("https://baike.baidu.com" + str(item.contents[1].attrs['href']), data={}, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36", "Referer": "https://baike.baidu.com/"}, timeout=10)
                except Exception as e:
                    print(e)
                    res_2 = send_http_get("https://baike.baidu.com" + str(item.contents[1].attrs['href']), data={}, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36", "Referer": "https://baike.baidu.com/"}, timeout=10)
                bs_2 = BeautifulSoup(res_2, features="html.parser")
                for content in bs_2.find_all("div", class_="para"):
                    if content.string is not None:
                        result += content.string + "\n"
                points = re.compile(u"[\U00010000-\U0010ffff]", flags=re.UNICODE)
                result = points.sub(u'', result)
                counter += 1
                result += "\n"
        except Exception as e:
            print(e)

    if not has_branch:
        try:
            result = ""
            result += "搜索结果 - 1 " + keyword + "\n\n"
            for content in bs.find_all("div", class_="para"):
                if content.string is not None:
                    result += content.string + "\n"
            points = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
            result = points.sub(u'', result)
        except Exception as e:
            print(e)

    return result
