import pymongo
import json
import pandas as pd
from flight.config import mongo_client


### Provide the mongodb localhost url to connect python to mongodb
client = mongo_client


DATABASE_NAME = 'flight'
COLLECTION_NAME = 'price'

if __name__=="__main__":
    df_train = pd.read_excel('Data_Train.xlsx')
    train_len = df_train.shape[0]
    ## creating test dataset
    test = pd.read_excel('Test_set.xlsx')
    sample_submission = pd.read_excel('Sample_submission.xlsx')
    df_test = pd.concat([test,sample_submission],axis=1)
    test_len = df_test.shape[0]
    ##creating a single dataframe
    df  = pd.concat([df_train,df_test],axis=0)

    ## Converting dataframe to json to dump it into mongodb
    df.reset_index(drop=True,inplace=True)
    json_record = list(json.loads(df.T.to_json()).values())

    ## Inserting converted json to mongodb
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)