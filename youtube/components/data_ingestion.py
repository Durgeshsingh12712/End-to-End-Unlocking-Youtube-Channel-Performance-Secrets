import os, sys
import urllib.request as request

from youtube.loggers import logger
from youtube.exceptions import YException
from youtube.entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
    
    def download_file(self):
        try:
            if not os.path.exists(self.config.local_data_file):
                filename, header = request.urlretrieve(
                    url=self.config.source_URL,
                    filename=self.config.local_data_file
                )
                logger.info(f"{filename} download! with following info: \n{header}")
            else:
                logger.info(f"File already exist of size: {os.path.getsize(self.config.local_data_file)}")
        except Exception as e:
            raise YException(e, sys)

    def initiate_data_ingestion(self):
          try:
              logger.info("Start Data Ingestion")
              self.download_file()
              logger.info("Data Ingestion Completed")

              return self.config.local_data_file
          except Exception as e:
              raise YException(e, sys)
          