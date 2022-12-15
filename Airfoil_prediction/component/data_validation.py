from Airfoil_prediction.entity.config_entity import DataValidationConfig
from Airfoil_prediction.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact 
from Airfoil_prediction.logger import logging
from Airfoil_prediction.exception import FailureException
import pandas as pd
from Airfoil_prediction.util.util import read_yaml , write_json
import os , sys
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import json
from Airfoil_prediction.util.util import read_yaml



class DataValidation:

    def __init__(self ,data_validation_config:DataValidationConfig , data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config =data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.schema=read_yaml(data_validation_config.schema_file_path)
            

            


        except Exception as e:
            raise FailureException(e,sys) from e
    def get_train_and_test_df(self):
        try:
            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path
            train_df =pd.read_csv(train_file_path)
            test_df=pd.read_csv(test_file_path)
            return train_df,test_df
        except Exception as e:
            raise FailureException(e,sys) from e

    def is_train_test_file_exist(self)->bool:
        try:
            logging.info("checking whether test and train file exist or not")
            is_train_file_exist= False
            is_test_file_exist = False

            training_file_path =self.data_ingestion_artifact.train_file_path
            testing_file_path =self.data_ingestion_artifact.test_file_path

            is_train_file_exist= os.path.exists(training_file_path)
            is_test_file_exist = os.path.exists(testing_file_path)



            return is_train_file_exist and is_train_file_exist

            
            logging.info(f"Is train_file_exist[{is_train_file_exist}], is test file exist[{is_test_file_exist}]")
            if not (is_train_file_exist and is_train_file_exist):
                raise Exception(f"train or test file missing")
        except Exception as e:
            raise FailureException(e,sys) from e    

    def validate_dataset_schema(self):
        try:
            return True
        except Exception as e:
            raise FailureException(e,sys) from e



        except exception as e:
            raise FailureException(e,sys) from e 
    def get_and_save_data_drift_report(self):
        try:
            profile =Profile(sections=[DataDriftProfileSection()])
            train_df,test_df =self.get_train_and_test_df()
            profile.calculate(train_df,test_df)
            report=json.loads(profile.json())
            report_file_path = self.data_validation_config.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)    

            write_json(report_file_path,report)
            return report



        except Exception as e:
            raise FailureException(e,sys) from e

    def save_data_drift_report_page(self):
        try:
            dashboard =Dashboard(tabs=[DataDriftTab()])
            train_df,test_df =self.get_train_and_test_df()
            dashboard.calculate(train_df,test_df)
            report_page_file_path=self.data_validation_config.report_page_file_path
            report_page_dir =os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir , exist_ok=True)

            dashboard.save(report_page_file_path)
            
        except Exception as e:
            raise FailureException(e,sys) from e        

    def is_data_drift_found(self):
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return True
        except Exception as e:
            raise FailureException(e,sys) from e                


    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            self.is_train_test_file_exist()

            
            self.validate_dataset_schema()
            self.is_data_drift_found()
            data_validation_artifact=DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_file_path,
                report_page_file_path=self.data_validation_config.report_page_file_path,
                report_file_path =self.data_validation_config.report_file_path,
                is_validated=True


            )
            return data_validation_artifact
            logging.info("data validation artifact {data_validation_artifact}")

        except Exception as e:
            raise FailureException(e,sys) from e       

    def __del__(self):
        logging.info(f"{'='*20} Data validation completed {'='*20}\n\n") 
