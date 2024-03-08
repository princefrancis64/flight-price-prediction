from datetime import datetime
import os


FILE_NAME = 'flight_price.csv'
TRAIN_FILE_NAME= 'train.csv'
TEST_FILE_NAME = 'test.csv'

class TrainingPipelineConfig:

    def __init__(self,):
        self.artifact_dir = os.path.join(os.getcwd(),'artifact',f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")

class DataIngestionConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.database_name ='flight'
        self.collection_name='price'
        self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir,"data_ingestion")
        self.feature_store_file_path = os.path.join(self.data_ingestion_dir,"feature_store",FILE_NAME)
        self.train_file_path  = os.path.join(self.data_ingestion_dir,"dataset",TRAIN_FILE_NAME)
        self.test_file_path = os.path.join(self.data_ingestion_dir,"dataset",TEST_FILE_NAME)
        self.train_length = 10683

class DataValidationConfig:...
class DataTransformationConfig:...
class ModelTrainerConfig:...
class ModelEvaluationConfig:...
class ModelPusherConfig:...
