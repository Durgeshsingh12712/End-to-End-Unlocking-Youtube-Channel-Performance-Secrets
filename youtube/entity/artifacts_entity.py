from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionArtifact:
    trained_file_path: Path

@dataclass
class DataValidationArtifact:
    validation_status: bool