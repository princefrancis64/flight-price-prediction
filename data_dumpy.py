import pymongo
import json
import pandas as pd



### Provide the mongodb localhost url to connect python to mongodb
client = pymongo.MongoClient('mongodb+srv://princefrancis64:Oejb2e2l74Gz4NAK@cluster0.o5qm0dq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')



DATABASE_NAME = 'flight'
COLLECTION_NAME = 'price'

if __name__=="__main__":
    df_train = pd.read_excel('Data_Train.xlsx')
    ## creating test dataset
    test = pd.read_excel('Test_set.xlsx')
    sample_submission = pd.read_excel('Sample_submission.xlsx')
    df_test = pd.concat([test,sample_submission],axis=1)

    ##creating a single dataframe
    df  = pd.concat([df_train,df_test],axis=0)

    ## Converting dataframe to json to dump it into mongodb
    df.reset_index(drop=True,inplace=True)
    json_record = list(json.loads(df.T.to_json()).values())

    ## Inserting converted json to mongodb
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)