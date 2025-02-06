import pickle
import os
import sys

from src.exception import CustomException
from src.logger import logging

def save_object(object , save_path : str ):
    
    try:
        dir_path = os.path.dirname(save_path)
        os.makedirs(dir_path , exist_ok=True)
        
        with open(save_path , 'ab') as save_file:
            pickle.dump(object,save_file)
            
    except Exception as e:
        logging.exception(e)
        raise CustomException(e,sys)        
    
def load_object(load_path :str):
    try:
        with open(load_path,"rb") as load_file:
            return pickle.load(load_path)
        
    except Exception as e:
        logging.exception(e) 
        raise CustomException(e,sys)
    
def check_model_exist(save_path :str):
    try:
        if os.path.isfile(save_path):
            return True
        else:
            return False
        
    except Exception as e:
        logging.exception(e) 
        raise CustomException(e,sys)
                   