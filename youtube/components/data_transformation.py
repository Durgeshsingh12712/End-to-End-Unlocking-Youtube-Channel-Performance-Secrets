import sys
import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

from youtube.loggers import logger
from youtube.exceptions import YException
from youtube.entity import DataTransformationConfig, DataTransformationArtifact
from youtube.utils import save_bin


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def get_data_transformation_object(self):
        try:
            numerical_columns = [
                'Video Duration', 'Days Since Publish', 'Day', 'Month', 'Year',
                'Revenue per 1000 Views (USD)', 'Monetized Playbacks (Estimate)',
                'Views', 'Watch Time (hours)', 'Subscribers', 'Impressions',
                'Video Thumbnail CTR (%)', 'Average View Percentage (%)',
                'Average View Duration'
            ]

            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]

            )

            preprocessor = ColumnTransformer([
                ("num_pipeline", num_pipeline, numerical_columns)
            ])

            return preprocessor
        
        except Exception as e:
            raise YException(e, sys)
    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            train_df = pd.read_csv(self.config.data_path)
            logger.info("Read Train and Test Data Completed")

            # Handle DataTime Conversion
            if 'Video Publish Time' in train_df.columns:
                train_df['Video Publish Time'] = pd.to_datetime(train_df['Video Publish Time'])
                train_df['Publish Year'] = train_df['Video Publish Time'].dt.year
                train_df['Publish Month'] = train_df['Video Publish Time'].dt.month
                train_df['Publish Day'] = train_df['Video Publish Time'].dt.day
                train_df = train_df.drop(columns=['Video Publish Time'])
            
            if 'Day of Week' in train_df.columns:
                label_encoder = LabelEncoder()
                train_df['Day of Week'] = label_encoder.fit_transform(train_df['Day of Week'])

            logger.info("Obtaining Preprocessing Object")
            preprocessing_obj = self.get_data_transformation_object()

            target_column_name = "Estimated Revenue (USD)"

            columns_to_drop = ['ID'] if 'ID' in train_df.columns else []

            input_feature_train_df = train_df.drop(columns=[target_column_name] + columns_to_drop, axis=1)
            target_feature_train_df = train_df[target_column_name]

            logger.info("Applying Preprocessing Object On Training DataFrame")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)

            train_arr, test_arr, train_target, test_target = train_test_split(
                input_feature_train_arr, target_feature_train_df,
                test_size=0.2, random_state=42
            )

            train_arr = np.c_[train_arr, np.array(train_target)]
            test_arr = np.c_[test_arr, np.array(test_target)]

            logger.info("Saved Preprocessing Object")

            save_bin(
                data=preprocessing_obj,
                path=Path(self.config.preprocessor_obj_file_path)
            )

            train_df_transformed = pd.DataFrame(train_arr)
            test_df_transformed = pd.DataFrame(test_arr)

            train_df_transformed.to_csv(self.config.transformed_train_file_path, index=False, header=False)
            test_df_transformed.to_csv(self.config.transformed_test_file_path, index=False, header=False)

            return DataTransformationArtifact(
                transformed_object_file_path=self.config.preprocessor_obj_file_path,
                transformed_train_file_path=train_arr,
                transformed_test_file_path=test_arr
            )
        except Exception as e:
            raise YException(e, sys)