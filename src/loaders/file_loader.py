from abc import ABC, abstractmethod
import os

class FileLoader(ABC):
    """Abstract base class for loading files"""

    def __init__(self, file_path: str) -> None:
        self.file_path: str = file_path
        self.validate_file()

    def validate_file(self) -> None:
        """Check if the file exists and has the correct format"""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")

    @abstractmethod
    def load_file(self) -> None:
        """Method to be implemented by concrete classes"""
        pass
