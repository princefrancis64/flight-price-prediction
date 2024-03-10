from flight.entity import config_entity,artifact_entity
from flight.logger import logging
from flight.exception import FlightException
from typing import Optional
from scipy.stats import chi2_contingency
import os,sys
from flight import utils
import pandas as pd,numpy as np

class DataValidation:

    def __init__(self,
                 data_validation_config:config_entity.DataValidationConfig,
                 data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_error = dict()
        except Exception as e:
            raise FlightException(e,sys)
        
    def drop_missing_cols_above_threshold(self,df:pd.DataFrame,report_key_name:str)->Optional[pd.DataFrame]:
        try:
            threshold = self.data_validation_config.missing_threshold
            null_report = df.isna().sum()/df.shape[0]
            #selecting column name which contains null
            logging.info(f"selecting column name which contains null values above to {threshold}")
            drop_column_names = null_report[null_report>threshold].index
            
            if len(drop_column_names)>0:
                logging.info(f"Columns to drop:{list(drop_column_names)}")
                self.validation_error[report_key_name] = list(drop_column_names)
                df.drop(list(drop_column_names),axis=1,inplace=True)
            elif len(drop_column_names)==0:
                self.validation_error[report_key_name] = 'No null values above threshold'

            #return None no columns left
            if len(df.columns)==0:
                return None
            return df
        except Exception as e:
            raise FlightException(e,sys)
        
    
    def is_required_columns_exists(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str)->bool:
        try:
            base_columns = base_df.columns
            current_columns = current_df.columns

            missing_columns = []
            for base_column in base_columns:
                if base_column not in current_columns:
                    logging.info(f"Column:[{base_column} is not available]")
                    missing_columns.append(base_column)

            if len(missing_columns)>0:
                self.validation_error[report_key_name] = missing_columns
                return False
            elif len(missing_columns)==0:
                self.validation_error[report_key_name] = "All columns are present"
                return True
        except Exception as e:
            raise FlightException(e,sys)
        

    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str):
        try:
            drift_report = dict()
            base_columns = base_df.columns
            current_columns = current_df.columns

            for base_column in base_columns:
                base_data,current_data = base_df[base_column],current_df[base_column]
                
                ## (H0): There is no association between the two categorical variables.
                ## (H1): There is an association between the two categorical variables.
                logging.info(f"Hypothesis {base_column}:{base_data.dtype},{current_data.dtype}")

                ## creating contingency table
                contingency_table= pd.crosstab(base_df[base_column],current_df[base_column])

                # Perform Chi-Square Test
                chi2,pvalue,dof,expected = chi2_contingency(contingency_table)

                if pvalue>0.05:
                    ## We are accepting null hypothesis
                    drift_report[base_column] = {
                        'pvalues':float(pvalue),
                        'same_distribution':False
                    }
                else:
                    drift_report[base_column] = {
                        'pvalues':float(pvalue),
                        "same_distribution":True
                    }
            self.validation_error[report_key_name] = drift_report

            
        except Exception as e:
            raise FlightException(e,sys)
        

    
    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:
            #####################   READING THE DATASET#############################
            logging.info(f"Reading base dataframe")
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
 

            logging.info(f"Reading train dataframe")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info(f"Reading test dataframe")
            test_df = pd.read_csv(self.data_ingestion_artifact.val_file_path)

            ###################### DROP COLS WITH NULL VALUES ABOVE THRESHOLD ###############################

            logging.info(f"Drop null value columns from train df")
            train_df = self.drop_missing_cols_above_threshold(df = train_df,report_key_name="missing_values_within_train_dataset")
            logging.info(f"Drop null value columns from test df")
            test_df = self.drop_missing_cols_above_threshold(df=test_df,report_key_name="missing_values_within_test_dataset")


            ###################### DOES ALL THE COLUMNS IN BASE_DF ARE IN CURRENT_DF##########################

            logging.info(f"Is all required columns present in train df")
            train_df_columns_status = self.is_required_columns_exists(base_df=base_df,current_df=train_df,report_key_name="All columns present")
            logging.info(f"Does all the columns exist in test set")
            test_df_columns_status = self.is_required_columns_exists(base_df=base_df,current_df=test_df,report_key_name="All columns present")

            ###############        CHECKING DATA DRIFT       #######################################
            if train_df_columns_status:
                logging.info(f"All the columns are present in the train_df hence detecting data drift")
                self.data_drift(base_df=base_df,current_df=train_df,report_key_name="data_drift_within_train_dataset")
            if test_df_columns_status:
                logging.info(f"All the columns are present in the test_df hence detecting data drift")
                self.data_drift(base_df=base_df,current_df=test_df,report_key_name="data_drift_within_test_dataset")


            ## writing the yaml report
            logging.info("Writing the report in yaml file")
            utils.write_yaml_file(file_path=self.data_validation_config.report_file_path,data=self.validation_error)

            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path,
                                                                              )
            logging.info(f"Data Validation Artifact:{data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise FlightException(e,sys)