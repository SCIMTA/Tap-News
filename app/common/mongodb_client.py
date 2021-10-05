from pymongo import MongoClient

DB_NAME = 'tap-news'

# client = MongoClient("%s:%d" % (MONGO_DB_HOST, MONGO_DB_PORT))
client = MongoClient('mongodb+srv://thanh:thanhtn123@cluster0.un40r.mongodb.net/tap-news?retryWrites=true&w=majority')

def get_db(db=DB_NAME):
    db = client[db]
    return db
