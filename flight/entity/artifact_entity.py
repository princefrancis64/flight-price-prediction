from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    feature_store_file_path:str
    train_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifact:
    report_file_path:str

@dataclass
class DataTransformationArtifact:
    pca_object_file_path:str
    min_max_scaler_file_path:str
    train_transformed_data:str
    test_transformed_data:str

@dataclass
class ModelTrainerArtifact:
    model_path:str
    r2_score_train:float
    r2_score_test:float

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted:True
    improved_accuracy:float

@dataclass
class ModelPusherArtifact:
    improved_model_path:str
    improved_pca_path:str
    improved_min_max_path:str