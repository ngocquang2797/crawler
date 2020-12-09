from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

client = MongoClient('mongodb://ngocquang2797:123456789@mongo:27017/')

try:
    info = client.server_info() # Forces a call.
    print(info)
except ServerSelectionTimeoutError:
    print("server is down.")