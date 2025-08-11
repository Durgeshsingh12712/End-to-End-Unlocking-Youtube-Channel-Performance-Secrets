import sys
import pandas as pd

from youtube.loggers import logger
from youtube.exceptions import YException
from youtube.entity import DataValidationConfig

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_columns(self) -> bool:
        try:
            validation_status = None
            
            data = pd.read_csv(self.config.unzip_data_dir)
            all_cols = list(data.columns)

            all_schema = {
                'ID': 'int64',
                'Video Duration': 'float64',
                'Days Since Publish': 'int64',
                'Day': 'int64',
                'Month': 'int64',
                'Year': 'int64',
                'Revenue per 1000 Views (USD)': 'float64',
                'Monetized Playbacks (Estimate)': 'float64',
                'Views': 'float64',
                'Watch Time (hours)': 'float64',
                'Subscribers': 'float64',
                'Estimated Revenue (USD)': 'float64',
                'Impressions': 'float64'
            }

            for col in all_schema.keys():
                if col not in all_cols:
                    validation_status = False
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"Validation status: {validation_status}")
                    return validation_status

            validation_status = True
            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation status: {validation_status}")

            return validation_status
        
        except Exception as e:
            logger.error("Error to validate")
            raise YException(e, sys)