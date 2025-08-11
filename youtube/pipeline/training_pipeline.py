import sys

from youtube.loggers import logger
from youtube.exceptions import YException
from youtube.configure import ConfigurationManager
from youtube.components import (
    DataIngestion,
    DataValidation,
)

class TrainingPipeline:
    def __init__(self):
        pass

    def data_ingestion(self):
        try:
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logger.info("Data Ingestion Complated")
            return data_ingestion_artifact
        except Exception as e:
            raise YException(e, sys)
        
    def data_validation(self):
        try:
            config = ConfigurationManager()
            data_validation_config = config.get_data_validation_config()
            data_validation = DataValidation(config=data_validation_config)
            data_validation_artifact = data_validation.validate_all_columns()
            logger.info("Data Validation Completed")
            return data_validation_artifact
        except Exception as e:
            raise YException(e, sys)