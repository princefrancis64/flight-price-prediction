from flight.logger  import logging
from flight.exception import FlightException
import os,sys
from flight.entity import artifact_entity,config_entity
from flight.resolver import ModelResolver
from flight.utils import load_object,save_object
from flight.entity.config_entity import TRANSFORM_OBJECT_FILE_NAME,MODEL_FILE_NAME


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
            
            ## creating the new transformer folder inside the new folder
            improved_folder_transformer_path = os.path.join(improved_folder_path,"transformer",TRANSFORM_OBJECT_FILE_NAME)
            os.makedirs(os.path.dirname(improved_folder_transformer_path),exist_ok=True)

            #####   GETTING THE MODEL AND TRANSFORMER OF THE CURRENT MODEL TO BE PUSHED #####
            model = load_object(self.model_trainer_artifact.model_path)
            transformer = load_object(self.data_transformation_artifact.transform_object_file_path)
            logging.info("loaded the model and transformer object")

            
            ##### SAVING THE IMPROVED MODEL AND TRANSFORMER TO THE NEW FOLDER #########
            save_object(file_path=improved_folder_model_path,obj=model)
            save_object(file_path=improved_folder_transformer_path,obj=transformer)
            
            ######## SAVING THE CURRENT MODEL AND TRANSFORMER TO MODEL PUSHER DIR######
            ### creating the model pusher dir
            os.makedirs(self.model_pusher_config.model_pusher_dir)

            ### creating the models dir and saving the model object
            os.makedirs(os.path.dirname(self.model_pusher_config.model_pusher_model_dir))
            save_object(file_path=self.model_pusher_config.model_pusher_model_dir,obj=model)

            ### creating the transformer dir and saving the transformer object
            os.makedirs(os.path.dirname(self.model_pusher_config.model_pusher_transformer_dir))
            save_object(file_path=self.model_pusher_config.model_pusher_transformer_dir,obj=transformer) 

            model_pusher_artifact = artifact_entity.ModelPusherArtifact(improved_model_path=improved_folder_model_path,
                                                                        improved_transformer_path=improved_folder_transformer_path)
            logging.info(f"Model Pusher Artifact{model_pusher_artifact}")

        except Exception as e:
            raise FlightException(e,sys)