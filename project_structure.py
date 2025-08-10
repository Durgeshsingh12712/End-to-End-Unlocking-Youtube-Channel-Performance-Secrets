import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

project_name = "youtube"

list_of_files = [
    ".github/workflows/.gitkeep",
    "config/config.yaml",
    "config/params.yaml",
    f"{project_name}/__init__.py",
    f"{project_name}/loggers/__init__.py",
    f"{project_name}/loggers/logger.py",
    f"{project_name}/exceptions/__init__.py",
    f"{project_name}/exceptions/YExpection.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/tools.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/config_entity.py",
    f"{project_name}/entity/artifacts_entity.py",
    f"{project_name}/constants/__init__.py",
    f"{project_name}/constants/constant.py",
    f"{project_name}/configure/__init__.py",
    f"{project_name}/configure/configuration.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/data_ingestion.py",
    f"{project_name}/components/data_validation.py",
    f"{project_name}/components/data_transformation.py",
    f"{project_name}/components/model_trainer.py",
    f"{project_name}/components/model_evaluation.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/pipeline/training_pipeline.py",
    f"{project_name}/pipeline/prediction_pipeline.py",
    "notebooks/research.ipynb",
    "templates/index.html",
    "templates/home.html",
    "main.py",
    "app.py",
    "requirements.txt",
    "setup.py"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    
    filedir, filename = os.path.split(filepath)
    
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating Directory: {filedir} for the file {filename}")
    
    try:
        if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
            with open(filepath, "w") as f:
                pass
            logging.info(f"Creating Empty File: {filepath}")
        else:
            logging.info(f"{filepath} already exists and is not empty")
    except (OSError, PermissionError) as e:
        logging.error(f"Error creating file {filepath}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error with {filepath}: {e}")