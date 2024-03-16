from flight.exception import FlightException
from flight.logger import logging
from flight.resolver import ModelResolver
import pandas as pd
from flight.utils import load_object
import os,sys
import numpy as np
from datetime import datetime
from flight.transformation import feature_engineering
from flight.utils import get_collection_as_dataframe
from flight.entity.config_entity import d

PREDICTION_DIR="predicted_files"

def start_batch_prediction(input_file_path):
    try:
        database_name='flight'
        collection_name='price2'
        input_file_path = "input_files\Test_set.xlsx"
        os.makedirs(PREDICTION_DIR,exist_ok=True)
        logging.info(f"Creating model resolve object")
        model_resolver = ModelResolver(model_registry="saved_models")
        logging.info(f"Reading file:{input_file_path}")
        df = get_collection_as_dataframe(database_name=database_name,collection_name=collection_name)


        ## replacing the na values with np.NAN
        df.replace({"na":np.NAN},inplace=True)

        X = df.copy()
        ### Doing feature engineering on the dataframe
        X = feature_engineering(df=X)

        ## Scaling the dataframe
        scaling_obj = load_object(file_path=model_resolver.get_latest_min_max_path())
        X = scaling_obj.transform(X)

        ## Pca 
        pca_obj = load_object(file_path=model_resolver.get_latest_pca_path())
        X_scaled = pca_obj.transform(X)

        ## predicting the model
        model_obj = load_object(file_path=model_resolver.get_latest_model_path())
        df["predictions"] = model_obj.predict(X_scaled)
        
        ### Making a new folder for predictions
        prediction_file_path = os.path.join(PREDICTION_DIR,"prediction"+f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
        df.to_csv(path_or_buf=prediction_file_path,index=False,header=True)
        return prediction_file_path

    except Exception as e:
        raise FlightException(e,sys)

