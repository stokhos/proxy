import requests
from pymongo import MongoClient

MONGODB = 'mongodb://localhost:27017'


def check(ip_port):
  check_url_list = [
      'http://m.weibo.cn/container/getIndex?type=uid&value=5273307470&containerid=1005055273307470&page=1',
      'http://www.baidu.com',
  ]
  timeout = 3
  proxies = {
      'http': ip_port,
  }
  for check_url in check_url_list:
    try:
      r = requests.get(check_url, proxies=proxies, timeout=timeout)
      if r.status_code != 200:
        raise HttpError
    except:
      print(ip_port + '已舍弃')
      return False
  return ip_port


def insert(ip_port):
  ip_port = check(ip_port)
  if ip_port:
    client = MongoClient(MONGODB)
    db = client['proxy_pool']
    collection = db['articles']
    post = {
        "ip": ip_port,
    }
    existence = collection.find_one({"ip": ip_port})
    if not existence:
      post_id = collection.insert_one(post).inserted_id
      print(ip_port + '已写入')
    else:
      print(existence["ip"] + '已存在')


def query():
  collection = MongoClient(MONGODB)['proxy_pool']['articles']
  try:
    ip_port = list(collection.aggregate([{"$sample": {"size": 1}}]))[0]["ip"]
    if check(ip_port):
      return ip_port
    else:
      delete(ip_port)
      ip_port = list(collection.aggregate([{"$sample": {"size": 1}}]))[0]["ip"]
      while not check(ip_port):
        delete(ip_port)
        ip_port = list(collection.aggregate(
            [{"$sample": {"size": 1}}]))[0]["ip"]
      return ip_port
  except IndexError:
    print('数据库为空，请先抓取IP_PORT')
    return False


def delete(ip_port):
  if ip_port:
    collection = MongoClient(MONGODB)['proxy_pool']['articles']
    collection.remove({"ip": ip_port})
    print(ip_port + '已删除')


def polling():
  collection = MongoClient(MONGODB)['proxy_pool']['articles']
  cursor = collection.find()
  for document in cursor:
    ip_port = document["ip"]
    if check(ip_port):
      print(ip_port)
      break
    else:
      delete(ip_port)
