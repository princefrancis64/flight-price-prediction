import pymongo
import json
import pandas as pd
from flight.config import mongo_client

client = mongo_client

DATA_FILE_PATH = "Data_Train.xlsx"
DATABASE_NAME="flight"
COLLECTION_NAME="price"
COLLECTION_NAME2="price2"

if __name__=="__main__":
    df = pd.read_excel(DATA_FILE_PATH)
    ### Test dataset
    test = pd.read_excel("input_files\Test_set.xlsx")

    #Convert dataframe to json to dump the records into mongodb
    df.reset_index(drop = True,inplace = True)
    json_record = list(json.loads(df.T.to_json()).values())

    test.reset_index(drop = True,inplace = True)
    json_record2 = list(json.loads(test.T.to_json()).values())


    #insert converted json record to mongodb
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)
    client[DATABASE_NAME][COLLECTION_NAME2].insert_many(json_record2)