from abc import ABC, abstractmethod
from src.extractors.data_extractor import DataExtractor

class Storage(ABC):
    """Abstract class for storing extracted data"""

    def __init__(self, extractor: DataExtractor) -> None:
        self.extractor = extractor

    @abstractmethod
    def store_data(self) -> None:
        """Method to store extracted data"""
        pass
