import pymongo
import json
import pandas as pd
from flight.config import mongo_client


### Provide the mongodb localhost url to connect python to mongodb
client = mongo_client


DATABASE_NAME = 'flight'
COLLECTION_NAME1 = 'train'
COLLECTION_NAME2 = 'test'

if __name__=="__main__":
    train= pd.read_excel('Data_Train.xlsx')
    test = pd.read_excel('Test_set.xlsx')

    ## Converting dataframe to json to dump it into mongodb
    train.reset_index(drop=True,inplace=True)
    test.reset_index(drop=True,inplace=True)
    json_record_train = list(json.loads(train.T.to_json()).values())
    json_record_test = list(json.loads(test.T.to_json()).values())

    ## Inserting converted json to mongodb
    client[DATABASE_NAME][COLLECTION_NAME1].insert_many(json_record_train)
    client[DATABASE_NAME][COLLECTION_NAME2].insert_many(json_record_test)