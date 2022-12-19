from Airfoil_prediction.exception import FailureException
from Airfoil_prediction.logger import logging
from Airfoil_prediction.entity.config_entity import ModelTrainerConfig
from Airfoil_prediction.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from Airfoil_preadiction.util.util import load_numpy_array
class ModelTrainer:
    def __init__(self ,model_trainer_config:ModelTrainerConfig , data_transformation_artifact:DataTransformationArtifact):
        try:
            logging.info("{'>>'*20} model Training log started {'<<'*20}")
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise  FailureExeption(e,sys) from e



    def initiate_model_training(self)->ModelTrainerArtifact:
        try:
            transformed_train_file_path=self.data_transformation_artifact.transformed_train_file_path
            train_array=load_numpy_array(file_path=transformed_train_file_path)

            transformed_test_file_path=self.data_transformation_artifact.transformed_test_file_path
            test_array=load_numpy_array(file_path=transformed_test_file_path)

            x_train,y_train,x_test,y_test=train_array[:,:-1] , train_array[:,-1],test_array[:,:-1],test_array[: ,-1]

            model_config_file_path=self.model_trainer_config.model_config_file_path

            model_factory = ModelFactory(model_config_path=model_config_file_path)

            base_accuracy=self.model_trainer_config.base_accuracy
            



        except Exception as e:
            raise FailureException(e,sys) from e    

    