from flight import utils
from flight.entity import config_entity,artifact_entity
from flight.exception import FlightException
from flight.logger import logging
import os,sys
import pandas as pd
from sklearn.model_selection import train_test_split

class DataIngestion:
    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise FlightException(e,sys)
        
    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        try:
            logging.info(f"Data Ingestion into feature store and dataaset folder")
            ## Getting training dataset from mongodb
            df_train:pd.DataFrame= utils.get_collection_as_dataframe(
                database_name= self.data_ingestion_config.database_name,
                collection_name= self.data_ingestion_config.collection_name1
            )

            ## Getting the testing dataset from mongodb
            df_test:pd.DataFrame= utils.get_collection_as_dataframe(
                database_name= self.data_ingestion_config.database_name,
                collection_name= self.data_ingestion_config.collection_name2
            )

            logging.info("Save the complete TRAINING data into feature store")

            ## Save data into feature store
            logging.info("Creating feature store folder if not available")
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True)
            logging.info("Saving dataset into feature store")
            ## Saving dataset to feature store
            df_train.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False,header=True)

            logging.info("splitting the TRAIN dataset into TRAIN AND VALIDATION SET")
            train_df,val_df = train_test_split(df_train,test_size=0.2,random_state=42)

            logging.info("Creating dataset directory if not available")
            ## Create train dataset directory if not available
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True)

            logging.info("Saving train,validation and test dataset into the dataset folder")
            train_df.to_csv(path_or_buf = self.data_ingestion_config.train_file_path,index=False,header=True)
            val_df.to_csv(path_or_buf = self.data_ingestion_config.val_file_path,index=False,header=True)
            df_test.to_csv(path_or_buf = self.data_ingestion_config.test_file_path,index=False,header=True)

            ### Preparing the artifact
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path,
                val_file_path=self.data_ingestion_config.val_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
            )

            logging.info(f"Data Ingestion artifact:{data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise FlightException(e,sys)