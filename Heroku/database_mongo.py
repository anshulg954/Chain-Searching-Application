import pymongo
from pymongo import MongoClient
import json
from multiprocessing.dummy import Pool as ThreadPool

from bson.json_util import dumps
client = pymongo.MongoClient(
    "mongodb+srv://tanishq:9m1pZqvlST5FW52D@rcsb-data.f4dqp.mongodb.net/rcsb?retryWrites=true&w=majority")
db = client['rcsb']
collection = db['rcsb']


def search_chains(info):
    info = ".*"+info+".*"
    temp = collection.find({'chain': {'$regex': info}}, {'_id': 0})
    ans = []
    seq = []
    for i, t in enumerate(temp):
        ans.append(t)
        seq.append(t['key'])
    return [seq, ans]


def homologous_search(info):
    X = info
    s = set()
    s.add(X)
    temp = set(s)
    for i in temp:
        s.add(i.replace('L', 'I'))
        s.add(i.replace('L', 'M'))
        s.add(i.replace('I', 'M'))
        s.add(i.replace('I', 'L'))
        s.add(i.replace('M', 'L'))
        s.add(i.replace('M', 'I'))
    temp = set(s)
    for i in temp:
        s.add(i.replace('F', 'Y'))
        s.add(i.replace('F', 'W'))
        s.add(i.replace('Y', 'F'))
        s.add(i.replace('Y', 'W'))
        s.add(i.replace('W', 'F'))
        s.add(i.replace('W', 'Y'))
    temp = set(s)
    for i in temp:
        s.add(i.replace('H', 'K'))
        s.add(i.replace('H', 'R'))
        s.add(i.replace('K', 'H'))
        s.add(i.replace('K', 'R'))
        s.add(i.replace('R', 'H'))
        s.add(i.replace('R', 'K'))
    temp = set(s)
    for i in temp:
        s.add(i.replace('S', 'T'))
        s.add(i.replace('T', 'S'))
    temp = set(s)
    for i in temp:
        s.add(i.replace('N', 'Q'))
        s.add(i.replace('Q', 'N'))
    temp = set(s)
    for i in temp:
        s.add(i.replace('D', 'E'))
        s.add(i.replace('E', 'D'))
    temp = set(s)
    for i in temp:
        s.add(i.replace('A', 'V'))
        s.add(i.replace('V', 'A'))
    infos = []
    for i in s:
        infos.append(".*"+i+".*")
    pool = ThreadPool(30)
    pool.map(do_thread, infos)
    pool.close()
    pool.join()
    return [seq, ans]


ans = []
seq = []


def do_thread(infos):
    temp = infos
    dic = {}
    data = []
    dic["Chain"] = temp[2:-2]
    temp = collection.find({'chain': {'$regex': temp}}, {'_id': 0}).limit(50)
    for i, t in enumerate(temp):
        data.append(t)
        seq.append(t['key'])
    dic["Data"] = data
    ans.append(dic)
