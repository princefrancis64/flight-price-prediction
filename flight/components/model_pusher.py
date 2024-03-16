from flight.logger  import logging
from flight.exception import FlightException
import os,sys
from flight.entity import artifact_entity,config_entity
from flight.resolver import ModelResolver
from flight.utils import load_object,save_object
from flight.entity.config_entity import MODEL_FILE_NAME,PCA_OBJECT_FILE_NAME,MIN_MAX_SCALER_OBJECT_FILE_NAME


class ModelPusher:

    def __init__(self,model_pusher_config:config_entity.ModelPusherConfig,
                 model_trainer_config:config_entity.ModelTrainerConfig,
                 data_transformation_artifact:artifact_entity.DataTransformationArtifact,
                 model_evaluation_config:config_entity.ModelEvaluationConfig,
                 model_trainer_artifact:artifact_entity.ModelTrainerArtifact,
                 ):
        try:
            self.model_pusher_config = model_pusher_config
            self.model_trainer_config =  model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
            self.model_evaluation_config= model_evaluation_config
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver()
        except Exception as e:
            raise FlightException(e,sys)
        

    def initiate_model_pusher(self):
        try:
            logging.info(f"{'>>'*20}Model Pusher Initiated{'<<'*20}")

            ## creating the new folder
            improved_folder_path = self.model_resolver.get_latest_save_dir_path()
            os.makedirs(improved_folder_path,exist_ok=True)
            ## creating the new model folder inside the new folder
            improved_folder_model_path = os.path.join(improved_folder_path,"model",MODEL_FILE_NAME)
            os.makedirs(os.path.dirname(improved_folder_model_path),exist_ok=True)
            

            ## creating the new pca folder inside the new folder
            improved_folder_pca_path = os.path.join(improved_folder_path,"pca",PCA_OBJECT_FILE_NAME)
            os.makedirs(os.path.dirname(improved_folder_pca_path),exist_ok=True)

            ## creating the new min_max folder inside the new folder
            improved_folder_min_max_path = os.path.join(improved_folder_path,"min_max",MIN_MAX_SCALER_OBJECT_FILE_NAME)
            os.makedirs(os.path.dirname(improved_folder_min_max_path),exist_ok=True)

            #####   GETTING THE MODEL,pca, min_max object  OF THE CURRENT MODEL TO BE PUSHED #####
            model = load_object(self.model_trainer_artifact.model_path)
            pca = load_object(self.data_transformation_artifact.pca_object_file_path)
            min_max = load_object(self.data_transformation_artifact.min_max_scaler_file_path)
            logging.info("loaded the model,imputer object,pca object and min_max object")

            
            ##### SAVING THE IMPROVED MODEL,PCA,MIN_MAX TO THE NEW FOLDER #########
            save_object(file_path=improved_folder_model_path,obj=model)
            save_object(file_path=improved_folder_pca_path,obj=pca)
            save_object(file_path=improved_folder_min_max_path,obj=min_max)
            
            ######## SAVING THE CURRENT MODEL,PCA,MIN_MAX TO MODEL PUSHER DIR######
            ### creating the model pusher dir
            os.makedirs(self.model_pusher_config.model_pusher_dir)

            ### creating the models dir and saving the model object
            os.makedirs(os.path.dirname(self.model_pusher_config.model_pusher_model_dir))
            save_object(file_path=self.model_pusher_config.model_pusher_model_dir,obj=model)

            ### creating the pca dir and saving the pca object
            os.makedirs(os.path.dirname(self.model_pusher_config.model_pusher_pca_dir))
            save_object(file_path=self.model_pusher_config.model_pusher_pca_dir,obj=pca)

            ### creating the min_max dir and saving the min_max object
            os.makedirs(os.path.dirname(self.model_pusher_config.model_pusher_min_max_dir))
            save_object(file_path=self.model_pusher_config.model_pusher_min_max_dir,obj=min_max)

            model_pusher_artifact = artifact_entity.ModelPusherArtifact(improved_model_path=improved_folder_model_path,
                                                                        improved_pca_path=improved_folder_pca_path,
                                                                        improved_min_max_path=improved_folder_min_max_path)
            logging.info(f"Model Pusher Artifact{model_pusher_artifact}")

        except Exception as e:
            raise FlightException(e,sys)