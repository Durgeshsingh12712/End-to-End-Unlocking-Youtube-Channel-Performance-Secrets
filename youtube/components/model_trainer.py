import os, sys
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

from youtube.loggers import logger
from youtube.exceptions import YException
from youtube.entity import ModelTrainerConfig, ModelTrainerArtifact
from youtube.utils import save_bin

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config
    
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_data = pd.read_csv(self.config.train_data_path, header=None)
            test_data = pd.read_csv(self.config.test_data_path, header=None)

            logger.info("Split training and test input data")
            X_train, y_train, X_test, y_test = (
                train_data.iloc[:, :-1],
                train_data.iloc[:, -1],
                test_data.iloc[:, :-1],
                test_data.iloc[:, -1]
            )

            models = {
                "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
                "Linear Regression": LinearRegression(),
            }

            model_report = {}

            for i in range(len(list(models))):
                model = list(models.values())[i]
                model.fit(X_train, y_train)

                y_train_pred = model.predict(X_train)
                y_test_pred = model.predict(X_test)

                train_model_score = r2_score(y_train, y_train_pred)
                test_model_score = r2_score(y_test, y_test_pred)

                model_report[list(models.keys())[i]] = test_model_score
            
            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise YException("NO Best Model Found", sys)

            logger.info(f"Best Found Model on Both Training and Testing Dataset")

            save_bin(
                data=best_model,
                path=os.path.join(self.config.root_dir, self.config.model_name)
            )

            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test, predicted)
            logger.info(f"Best R2 Score: {r2_square}")

            return ModelTrainerArtifact(
                trained_model_file_path=best_model
            )
        except Exception as e:
            raise YException(e, sys)