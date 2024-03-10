from flight.entity import config_entity,artifact_entity
from flight.entity.artifact_entity import DataTransformationArtifact,DataIngestionArtifact
from flight.entity.config_entity import DataTransformationConfig,DataIngestionConfig
from flight.logger import logging
from flight.exception import FlightException
import os,sys
import pandas as pd,numpy as np
from typing import Optional
from flight import utils
from sklearn.impute import SimpleImputer
from flight.utils import save_object,feature_engineering
from sklearn.preprocessing import MinMaxScaler



class DataTransformation:

    def __init__(self,data_transformation_config:DataTransformationConfig,data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise FlightException(e,sys)
        
    def get_data_transformer_object(self,):
        try:
            simple_imputer = SimpleImputer(strategy='most_frequent',missing_values=np.NAN)
            return simple_imputer
        except Exception as e:
            raise FlightException(e,sys)
        
    def initiate_data_transformation(self,)->artifact_entity.DataTransformationArtifact:

        try:

            ############ SAVING THE SIMPLE IMPUTER OBJECT ################
            simple_imputer_object =save_object(file_path=self.data_transformation_config.transform_object_path,
                                                         obj = self.get_data_transformer_object())
            logging.info("Successfully saved the simple imputer object")


            ############# READING THE DATASET################
            logging.info("Reading the dataset")
            df = pd.read_csv(self.data_ingestion_artifact.feature_store_file_path)


            ############ IMPUTING THE MISSING VALUES ############
            logging.info(f"Before Imputing:df has {len(df[df.isna().any(axis=1)])} null values")
            # Fit the imputer on the training data
            imputer = self.get_data_transformer_object()
            imputer.fit(df)
            
            df = pd.DataFrame(imputer.transform(df),columns=df.columns)
            logging.info(f"After imputing X_train has :{len(df[df.isna().any(axis=1)])} null values")
            
            ############ FEATURE ENGINEERING ###################
            df = feature_engineering(df)
            

            ### Handling the outliers in the Price column
            df.loc[df['Price']>40000,'Price'] = np.median(df['Price'])

            ### selecting the input features
            logging.info("Input features:X")
            X = df.drop('Price',axis=1)

            logging.info("Ouput variable:y")
            ### selecting the output variable 'Price'
            y = df['Price']

            train_len = 10683
            X_train = X.iloc[:train_len,:]
            X_test = X.iloc[train_len:,:]
            y_train = y.iloc[:train_len]
            y_test = y.iloc[train_len:]
                       

            ################# FEATURE ENGINEERING ########################
            
            
            columns = X_train.columns

            scaler =MinMaxScaler()
            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)
            logging.info("dataset has been fully ready to build a model upon")


            ########## Saving the train and test dataframe arrays ############
            df_train = np.c_[X_train,y_train]
            df_test = np.c_[X_test,y_test]
            utils.save_numpy_array(file_path=self.data_transformation_config.transformed_train_data_path,
                                   array = df_train)
            utils.save_numpy_array(file_path=self.data_transformation_config.transformed_test_data_path,
                                   array=df_test)
            
            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_file_path=self.data_transformation_config.transform_object_path,
                train_transformed_data= self.data_transformation_config.transformed_train_data_path,
                test_transformed_data= self.data_transformation_config.transformed_test_data_path
            )

            logging.info(f"Data transformation artifact{data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise FlightException(e,sys)
        
