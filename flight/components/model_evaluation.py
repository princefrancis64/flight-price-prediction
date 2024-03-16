from flight.entity import config_entity 
from flight.entity import artifact_entity
from flight.logger import logging
from flight.exception import FlightException
import os,sys
from flight.resolver import ModelResolver
from flight.utils import load_object, load_numpy_array
from sklearn.metrics import r2_score
from flight.transformation import feature_engineering
import pandas as pd,numpy as np

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
            
            
            ### ELSE FINDING THE LOCATION OF PREVIOUS MODEL,PCA,MIN_MAX_SCALER
            logging.info(f"finding the location of  model,pca, min_max_scaler")
            prev_pca_path = self.model_resolver.get_latest_pca_path()
            prev_min_max_path = self.model_resolver.get_latest_min_max_path()
            prev_model_path = self.model_resolver.get_latest_model_path()


            #### LOADING THE OBJECT FOR MODEL,PCA,MIN_MAX_SCALER OF PREVIOUSLY TRAINED MODEL
            logging.info(f"Loading the model,pca,min_max_scaler objects of previously trained model")
            prev_pca = load_object(file_path=prev_pca_path)
            prev_min_max = load_object(file_path=prev_min_max_path)
            prev_model =  load_object(file_path=prev_model_path)

            ##### GETTING THE ACCURACY FOR CURRENTLY TRAINED MODEL####
            acc_currently_trained = self.model_trainer_artifact.r2_score_test
            logging.info(f"Current trained model accuracy is {acc_currently_trained}")

            ### reading the dataframe
            df = pd.read_csv(self.data_ingestion_artifact.feature_store_file_path)

            ## dropping all the null values
            df.dropna(inplace=True)
            df.reset_index(drop=True,inplace=True)

            X = df.iloc[:,:-1]
            y = df.iloc[:,-1]
            ## Feature Engineering
            X = feature_engineering(X)

            ### scaling the features using previous scaler
            X = prev_min_max.transform(X)

            ### PCA implementation using previous pca
            X_scaled = prev_pca.transform(X)

            ## getting the outliers corrected
            y[y>40000] = np.median(y)

            ### Predicting the model
            y_pred = prev_model.predict(X_scaled)
            acc_previously_trained = r2_score(y,y_pred)

            if acc_currently_trained<acc_previously_trained:
                logging.info("Current Model is not better than previous model")
                raise Exception(f"Current Model is not better than previous model")
            elif (acc_currently_trained-acc_previously_trained)<self.model_evaluation_config.change_threshold:
                logging.info("New Model is not much of an improvement")
                raise Exception(f"New Model is not much of an improvement")
            
            logging.info("Current Model is better than Previous model")
            model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
                                                          improved_accuracy=acc_currently_trained-acc_previously_trained)
            logging.info(f"Model Evaluation Artifact:{model_eval_artifact}")
            return model_eval_artifact
        except Exception as e:
            raise FlightException(e,sys)

        