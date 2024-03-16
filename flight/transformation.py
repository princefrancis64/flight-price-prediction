import datetime as dt
import pandas as pd
import numpy as np
from flight import utils
from sklearn.preprocessing import LabelEncoder

def feature_engineering(df):
    """
    Description: This function helps in feature engineering
    =========================================================
    Params:
    df :pd.DataFrame which needs to be passed
    =========================================================
    returns pd.DataFrame
    """
    ### Converting the Date_of_Journey to datetime
    df['Date_of_Journey']=pd.to_datetime(df['Date_of_Journey'],format='%d/%m/%Y')
    
    ## Let's Convert the Dep_Time to suitable format and derive new columns
    df['Dep_Time'] = pd.to_datetime(df['Dep_Time'],format ='%H:%M')
    df['Dep_Time_hour'] = df['Dep_Time'].dt.hour
    df['Dep_Time_mins'] = df['Dep_Time'].dt.minute
    
    ## Converting the Arrival_Time to suitable format and deriving new columns
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
    df['Destination'].value_counts()
    df['Destination'].replace({'New Delhi':'Delhi'},inplace=True)
    
    
    # One-hot encoding for Airline, Source, and Destination
    airline = pd.get_dummies(df['Airline'], drop_first=True, prefix='Airline')
    source = pd.get_dummies(df['Source'], drop_first=True, prefix='Source')
    destination = pd.get_dummies(df['Destination'], drop_first=True, prefix='Destination')
    combined = pd.concat([airline, source, destination], axis=1)
    df = pd.concat([df, combined], axis=1)
    
    # Convert 'Total_Stops' to numeric
    df['Total_Stops'] = df['Total_Stops'].replace({
        '1 stop': 1,
        'non-stop': 0,
        '2 stops': 2,
        '3 stops': 3,
        '4 stops': 4
    }).astype(int)
    
    # Splitting 'Route' into separate columns
    route = df['Route'].str.split('→', expand=True)
    route.columns = [f'Route_{i}' for i in range(1, route.shape[1] + 1)]
    route = route.iloc[:,:4]
    
    # Dropping unnecessary columns
    cols_to_drop = ['Airline', 'Source', 'Destination', 'Route']
    df.drop(cols_to_drop, axis=1, inplace=True)
    
    # Concatenating 'df' and 'route'
    df = pd.concat([df, route], axis=1)
    
    ### getting the categorical columns:
    cat_cols = df.select_dtypes(include='O')
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    for i in cat_cols:
        df[i] = le.fit_transform(df[i])
    if 'Airline_Trujet' in df.columns:
        df = df.drop(['Airline_Trujet'],axis=1)
    #### removing the unecessary columns
    df.drop(['Date_of_Journey','Dep_Time','Arrival_Time'],axis=1,inplace=True)
    return df