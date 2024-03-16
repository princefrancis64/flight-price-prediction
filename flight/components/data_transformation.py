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
from flight.utils import save_object
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from flight import transformation
from catboost import CatBoostRegressor
from sklearn.decomposition import PCA



class DataTransformation:

    def __init__(self,data_transformation_config:DataTransformationConfig,data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise FlightException(e,sys)
                    
    def pca_transformation(self,X):
        try:
            pca=PCA(n_components=18)
            pca.fit(X)
            return pca
        except Exception as e:
            raise FlightException(e,sys)
        
    def min_max_transformer(self,X):
        try:
            scaler = MinMaxScaler()
            scaler.fit(X)
            return scaler
        except Exception as e:
            raise FlightException(e,sys)

        
    def initiate_data_transformation(self,)->artifact_entity.DataTransformationArtifact:

        try:
            
            ############# READING THE DATASET################
            logging.info("Reading the dataset")
            df = pd.read_csv(self.data_ingestion_artifact.feature_store_file_path)
            df.dropna(inplace=True)
            df.reset_index(drop=True,inplace=True)
            logging.info("Successfully dropped the missing column from the dataset")
            logging.info(f"After imputing dataset has :{len(df[df.isna().any(axis=1)])} null values")

            ############ FEATURE ENGINEERING ###################
            df = transformation.feature_engineering(df)

            ################# SCALING THE FEATURES ########################
            X = df.drop('Price',axis=1)
            y = df.Price

            ### Handling the outliers in the Price column
            y[y>40000] = np.median(y)
            
            ## Splitting the dataset
            X_train,X_test,y_train,y_test = train_test_split(X,y,train_size=0.7,random_state=100)
            scaler = self.min_max_transformer(X_train)
            ### Saving the MinMaxScaler object
            save_object(file_path=self.data_transformation_config.min_max_object_path,obj=scaler)

            X_train = scaler.transform(X_train)
            X_test = scaler.transform(X_test)

            ######################## PCA ########################################
            pca = self.pca_transformation(X_train)
            logging.info("Saving the pca object")
            save_object(file_path=self.data_transformation_config.pca_object_path,obj=pca)

            X_train_scaled = pca.transform(X_train)
            X_test_scaled = pca.transform(X_test)
            logging.info("dataset has been fully ready to build a model upon")

            

            ########## Saving the train and test dataframe arrays ############
            df_train = np.c_[X_train_scaled,y_train]
            df_test = np.c_[X_test_scaled,y_test]
            utils.save_numpy_array(file_path=self.data_transformation_config.transformed_train_data_path,
                                   array = df_train)
            utils.save_numpy_array(file_path=self.data_transformation_config.transformed_test_data_path,
                                   array=df_test)
            
            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                pca_object_file_path=self.data_transformation_config.pca_object_path,
                min_max_scaler_file_path=self.data_transformation_config.min_max_object_path,
                train_transformed_data= self.data_transformation_config.transformed_train_data_path,
                test_transformed_data= self.data_transformation_config.transformed_test_data_path
            )

            logging.info(f"Data transformation artifact{data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise FlightException(e,sys)
        
