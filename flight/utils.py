import pandas as pd
import numpy as np
from flight.logger import logging
from flight.exception import FlightException
from flight.config import mongo_client
import os,sys
import yaml
import dill
import numpy 
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
    
### data transformation steps
def feature_engineering(df):
    logging.info("Entered the feature engineering method of utils")
    df['Date_of_Journey']=pd.to_datetime(df['Date_of_Journey'],format='%d/%m/%Y')

    ## Let's Convert the Dep_Time to suitable format and also create new columns
    df['Dep_Time'] = pd.to_datetime(df['Dep_Time'],format ='%H:%M')
    df['Dep_Time_hour'] = df['Dep_Time'].dt.hour
    df['Dep_Time_mins'] = df['Dep_Time'].dt.minute

    ## Converting the Arrival_Time to suitable format and also create new columns
    df['Arrival_Time'] = pd.to_datetime(df['Arrival_Time'])
    df['Arrival_Time_hour'] = df['Arrival_Time'].dt.hour
    df['Arrival_Time_mins'] = df['Arrival_Time'].dt.minute

## Converting Duration of the flight to a numerical value
    def change_duration_to_minutes(duration):
        if 'h' in duration and 'm' in duration:
            hours,minutes = map(int,duration.replace('h','').replace('m','').split())
            return hours*60+minutes
        elif 'h' in duration:
            hours = int(duration.replace('h',''))
            return hours*60
        else:
            minutes = int(duration.replace('m',''))
            return minutes

    df['Duration'] = df['Duration'].apply(change_duration_to_minutes)


    ### Making New Delhi to Delhi since both are same   
    df['Destination'].replace({'New Delhi':'Delhi'},inplace=True)


    ### get dummies variable
    airline = pd.get_dummies(df['Airline'],drop_first=True,prefix='Airline')
    source = pd.get_dummies(df['Source'],drop_first=True,prefix='Source')
    destination = pd.get_dummies(df['Destination'],drop_first=True,prefix='Destination')

    ## Splitting the Route column to Route 1, Route 2 , Route 3, Route 4
    def split(x):
        return x.split()[0::2]
    df['Route'] = df['Route'].apply(split)

    # Splitting routes into separate columns
    df[['Route1', 'Route2', 'Route3', 'Route4','Route5','Route6']] = df['Route'].apply(lambda x: pd.Series(x))


    ## Dropping the original columns
    cols_todrop= ['Airline','Route','Source','Destination']
    df.drop(cols_todrop,axis=1,inplace=True)

    ### Encoding the columns now
    ### Total_Stops
    df.loc[:,'Total_Stops'] = df.loc[:,'Total_Stops'].replace({
        '1 stop':1,
        'non-stop':0,
        '2 stops':2,
        '3 stops':3,
        '4 stops':4
    })
    df['Total_Stops'] = df['Total_Stops'].apply(lambda x: int(x))

    ### LabelEncoding
    le = LabelEncoder()
    df.loc[:,'Route1'] = le.fit_transform(df['Route1'])
    df.loc[:,'Route2'] = le.fit_transform(df['Route2'])
    df.loc[:,'Route3'] = le.fit_transform(df['Route3'])
    df.loc[:,'Route4'] = le.fit_transform(df['Route4'])
    df.loc[:,'Route5'] = le.fit_transform(df['Route5'])
    df.loc[:,'Route6'] = le.fit_transform(df['Route6'])
    df.loc[:,'Additional_Info']  =le.fit_transform(df['Additional_Info'])

    ## Combining  the dummies
    combined = pd.concat([airline,source,destination],axis=1)
    cols = combined.columns

    ### Mapping the boolean values to 1 and 0
    for i in cols:
        combined[i] = combined[i].map({True:1,False:0})

        
    ## Concatenating to the main column
    df= pd.concat([df,combined],axis=1)
    ## Dropping unwanted columns
    df.drop(['Date_of_Journey','Dep_Time','Arrival_Time','Route6'],axis=1,inplace=True)
    logging.info("Exited the feature engineering method of utils")
    return df
    

def save_numpy_array(file_path:str,array:np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise FlightException(e,sys)
    




