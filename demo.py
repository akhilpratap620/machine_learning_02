from Airfoil_prediction.pipeline.pipeline import Pipeline
from Airfoil_prediction.exception import FailureException
from Airfoil_prediction.logger import logging
from Airfoil_prediction.config.configuration import Configuration
from Airfoil_prediction.component.data_transformation import DataTransformation
import os , sys
def main():
    try:
        config_path = os.path.join("config","config.yaml")
        pipeline = Pipeline(Configuration(config_file_path=config_path))
        pipeline.run_pipeline()
        #pipeline.start()
        # logging.info("main function execution completed.")
        # data_transformed_config = Configuration().get_data_transformation_config()
        # print(data_transformed_config)
        # schema_file_path=r"C:\Users\somit\Downloads\project_ineuron\machine_learning_02\notebook\schema_01.yaml"
        # file_path=r"C:\Users\somit\Downloads\project_ineuron\machine_learning_02\Airfoil_prediction\artifact\data_ingestion\2022-11-22-08-17-45\ingested_data\train\airfoil_self_noise.csv"

        # df= DataTransformation.load_data(file_path=file_path,schema_file_path=schema_file_path)
        # print(df.columns)
        # print(df.dtypes)

    except Exception as e:
        logging.error(f"{e}")
        print(e)



if __name__=="__main__":
    main()