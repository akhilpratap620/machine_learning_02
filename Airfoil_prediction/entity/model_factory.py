from Airfoil_prediction.exception import FailureException
from Airfoil_prediction.logger import logging
from collection import namedtuple
from cmath import log
import importlib
from pyexpat import model
import numpy as np
import yaml
from housing.exception import HousingException
import os
import sys

from collections import namedtuple
from typing import List
from housing.logger import logging
from sklearn.metrics import r2_score,mean_squared_error



GRID_SEARCH_KEY = 'grid_search'
MODULE_KEY = 'module'
CLASS_KEY = 'class'
PARAM_KEY = 'params'
MODEL_SELECTION_KEY = 'model_selection'
SEARCH_PARAM_GRID_KEY = "search_param_grid"

InitializedModelDetail = namedtuple("InitializedModelDetail",
                                    ["model_serial_number", "model", "param_grid_search", "model_name"])

GridSearchedBestModel = namedtuple("GridSearchedBestModel", ["model_serial_number",
                                                             "model",
                                                             "best_model",
                                                             "best_parameters",
                                                             "best_score",
                                                             ])

BestModel = namedtuple("BestModel", ["model_serial_number",
                                     "model",
                                     "best_model",
                                     "best_parameters",
                                     "best_score", ])
MetricInfoArtifact = namedtuple("MetricInfoArtifact",
                                ["model_name", "model_object", "train_rmse", "test_rmse", "train_accuracy",
                                 "test_accuracy", "model_accuracy", "index_number"])


def evaluate_regression_model(model_list:list ,x_train:np.ndarray,y_train:np.ndarray,x_test:np.ndarray ,y_test:np.ndarray , base_accuracy:float=0.6)->MetricInfoArtifact:
    try:
        index =0
        metric_info_artifact=None
        for model in model_list:
            model_name= str(model)

            train_pred=model.predict(x_train)
            test_pred=model.predict(x_test)

            test_acc=r2_score(y_test ,test_pred)
            train_acc=r2score(y_train,train_pred)

            train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
            test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))

            model_accuracy = (2 * (train_acc * test_acc)) / (train_acc + test_acc)
            diff_test_train_acc = abs(test_acc - train_acc)

            logging.info(f"{'>>'*30} Score {'<<'*30}")
            logging.info(f"Train Score\t\t Test Score\t\t Average Score")
            logging.info(f"{train_acc}\t\t {test_acc}\t\t{model_accuracy}")

            logging.info(f"{'>>'*30} Loss {'<<'*30}")
            logging.info(f"Diff test train accuracy: [{diff_test_train_acc}].") 
            logging.info(f"Train root mean squared error: [{train_rmse}].")
            logging.info(f"Test root mean squared error: [{test_rmse}].")

            if model_accuracy >=base_accuracy and diff_test_train_acc < 0.05 :
                base_accuracy=model_accuracy
                metric_info_artifact=MetricInfoArtifact(
                    model_name=model_name,
                    model_object=model,
                    train_rmse=train_rmse,
                    test_rmse=test_rmse,
                    train_accuracy=train_acc,
                    test_accuracy=test_acc,
                    model_accuracy=model_accuracy,
                    index_number=index

                )
            index +=1     

            if metric_info_artifact is None:
                logging.info("no module found with higher accuracy with the base accuracy")

            return metric_info_artifact    
    except Exception as e:
        raise FailureException(e,sys) from e
    
def get_sample_model_config_yaml_file(export_dir:str):
        

                 


