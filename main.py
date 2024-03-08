from flight.logger import logging
from flight.exception import FlightException
import sys,os
from flight.utils import get_collection_as_dataframe
from flight.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from flight.components.data_ingestion import DataIngestion
def test_logger_and_exception():
    try:
        result=3/0
        print(result)
    except Exception as e:
        raise FlightException(e,sys)
    

if __name__=="__main__":
    DataIngestion(DataIngestionConfig(TrainingPipelineConfig())).initiate_data_ingestion()
    
