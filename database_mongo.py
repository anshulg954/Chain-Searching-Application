import pymongo
from pymongo import MongoClient
import json
from bson.json_util import dumps
client = pymongo.MongoClient(
    "mongodb+srv://tanishq:9m1pZqvlST5FW52D@rcsb-data.f4dqp.mongodb.net/rcsb?retryWrites=true&w=majority")
db = client['rcsb']
collection = db['rcsb']


def insert_data(data):
    try:
        collection.insert_one(data)
        return True
    except Exception as e:
        print(e)
        return False


def json_get():
    with open("temp.json", "r") as inp:
        read_data = inp.read()
    filedata = json.loads(read_data)
    for data in filedata:
        status = check_key_duplicate(data['key'])
        if status == False:
            if(insert_data(data)):
                print("Successfully Inserted the data!")
            else:
                print("Insertion failed!")
        else:
            print("Duplicate Data")

# get all the data


def query():
    data_ob = collection.find()
    return data_ob

# get the data count


def get_document_count(filters):
    query = {}
    if filters:
        query.update(filters)
    collection_count = collection.count_documents(query)
    return collection_count


def check_key_duplicate(key):
    query = {"key": {"$eq": key}}
    count = get_document_count(query)
    if count == 0:
        return False
    return True

# the searching part


def search_chains(info):
    info = ".*"+info+".*"
    temp = collection.find({'chain': {'$regex': info}}, {'_id': 0})
    # temp = collection.find({'chain': {'$regex': info}}, {'_id': 0, 'chain': 0})
    ans = []
    for i, t in enumerate(temp):
        # for only url
        # dic = {}
        # dic['no'] = i
        # dic['url'] = t['url']
        # ans.append(dic)
        ans.append(t)
    return ans


if __name__ == "__main__":
    json_get()
    info = query()
    for i in info:
        print(type(i))
