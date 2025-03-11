from abc import ABC, abstractmethod
import os

class FileLoader(ABC):
    """
    Abstract base class for loading/validating files.
    Concrete classes (PDFLoader, DOCXLoader, PPTLoader) implement load_file().
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    def validate_file(self) -> bool:
        """Check if file exists on disk."""
        return os.path.isfile(self.file_path)

    @abstractmethod
    def load_file(self):
        """Open the file and return a loaded doc/presentation object."""
        pass
