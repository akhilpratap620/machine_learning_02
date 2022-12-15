from Airfoil_prediction.entity.config_entity import DataIngestionConfig
from Airfoil_prediction.entity.artifact_entity import DataIngestionArtifact
import sys , os
from Airfoil_prediction.logger import logging
from Airfoil_prediction.exception import FailureException
import tarfile
from six.moves import urllib
from sklearn.model_selection import StratifiedShuffleSplit
from Airfoil_prediction.constant import *
from Airfoil_prediction.config.configuration import Configuration
from pathlib import Path
import csv
import pandas as pd





class DataIngestion:
    def __init__(self , data_ingestion_config:DataIngestionConfig)->None:
        try:
            logging.info(f"{'='*20} Data Ingestion Log Started.{'='*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise FailureException(e,sys) from e

    def download_data(self)->str :
        try:
            download_url = self.data_ingestion_config.dataset_download_url
            #folder location to download
            
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir
            # checking whether directory is exist or not
            
            if os.path.exists(tgz_download_dir):
                os.remove(tgz_download_dir)

            os.makedirs(tgz_download_dir , exist_ok = True)
            Airfoil_file_name = os.path.basename(download_url)

            tgz_file_path = os.path.join(tgz_download_dir ,Airfoil_file_name)
            logging.info(f"Downloading file from[{download_url}] into :[{tgz_file_path}]")

            urllib.request.urlretrieve(download_url ,tgz_file_path)

            logging.info(f"{'='*20} Downloading completed {'='*20}")
            return tgz_file_path
            
        except Exception as e:
            raise FailureException(e,sys) from e

    def extract_zip_file(self ,tgz_file_path:str):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            logging.info(f"{'='*20}making directory[{raw_data_dir}]{'='*20}")

            os.makedirs(raw_data_dir , exist_ok = True)
            logging.info(f"{'='*20}making directory --completed[{raw_data_dir}]{'='*20}")
            
            file_name = 'airfoil_self_noise.csv'

            raw_data_file_path = os.path.join(raw_data_dir , file_name)

            logging.info(f"{'='*20}started extraction of data from[{tgz_file_path}]{'='*20}")

            datContent = [i.strip().split() for i in open(tgz_file_path).readlines()]
            header =["Frequency" , "Angle of attack" , "Chord length" , "Free-stream velocity" , "Section side displacement thickness" , "Scaled Sound Pressure Level"]
            with open(raw_data_file_path, "w") as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(datContent)
                return raw_data_file_path

            logging.info(f"{'='*20} Extraction completde of data from [{tgz_file_path}]{'='*20}")    


            
        except Exception as e:
            raise FailureException(e,sys) from e

    def split_data_as_train_test(self):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            file_name = os.listdir(raw_data_dir)[0]
            Airfoil_file_path = os.path.join(raw_data_dir ,file_name)

            logging.info(f"reading Airfoil data[{Airfoil_file_path}]")

            Airfoil_data_frame =pd.read_csv( Airfoil_file_path)

            Airfoil_data_frame['dummy']=pd.cut(Airfoil_data_frame['Free-stream velocity'] , bins=[0.0 ,31.7, 39.6, 55.5,71.3] , labels=[1,2,3,4])

            
            logging.info(f"spliting the data into train test")

            split =StratifiedShuffleSplit(n_splits =1,test_size =0.2 ,random_state =42)
            
            
            for train_index , test_index in split.split(Airfoil_data_frame ,Airfoil_data_frame["dummy"]):
                
                strat_train_set = Airfoil_data_frame.loc[train_index].drop(["dummy"],axis =1)
                strat_test_set = Airfoil_data_frame.loc[test_index].drop(["dummy"],axis =1)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir ,file_name)
            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir ,file_name)

            if strat_train_set is not None :
                os.makedirs(self.data_ingestion_config.ingested_train_dir , exist_ok = True)
                logging.info(f"spliting data into training dataset[{train_file_path}]")
                strat_train_set.to_csv(train_file_path ,index = False)

            if strat_test_set is not None :
                os.makedirs(self.data_ingestion_config.ingested_test_dir , exist_ok = True)
                logging.info(f"spliting data into testing dataset[{test_file_path}]")
                strat_train_set.to_csv(test_file_path ,index = False)   

            data_ingestion_artifact=DataIngestionArtifact(


                train_file_path=train_file_path ,
                test_file_path=test_file_path ,
                is_ingested=True ,
                message ="Data_Ingestion_completed" ) 

            return data_ingestion_artifact
            logging.info(f"data ingestion [{data_ingestion_artifact}]")    
                

        except Exception  as e:
            raise FailureException(e, sys) from e         








    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            tgz_file_path = self.download_data()
            self.extract_zip_file(tgz_file_path=tgz_file_path)
            return self.split_data_as_train_test()
            
            

        except Exception as e:
            raise FailureException(e , sys) from e      

    def __del__(self):
        logging.info(f"{'='*20} Data Ingestion completed {'='*20}\n\n")           