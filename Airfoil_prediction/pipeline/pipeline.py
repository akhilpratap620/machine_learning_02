from Airfoil_prediction.config.configuration import Configuration
from Airfoil_prediction.logger import logging
from Airfoil_prediction.exception import FailureException
from Airfoil_prediction.entity.artifact_entity import DataIngestionArtifact
from Airfoil_prediction.entity.config_entity import DataIngestionConfig
from Airfoil_prediction.component.data_ingestion import DataIngestion
import sys ,os


class Pipeline:
    

    
    def __init__(self,config:Configuration =Configuration())->None:
        try:
            self.config = config
        except Exception  as e:
            raise FailureException(e, sys) from e
    
        


    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config =self.config.get_data_ingestion_config())   
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise FailureException(e,sys) from e

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()

            return data_ingestion_artifact
        except Exception as e:
            raise FailureException(e,sys) from e    
    
    def run(self):
        try:
            self.run_pipeline()
        except Exception as e:
            raise FailureException(e,sys) from e       



    