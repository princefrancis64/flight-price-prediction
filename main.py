from flight.logger import logging
from flight.exception import FlightException
import sys,os
from flight.utils import get_collection_as_dataframe
from flight.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig,DataValidationConfig
from flight.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from flight.components.data_ingestion import DataIngestion
from flight.components.data_validation import DataValidation
def test_logger_and_exception():
    try:
        result=3/0
        print(result)
    except Exception as e:
        raise FlightException(e,sys)
    

if __name__=="__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        data_validation_config = DataValidationConfig(training_pipeline_config=training_pipeline_config.artifact_dir)
        data_validation = DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
        data_validation_artifact = data_validation.initiate_data_validation()
    except Exception as e:
        print(e)


    
