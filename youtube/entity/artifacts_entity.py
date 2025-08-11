from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionArtifact:
    trained_file_path: Path

@dataclass
class DataValidationArtifact:
    validation_status: bool

@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: Path
    transformed_train_file_path: Path
    transformed_test_file_path: Path