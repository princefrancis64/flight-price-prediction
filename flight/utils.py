import pandas as pd
import numpy as np
from flight.logger import logging
from flight.exception import FlightException
from flight.config import mongo_client
import os,sys
import yaml
import dill
import datetime as dt
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

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
    

def save_object(file_path:str,obj:object)->None:
    try:
        logging.info("Entered the save object method of utils")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as file_obj:
            dill.dump(obj,file_obj)
        logging.info("Exited the save object method of utils")
    except Exception as e:
        raise FlightException(e,sys)
        

def save_numpy_array(file_path:str,array:np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise FlightException(e,sys)
    

def load_numpy_array(file_path:str)->np.array:
    try:
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj,allow_pickle=True)
    except Exception as e:
        raise FlightException(e,sys)
    

def load_object(file_path:str)->object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file path {file_path} do not exists")
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise FlightException(e,sys)
    




