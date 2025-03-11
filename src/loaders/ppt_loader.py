from .file_loader import FileLoader
from pptx import Presentation

class PPTLoader(FileLoader):
    """Loader for PPTX files (just opens the file)."""

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.prs = None  # Will hold the python-pptx Presentation

    def load_file(self):
        """
        Validate and open the PPTX file, returning the Presentation object.
        """
        if not self.validate_file():
            raise FileNotFoundError(f"PPTX file not found: {self.file_path}")

        try:
            self.prs = Presentation(self.file_path)
            print(f"PPTX loaded from {self.file_path}")
            return self.prs
        except Exception as e:
            raise RuntimeError(f"Failed to open PPTX: {e}")
