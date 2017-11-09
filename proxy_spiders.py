import requests
import re
import sys
import time
import database
proxies = {
    'http': 'socks5://localhost:1086',
    'https': 'socks5://localhost:1086',
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
}
spider_numbers = 3


def spider0():
    url = 'http://cn-proxy.com/'
    r = requests.get(url, proxies=proxies)
    for ip, port in re.findall('<td>(\d+\.\d+\.\d+\.\d+)</td>\n<td>(\d+)</td>', r.text):
        ip_port = ip + ':' + port
        database.insert(ip_port)


def spider1():
    url = 'http://www.xicidaili.com/'
    r = requests.get(url, headers=headers)
    ips = re.findall('<td>(\d+\.\d+\.\d+\.\d+)</td>', r.text)
    ports = re.findall('<td>(\d+)</td>', r.text)
    for ip, port in zip(ips, ports):
        ip_port = ip + ':' + port
        database.insert(ip_port)


def spider2():
    url = 'http://proxy.com.ru/'
    r = requests.get(url)
    for ip, port in re.findall('<td>(\d+\.\d+\.\d+\.\d+)</td><td>(\d+)</td>', r.text):
        ip_port = ip + ':' + port
        database.insert(ip_port)


def spider3():
    pass


def spider4():
    pass


def spider5():
    pass


def spider6():
    pass
while True:
    print("启动成功，下面开始爬取代理")
    for i in range(spider_numbers):
        function_name = 'spider' + str(i)
        print('spider' + str(i) + '开始工作')
        getattr(sys.modules[__name__], function_name)()
    print("爬取完成，下面开始清理数据库")
    database.polling()
    print("情理完成，下面开始等待3小时")
    time.sleep(10800)
