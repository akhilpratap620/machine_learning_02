import yaml
from Airfoil_prediction.exception import FailureException
import os , sys
import json
import numpy as np
import dill

def read_yaml(file_path:str)->dict:
    """
    Read a YAML file and return in as dict 
    file_path:str
    """
    try:
        with open(file_path , "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise FailureException(e, sys) from e 
        
def write_json(file_path:str ,data):
    try:
        with open(file_path ,"w") as file:
            json.dump(data , file , indent=6)
    except Exception as e:
        raise FailureException(e, sys) from e        
        
def save_numpy_array_data(file_path:str,array:np.array)->np.array:
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path , exist_ok=True)
        with open(file_path ,'wb') as file_obj:
            np.save(file_obj ,array)
    except Exception as e:
        raise FailureException(e,sys) from e

def load_numpy_array(file_path:str)->np.array:
    try:
        with open(file_path , 'rb') as file_obj:
            return np.load(file_obj)

    except Exception as e:
        raise FailureException(e,sys) from e

def save_object(file_path:str ,obj):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path ,exist_ok=True)
        with open(file_path ,"wb") as file_obj:
            dill.dump(obj ,file_obj)
    except Exception as e:
        raise FailureExeption(e,sys) from e

def load_object(file_path:str):
    try:
        with open(dir_path , 'rb') as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise FailureExeption(e,sys) from e