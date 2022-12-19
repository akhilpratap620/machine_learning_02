from Airfoil_prediction.logger import logging
from Airfoil_prediction.exception import FailureException
from Airfoil_prediction.entity.config_entity import DataTransformationConfig
from Airfoil_prediction.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
import sys , os
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator , TransformerMixin
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from Airfoil_prediction.util.util import read_yaml ,save_numpy_array_data,load_numpy_array,save_object,load_object
from Airfoil_prediction.constant import *
import pandas as pd
import numpy as np


class DataTransformation:
    def __init__(self , data_transformation_config:DataTransformationConfig,
                 data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_artifact:DataValidationArtifact
                 ):

        try:
            self.data_transformation_config=data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_artifact=data_validation_artifact
            
        except Exception as e:
            raise FailureException(e,sys) from e
    @staticmethod         
    def load_data(file_path:str ,schema_file_path:str)->pd.DataFrame:
        try:
            dataset_schema = read_yaml(schema_file_path) 
            schema = dataset_schema[DATASET_SCHEMA_COLUMNS_KEY]               
            dataframe=pd.read_csv(file_path)
            error_message=""

            for column in dataframe.columns:
                if column in list(schema.keys()):
                    dataframe[column].astype(schema[column])
                else:
                    error_message = f"{error_message} Column: [{column}] is not in schema"

            if len(error_message)>0:
                raise Exception(error_message) 
            return dataframe

        except Exception as e:
            raise FailureException(e,sys) from e                   

    def get_data_transformer_object(self)->ColumnTransformer:
        try:
            schema_file_path=self.data_validation_artifact.schema_file_path
            dataset_schema=read_yaml(schema_file_path)
            columns=dataset_schema[DATASET_SCHEMA_COLUMNS_KEY]
            

            preprocessing=Pipeline(steps=[

                ('imputer', SimpleImputer(strategy="median")),
                ('scalling',StandardScaler())
            ])
            return preprocessing
            logging.info("preprocessing obj generated")
        except Exception as e:
            raise FailureException(e,sys) from e        

    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info(f"started data transformation")
            preprocessing_obj=self.get_data_transformer_object()
            
            logging.info("obtaining train and test file path")
            train_file_path=self.data_ingestion_artifact.train_file_path

            
            test_file_path=self.data_ingestion_artifact.test_file_path

            
            schema_file_path=self.data_validation_artifact.schema_file_path
            logging.info("loading train and test df")
            
            train_df=DataTransformation.load_data(file_path=train_file_path , schema_file_path=schema_file_path)
            test_df=DataTransformation.load_data(file_path=train_file_path , schema_file_path=schema_file_path)
            logging.info("train and test df loaded successfully")

            schema =read_yaml(file_path=schema_file_path)
            target_column=schema[TARGET_COLUMN_KEY]

            logging.info("extracting train and test feature with target column")

            input_feature_train_df=train_df.drop(columns=[target_column], axis=1)
            target_feature_train_df=train_df[target_column]
            
            input_feature_test_df=test_df.drop(columns=[target_column], axis=1)
            target_feature_test_df=test_df[target_column]

            logging.info("extracting train and test feature with target column is successfully done")
            logging.info("started preprocessing of indipendent variables")

            input_feature_train_array=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_array=preprocessing_obj.transform(input_feature_test_df)

            logging.info("preprocessing done successfully")

            train_arr=np.c_[input_feature_train_array,np.array(target_feature_train_df)]
            test_arr=np.c_[input_feature_test_array,np.array(target_feature_test_df)]

            transformed_train_dir=self.data_transformation_config.transformed_train_dir
            transformed_test_dir=self.data_transformation_config.transformed_test_dir

            train_file_name=os.path.basename(train_file_path).replace(".csv" , ".npz")
            test_file_name=os.path.basename(test_file_path).replace(".csv" , ".npz")

            logging.info("creating transformed train file path and test file path")

            transformed_train_file_path=os.path.join(transformed_train_dir,train_file_name)
            transformed_test_file_path=os.path.join(transformed_test_dir,test_file_name)

            logging.info("saving transformed data")

            save_numpy_array_data(file_path=transformed_train_file_path , array=train_arr)
            save_numpy_array_data(file_path=transformed_test_file_path , array=test_arr)

            logging.info("saving transformed data successfully dane")
            logging.info("saving preprocessing obj")

            preprocessing_obj_file_path=self.data_transformation_config.preprocessed_object_file_path
            save_object(file_path=preprocessing_obj_file_path , obj=preprocessing_obj)
            logging.info("saving preprocessing obj is successfull")

            data_transformation_artifact=DataTransformationArtifact(
                is_Transformed=True,
                message="Data transformation successfull",
                transformed_train_file_path=transformed_train_file_path,
                transformed_test_file_path=transformed_test_file_path,
                preprocessed_object_file_path=preprocessing_obj_file_path
            )
            logging.info(f"Data transformation artifact:{data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise FailureException(e,sys) from e            