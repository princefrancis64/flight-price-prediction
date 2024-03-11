from flight.entity import config_entity 
from flight.entity import artifact_entity
from flight.logger import logging
from flight.exception import FlightException
import os,sys
from flight.resolver import ModelResolver
from flight.utils import load_object, load_numpy_array
from sklearn.metrics import r2_score

class ModelEvaluation:

    def __init__(self,
        model_evaluation_config:config_entity.ModelEvaluationConfig,
        data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
        data_transformation_artifact:artifact_entity.DataTransformationArtifact,
        model_trainer_artifact:artifact_entity.ModelTrainerArtifact
        ):
        try:
            logging.info(f"{'>>'*20} Model Evaluation{'<<'*20}")
            self.model_evaluation_config = model_evaluation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver()
        except Exception as e:
            raise FlightException(e,sys)
        

    def initiate_model_evaluation(self):
        try:
            ## If our `saved_model` folder has any subfolders then we will compare it with that of the new model we have in the 
            ## model_trainer folder
            logging.info("If our `saved_model` folder has any subfolders then we will compare it with that of the new model we have in the\
                         `model_trainer` folder")
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path is None:
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,improved_accuracy=None)
                logging.info(f"Model Evaluation Artifact:{model_eval_artifact}")
                return model_eval_artifact
            
            ### ELSE FINDING THE LOCATION OF LATEST TRANSFORMER,MODEL
            logging.info(f"finding the location of latest, transformer, model")
            prev_transformer_path = self.model_resolver.get_latest_transformer_path()
            prev_model_path = self.model_resolver.get_latest_model_path()

            #### LOADING THE TRANSFOMRER, MODEL OF PREVIOUSLY TRAINED MODEL
            logging.info(f"Loading the transformer, model objects of previously trained model")
            prev_transformer = load_object(file_path=prev_transformer_path)
            prev_model =  load_object(file_path=prev_model_path)

            ### LOADING THE TRANSFORMER, MODEL OF CURRENTLY TRAINED MODEL
            logging.info(f"Loading the transformer, model of currently trained mode")
            current_transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path)
            current_model = load_object(file_path=self.model_trainer_artifact.model_path)
            

            ##### GETTING THE ACCURACY FOR CURRENTLY TRAINED MODEL####
            acc_currently_trained = self.model_trainer_artifact.r2_score_test

            #### GETTING THE ACCURACY FOR PREVIOUSLY TRAINED MODEL #####
            test_df = load_numpy_array(file_path=self.data_transformation_artifact.val_transformed_data)
            ### separating the input and output variable
            X = test_df[:,:-1]
            y = test_df[:,-1]
            y_pred = prev_model.predict(X)
            acc_previously_trained = r2_score(y,y_pred)
            if acc_currently_trained<acc_previously_trained:
                logging.info("Current Model is not better than previous model")
                raise Exception(f"Current Model is not better than previous model")
            model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
                                                          improved_accuracy=acc_currently_trained-acc_previously_trained)
            logging.info(f"Model Evaluation Artifact:{model_eval_artifact}")
            return model_eval_artifact
        except Exception as e:
            raise FlightException(e,sys)

        