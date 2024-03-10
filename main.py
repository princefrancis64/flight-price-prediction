from flight.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig
from flight.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from flight.components.data_ingestion import DataIngestion
from flight.components.data_validation import DataValidation
from flight.components.data_transformation import DataTransformation


    

if __name__=="__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        data_validation_config = DataValidationConfig(training_pipeline_config=training_pipeline_config.artifact_dir)
        data_validation = DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
        data_validation_artifact = data_validation.initiate_data_validation()

        data_transformation_config = DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_transformation = DataTransformation(data_transformation_config=data_transformation_config,data_ingestion_artifact=data_ingestion_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
    except Exception as e:
        print(e)


    
