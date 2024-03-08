from flight import utils
from flight.entity import config_entity,artifact_entity
from flight.exception import FlightException
from flight.logger import logging
import os,sys
import pandas as pd

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
            ## Exporting collection data as pandas dataframe
            df:pd.DataFrame= utils.get_collection_as_dataframe(
                database_name= self.data_ingestion_config.database_name,
                collection_name= self.data_ingestion_config.collection_name
            )
            logging.info("Save the complete data into feature store")

            ### dropping the rows with NAN values
            df.dropna(inplace=True)
            ## reset the index
            df.reset_index(drop=True,inplace=True)

            ## Save data into feature store
            logging.info("Creating feature store folder if not available")
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True)
            logging.info("Saving dataset into feature store")
            ## Saving dataset to feature store
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False,header=True)

            logging.info("splitting dataset intot train and test set")
            train_length = self.data_ingestion_config.train_length
            train_df = df.iloc[:train_length-1]
            test_df = df.iloc[train_length-1:]

            logging.info("Creating dataset directory if not available")
            ## Create dataset directory if not available
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True)

            logging.info("Saving train and test dataset into the dataset folder")
            train_df.to_csv(path_or_buf = self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df.to_csv(path_or_buf = self.data_ingestion_config.test_file_path,index=False,header=True)

            ### Preparing the artifact
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
            )

            logging.info(f"Data Ingestion artifact:{data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise FlightException(e,sys)