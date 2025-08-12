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

try:
    logger.info(">>>>>>>Data Validation Started <<<<<<<")
    data_validation = TrainingPipeline()
    data_validation.data_validation()
    logger.info(f">>>>>>> Data Validation Completed <<<<<<<")
except Exception as e:
    logger.exception(e)
    raise e

try:
    logger.info(">>>>>>>Data Transformation Started <<<<<<<")
    data_tranformation = TrainingPipeline()
    data_tranformation.data_tranformation()
    logger.info(f">>>>>>> Data Tranformation Completed <<<<<<<")
except Exception as e:
    logger.exception(e)
    raise e

try:
    logger.info(">>>>>>>Model Trainer Started <<<<<<<")
    model_trainer = TrainingPipeline()
    model_trainer.model_trainer()
    logger.info(f">>>>>>> Model Trainer Completed <<<<<<<")
except Exception as e:
    logger.exception(e)
    raise e

try:
    logger.info(">>>>>>>Model Evaluation Started <<<<<<<")
    model_evaluation = TrainingPipeline()
    model_evaluation.model_evaluation()
    logger.info(f">>>>>>> Model Evaluation Completed <<<<<<<")
except Exception as e:
    logger.exception(e)
    raise e