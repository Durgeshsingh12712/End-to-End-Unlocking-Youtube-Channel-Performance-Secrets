import sys
import pandas as pd
from pathlib import Path

from youtube.loggers import logger
from youtube.exceptions import YException
from youtube.utils import load_bin


class PredictionPipeline:
    def __init__(self, model_path: Path, preprocessor_path: Path):
        try:
            model_path = "artifacts/model_trainer/model.pkl"
            preprocessor_path = "artifacts/data_transformation/preprocessor.pkl"
            self.model = load_bin(Path(model_path))
            self.preprocessor = load_bin(Path(preprocessor_path))
            logger.info(f"Loaded Model From {model_path} and Preprocessor from {preprocessor_path}")
        except Exception as e:
            logger.error("Failed to Load Model or Preprocessor")
            raise YException(e, sys)
        
    def predict(self, features: pd.DataFrame):
        try:
            logger.info(f"Received Features for prediction: {features.head()}")

            data_scaled = self.preprocessor.transform(features)
            logger.info("Applied preprocessing on input features.")

            preds = self.model.predict(data_scaled)
            logger.info(f"Prediction Completed succesfully, Output: {preds}")

            return preds
        except Exception as e:
            logger.error(f"Exception occured during prediction")
            raise YException(e, sys)

class CustomData:
    def __init__(
        self,
        video_duration: float,
        days_since_publish: int,
        day: int,
        month: int,
        year: int,
        revenue_per_1000_views: float,
        monetized_playbacks: float,
        views: float,
        watch_time_hours: float,
        subscribers: float,
        impressions: float,
        video_thumbnail_ctr: float,
        average_view_percentage: float,
        average_view_duration: float,
        day_of_week: int,
    ):
        self.video_duration = video_duration
        self.days_since_publish = days_since_publish
        self.day = day
        self.month = month
        self.year = year
        self.revenue_per_1000_views = revenue_per_1000_views
        self.monetized_playbacks = monetized_playbacks
        self.views = views
        self.watch_time_hours = watch_time_hours
        self.subscribers = subscribers
        self.impressions = impressions
        self.video_thumbnail_ctr = video_thumbnail_ctr
        self.average_view_percentage = average_view_percentage
        self.average_view_duration = average_view_duration
        self.day_of_week = day_of_week
    
    def get_data_as_data_frame(self) -> pd.DataFrame:
        try:
            data = {
                "Video Duration": [self.video_duration],
                "Days Since Publish": [self.days_since_publish],
                "Day": [self.day],
                "Month": [self.month],
                "Year": [self.year],
                "Revenue per 1000 Views (USD)": [self.revenue_per_1000_views],
                "Monetized Playbacks (Estimate)": [self.monetized_playbacks],
                "Views": [self.views],
                "Watch Time (hours)": [self.watch_time_hours],
                "Subscribers": [self.subscribers],
                "Impressions": [self.impressions],
                "Video Thumbnail CTR (%)": [self.video_thumbnail_ctr],
                "Average View Percentage (%)": [self.average_view_percentage],
                "Average View Duration": [self.average_view_duration],
                "Day of Week": [self.day_of_week],
            }
            df = pd.DataFrame(data)
            logger.info(f"Created DataFrame from input Data: {df.head()}")
            return df
        
        except Exception as e:
            logger.error("Error while creating Dataframe from input data")
            raise YException(e, sys)
