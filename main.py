from youtube.loggers import logger
from youtube.pipeline import TrainingPipeline

try:
    logger.info(">>>>>>>Data Ingestion Started <<<<<<<")
    data_ingestion = TrainingPipeline()
    data_ingestion.data_ingestion()
    logger.info(f">>>>>>> Data Ingestion Completed <<<<<<<")
except Exception as e:
    logger.exception(e)
    raise e