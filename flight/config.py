import pymongo
import pandas as pd
import json
from dataclasses import dataclass
import os

@dataclass
class EnvironmentVariable:
    mongo_db_url:str = os.getenv("MONGO_DB_URL")



evn_var = EnvironmentVariable()
mongo_client= pymongo.MongoClient(evn_var.mongo_db_url)