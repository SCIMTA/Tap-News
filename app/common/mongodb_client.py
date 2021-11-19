from pymongo import MongoClient

DB_NAME = 'tap-news'
MONGO_DB_HOST = 'mongo'
MONGO_DB_PORT = '27017'
# client = MongoClient("%s:%d" % (MONGO_DB_HOST, MONGO_DB_PORT))
# client = MongoClient('mongodb+srv://thanh:thanhtn123@cluster0.un40r.mongodb.net/tap-news?retryWrites=true&w=majority')
client = MongoClient(f'mongodb://{MONGO_DB_HOST}:{MONGO_DB_PORT}')

def get_db(db=DB_NAME):
    db = client[db]
    return db
