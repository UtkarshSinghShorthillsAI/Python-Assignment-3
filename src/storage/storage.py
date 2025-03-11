# src/storage/storage.py

from abc import ABC, abstractmethod
from typing import Dict, Any

class Storage(ABC):
    """
    Abstract base class for storing extracted data.
    Concrete classes:
      - FileStorage: saves extracted data to files.
      - SQLStorage: saves extracted data to an SQL database.
    """

    @abstractmethod
    def save(self, data: Dict[str, Any], file_name: str):
        """
        Save the extracted data in the desired format.
        """
        pass
