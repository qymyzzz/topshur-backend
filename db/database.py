import os

import certifi
import pymongo
from dotenv import load_dotenv

load_dotenv()

ca = certifi.where()
MONGODB_URL = os.getenv("MONGODB_URL")
client = pymongo.MongoClient(MONGODB_URL, tlsCAFile=ca)
db = client.db
users_collection = db.users
audio_files_collection = db.audio_files
