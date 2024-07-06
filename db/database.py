import os
import ssl

import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
client = pymongo.MongoClient(MONGODB_URL, ssl_cert_reqs=ssl.CERT_NONE)
db = client.db
users_collection = db.users
audio_files_collection = db.audio_files
