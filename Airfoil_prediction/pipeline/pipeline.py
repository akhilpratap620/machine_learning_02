from Airfoil_prediction.config.configuration import Configuration
from Airfoil_prediction.logger import logging
from Airfoil_prediction.exception import FailureException
from Airfoil_prediction.entity.artifact_entity import DataIngestionArtifact ,DataValidationArtifact, DataTransformationArtifact
from Airfoil_prediction.entity.config_entity import DataIngestionConfig ,DataValidationConfig,DataTransformationConfig
from Airfoil_prediction.component.data_ingestion import DataIngestion 
from Airfoil_prediction.component.data_validation import DataValidation
from Airfoil_prediction.component.data_transformation import DataTransformation
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
            
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            logging.info(f"[{'='*20}]start data validating[{'='*20}]")
            data_validation =DataValidation(data_validation_config=self.config.get_data_validation_config() ,
                                            data_ingestion_artifact=data_ingestion_artifact
            )
            return data_validation.initiate_data_validation()
                  
        except Exception as e:
            raise FailureException(e,sys) from e

    def start_data_transformation(self, data_ingestion_artifact:DataIngestionArtifact, 
                                data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:
            data_transformation=DataTransformation(
                data_transformation_config=self.config.get_data_transformation_config(),
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact
            )
            return data_transformation.initiate_data_transformation()


        except Exception as e:
            raise FailureException(e,sys) from e                                  
    
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact
            )
            logging.info(f"data validating done successfully") 

            return data_validation_artifact
        except Exception as e:
            raise FailureException(e,sys) from e    
    
    def run(self):
        try:
            self.run_pipeline()
        except Exception as e:
            raise FailureException(e,sys) from e       


