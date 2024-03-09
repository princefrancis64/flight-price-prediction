import pandas as pd
from flight.logger import logging
from flight.exception import FlightException
from flight.config import mongo_client
import os,sys
import yaml
import dill
import numpy 


def get_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    try:
        logging.info(f"Reading data from database:{database_name} and collection:{collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Found columns:{df.columns}")
        if "_id" in df.columns:
            df.drop("_id",axis=1,inplace=True)
        logging.info(f"Rows and columns in df:{df.shape}")
        return df
    except Exception as e:
        raise FlightException(e,sys)
    
def write_yaml_file(file_path,data:dict):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        with open(file_path,"w") as file_writer:
            yaml.dump(data,file_writer)
    except Exception as e:
        raise FlightException(e,sys)
    


