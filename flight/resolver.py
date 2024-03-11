import os,sys
from typing import Optional
from flight.logger import logging
from flight.exception import FlightException
from flight.entity.config_entity import MODEL_FILE_NAME,TRANSFORM_OBJECT_FILE_NAME

class ModelResolver:
    
    def __init__(self,
                 model_registry:str = "saved_models",
                 transformer_dir_name = "transformer",
                 model_dir_name = "model"
                 ):
        self.model_registry = model_registry
        os.makedirs(self.model_registry,exist_ok=True)
        self.transformer_dir_name = transformer_dir_name
        self.model_dir_name = model_dir_name
        

    def get_latest_dir_path(self)->Optional[str]:
        try:
            dir_names = os.listdir(self.model_registry)
            if len(dir_names)==0:
                return None
            dir_names = list(map(int,dir_names))
            latest_dir_name = max(dir_names)
            return os.path.join(self.model_registry,f"{latest_dir_name}")
        except Exception as e:
            raise FlightException(e,sys) 
            
    def get_latest_model_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir == None:
                raise Exception(f"Model is not available")
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_NAME)
        except Exception as e:
            raise FlightException(e,sys)
            
    def get_latest_transformer_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"Transformer is not available")
            return os.path.join(latest_dir,self.transformer_dir_name,TRANSFORM_OBJECT_FILE_NAME)
        except Exception as e:
            raise FlightException(e,sys)
            
    def get_latest_save_dir_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                return os.path.join(self.model_registry,f"{0}")
            latest_dir_num = int(os.path.basename(latest_dir))
            return os.path.join(self.model_registry,f"{latest_dir_num+1}")
        except Exception as e:
            raise FlightException(e,sys)
            
        
    def get_latest_save_model_path(self):
        try:
            latest_save_dir_path = self.get_latest_save_dir_path()
            return os.path.join(latest_save_dir_path,self.model_dir_name,MODEL_FILE_NAME)
        except Exception as e:
            raise FlightException(e,sys)
            
    def get_latest_save_transformer_path(self):
        try:
            latest_save_dir_path = self.get_latest_save_dir_path()
            return os.path.join(latest_save_dir_path,self.transformer_dir_name,TRANSFORM_OBJECT_FILE_NAME)
        except Exception as e:
            raise FlightException(e,sys)
            
        