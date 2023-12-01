# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from random import randrange


def generate_proxy():
    proxies = []

    url = 'https://sslproxies.org/'
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'
    }
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.content, 'lxml')
    for item in soup.find('table', attrs={'class': 'table-striped'}):
        # print(item)
        try:
            proxies.append({'ip': item.select('td')[0].get_text(), 'port': item.select('td')[1].get_text()})
        except:
            print('')
    print(proxies)
    rnd=randrange(len(proxies))
    randomIP=proxies[rnd]['ip']
    randomPort=proxies[rnd]['port']
    return randomIP + ":" + randomPort

print(generate_proxy())

#http://47.74.154.143:8787	