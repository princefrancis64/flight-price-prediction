from flight.entity import artifact_entity,config_entity
from flight.exception import FlightException
from flight.logger import logging
import sys
import numpy as np
from catboost import CatBoostRegressor
from flight import utils
from sklearn.metrics import r2_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import GradientBoostingRegressor

class ModelTrainer:
    
    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,
                 data_transformation_artifact:artifact_entity.DataTransformationArtifact):
        try:
            logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise FlightException(e,sys)
        
    def train_model(self,X_train,y_train):
        try:
            model = GradientBoostingRegressor()
            model.fit(X_train,y_train)
            return model
        except Exception as e:
            raise FlightException(e,sys)
        
    def hyper_param_tuning(self,X_train,X_test,y_train,y_test):
        gb = GradientBoostingRegressor()
        param_grid = {
        'learning_rate': [0.01, 0.05, 0.1],  # Learning rate
        'n_estimators': [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],  # Number of boosting stages
        'max_depth': [3, 4, 5, 6, 7],  # Maximum depth of the individual estimators
        'min_samples_split': [2, 5, 10],  # Minimum number of samples required to split an internal node
        'min_samples_leaf': [1, 2, 4],  # Minimum number of samples required to be at a leaf node
        'max_features': ['sqrt', 'log2'],  # Number of features to consider when looking for the best split
        'subsample': [0.6, 0.7, 0.8, 0.9, 1.0],  # Fraction of samples used for fitting the individual base learners # Random seed for reproducibility
            }
        random_search = RandomizedSearchCV(estimator=gb,param_distributions=param_grid,
                            verbose=3,n_jobs=-1,cv=5,scoring='neg_mean_squared_error')
        random_search.fit(X_train,y_train)
        gb_best = random_search.best_estimator_
        y_train_pred= gb_best.predict(X_train)
        r2_train_gb = r2_score(y_train,y_train_pred)
        y_test_pred = gb_best.predict(X_test)
        r2_test_gb = r2_score(y_test,y_test_pred)
        logging.info(f"Train Acc After Hyperparameter tuning:{r2_train_gb}")
        logging.info(f"Test Acc after Hyperparameter tuning:{r2_test_gb}")
        return r2_train_gb,r2_test_gb,gb_best

        
    def initiate_trainer_modle(self,)->artifact_entity.ModelTrainerArtifact:
        try:
            logging.info(f"Initiating the Model Training Process")
            df_train = utils.load_numpy_array(file_path=self.data_transformation_artifact.train_transformed_data)
            df_test = utils.load_numpy_array(file_path=self.data_transformation_artifact.test_transformed_data)

            
            logging.info("splitting into independent and output feature")
            X_train = df_train[:,:-1]
            X_test = df_test[:,:-1]
            y_train = df_train[:,-1]
            y_test = df_test[:,-1]

            ######################## TRAINING THE MODEL ##########################
            model = self.train_model(X_train,y_train)
            

            logging.info("Calculating the r2_score of train_set")
            y_train_pred = model.predict(X_train)
            r2_score_train = r2_score(y_train,y_train_pred)
            

            logging.info("Calculating the r2_score of test_set ")
            y_test_pred = model.predict(X_test)
            r2_score_test = r2_score(y_test,y_test_pred)
            logging.info(f'Without hyperparameter tuning')  

            logging.info(f"[r2_score Train]:{r2_score_train}\n[r2_score_Test]:{r2_score_test}")
            #################### CHECK FOR OVERFITTING OR UNDERFITTING #######################
            logging.info("Checking if our model is underfitted or not")
            if r2_score_train<self.model_trainer_config.expected_score:
                raise Exception(f"Model is underfitting since the [Expected accuracy:{self.model_trainer_config.expected_score}]\
                                \n [Train Accuracy:{r2_score_train}]")
            
            logging.info(f"Checking if our model is overfitting or not")
            diff = np.abs(r2_score_train - r2_score_test)
            if diff > self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Model is overfitting since the [Expected threshold:{self.model_trainer_config.overfitting_threshold}]\
                                \n [Actual threshold:{diff}]")
            
            ################### HYPERPARAMETER TUNING ####################################

            # r2_train_gb,r2_test_gb,best_estimator = self.hyper_param_tuning(
            #                                                     X_train= X_train,
            #                                                     X_test = X_test,
            #                                                     y_train = y_train,
            #                                                     y_test = y_test)
            # if (r2_train_gb>r2_score_train) and (r2_test_gb>r2_score_test):
            #     r2_score_train = r2_train_gb
            #     r2_score_test = r2_test_gb
            #     model = best_estimator
            #     logging.info(f' Model accuracy increased with hyperparameter tuning')
                


            ################### SAVING THE MODEL ###################################
            utils.save_object(file_path=self.model_trainer_config.model_path,
                              obj = model)

            logging.info(f"Final Acc")
            logging.info(f"[Train Acc:{r2_score_train}]||[Test Acc:{r2_score_test}]")
            ### Preparing the artifact
            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(
                model_path=self.model_trainer_config.model_path,
                r2_score_train=r2_score_train,
                r2_score_test= r2_score_test
            )
                
            logging.info(f"Model Trainer Artifact:{model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise FlightException(e,sys)
        

    

        
    