from pymongo import MongoClient

import settings

client = MongoClient(settings.MONGO_LINK)

db = client(settings.MONGO_DB_NAME)
