import yaml
from Airfoil_prediction.exception import FailureException
import os , sys


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
        

        




    