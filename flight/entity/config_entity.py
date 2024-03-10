from datetime import datetime
import os,sys
from flight.logger import logging
from flight.exception import FlightException


FILE_NAME = 'flight_price.csv'
TRAIN_FILE_NAME= 'train.csv'
VAL_FILE_NAME = 'val.csv'
TEST_FILE_NAME = 'test.csv'
TRANSFORM_OBJECT_FILE_NAME = 'simple_imputer.pkl'
MODEL_FILE_NAME = "model.pkl"

class TrainingPipelineConfig:

    def __init__(self,):
        self.artifact_dir = os.path.join(os.getcwd(),'artifact',f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")

class DataIngestionConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.database_name ='flight'
        self.collection_name1='train'
        self.collection_name2 ='test'
        self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir,"data_ingestion")
        self.feature_store_file_path = os.path.join(self.data_ingestion_dir,"feature_store",FILE_NAME)
        self.train_file_path  = os.path.join(self.data_ingestion_dir,"dataset",TRAIN_FILE_NAME)
        self.val_file_path = os.path.join(self.data_ingestion_dir,"dataset",VAL_FILE_NAME)
        self.test_file_path = os.path.join(self.data_ingestion_dir,"dataset",TEST_FILE_NAME)

    def to_dict(self,)->dict:
        try:
            pass
        except Exception as e:
            raise FlightException(e,sys) 
        
class DataValidationConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(training_pipeline_config,"data_validation")
        self.report_file_path = os.path.join(self.data_validation_dir,"report.yaml")
        self.missing_threshold:float = 0.2
        self.base_file_path = os.path.join("flight_price_set1.csv")
        

class DataTransformationConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir,"data_transformation")
        self.transform_object_path = os.path.join(self.data_transformation_dir,"imputer_object",TRANSFORM_OBJECT_FILE_NAME)
        self.transformed_train_data_path = os.path.join(self.data_transformation_dir,"train_transformed_data",TRAIN_FILE_NAME.replace("csv","npz"))
        self.transformed_val_data_path = os.path.join(self.data_transformation_dir,"val_transformed_data", VAL_FILE_NAME.replace("csv","npz"))
        self.transformed_test_data_path = os.path.join(self.data_transformation_dir,"test_transformed_data",TEST_FILE_NAME.replace("csv","npz"))

        
        
class ModelTrainerConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir = os.path.join(training_pipeline_config.artifact_dir,"model_trainer")
        self.model_path = os.path.join(self.model_trainer_dir,MODEL_FILE_NAME)
        self.expected_score = 0.70
        self.overfitting_threshold = 0.10



class ModelEvaluationConfig:...
class ModelPusherConfig:...
