import html2text
import requests


def get_http_text(url):
    r = requests.get(url, timeout=10)
    return html2text.html2text(r.text)
