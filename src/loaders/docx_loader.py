from .file_loader import FileLoader
from docx import Document

class DOCXLoader(FileLoader):
    """Loader for DOCX files (just opens the file)."""

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.doc = None  # Will hold the python-docx Document

    def load_file(self):
        """
        Validate and open the DOCX file, returning the Document object.
        """
        if not self.validate_file():
            raise FileNotFoundError(f"DOCX file not found: {self.file_path}")

        try:
            self.doc = Document(self.file_path)
            print(f"DOCX loaded from {self.file_path}")
            return self.doc
        except Exception as e:
            raise RuntimeError(f"Failed to open DOCX: {e}")
