from datetime import datetime
import os,sys
from flight.logger import logging
from flight.exception import FlightException


FILE_NAME = 'flight_price.csv'
TRAIN_FILE_NAME= 'train.csv'
TEST_FILE_NAME = 'test.csv'
PCA_OBJECT_FILE_NAME = "pca.pkl"
MIN_MAX_SCALER_OBJECT_FILE_NAME = "min_max.pkl"
MODEL_FILE_NAME = "model.pkl"

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
        self.pca_object_path = os.path.join(self.data_transformation_dir,"pca",PCA_OBJECT_FILE_NAME)
        self.min_max_object_path = os.path.join(self.data_transformation_dir,"min_max",MIN_MAX_SCALER_OBJECT_FILE_NAME)
        self.transformed_train_data_path = os.path.join(self.data_transformation_dir,"train_transformed_data",TRAIN_FILE_NAME.replace("csv","npz"))
        self.transformed_test_data_path = os.path.join(self.data_transformation_dir,"test_transformed_data",TEST_FILE_NAME.replace("csv","npz"))

        
        
class ModelTrainerConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir = os.path.join(training_pipeline_config.artifact_dir,"model_trainer")
        self.model_path = os.path.join(self.model_trainer_dir,MODEL_FILE_NAME)
        self.expected_score = 0.70
        self.overfitting_threshold = 0.10



class ModelEvaluationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.change_threshold = 0.01
        
class ModelPusherConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_pusher_dir = os.path.join(training_pipeline_config.artifact_dir,"model_pusher")
        self.model_pusher_model_dir = os.path.join(self.model_pusher_dir,"model",MODEL_FILE_NAME)
        self.model_pusher_pca_dir = os.path.join(self.model_pusher_dir,"pca",PCA_OBJECT_FILE_NAME)
        self.model_pusher_min_max_dir = os.path.join(self.model_pusher_dir,"min_max",MIN_MAX_SCALER_OBJECT_FILE_NAME)


          