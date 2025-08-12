import sys
import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from youtube.loggers import logger
from youtube.exceptions import YException
from youtube.entity import ModelEvaluationConfig, ModelEvaluationArtifact
from youtube.utils import load_bin, save_json


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config
    
    def eval_metrics(self, y_true, y_pred):
        """Compute Root Mean Squared Error, Mean Absolute Error and R2 score"""
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        return rmse, mae, r2
    
    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        """Evaluate the Saved Model on Test data, Log metrics and save metrics locally"""
        try:
            test_data = pd.read_csv(self.config.test_data_path, header=None)

            model = load_bin(Path(self.config.model_path))

            X_test = test_data.iloc[:, :-1]
            y_test = test_data.iloc[:, -1]

            logger.info("Loaded Test Data and Model for evaluation")

            y_pred = model.predict(X_test)

            rmse, mae, r2 = self.eval_metrics(y_test, y_pred)

            logger.info(f"Model Evaluation Metrics: RMSE = {rmse:.4f}, MAE = {mae:.4f}, R2_Score = {r2:.4f}")

            scores = {
                "rmse": rmse,
                "mae": mae,
                "r2": r2
            }

            save_json(path=Path(self.config.metric_file_name), data= scores)

            logger.info(f"Saved Evaluation Metrics to {self.config.metric_file_name}")

            return ModelEvaluationArtifact(
                evaluation_score=scores
            )
        except Exception as e:
            logger.info("Exception Occured during Model Evaluation")
            raise YException(e, sys)
        