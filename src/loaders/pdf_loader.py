from .file_loader import FileLoader
import fitz  # PyMuPDF

class PDFLoader(FileLoader):
    """Loader for PDF files (just opens the file)."""

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.doc = None  # Will hold a PyMuPDF Document

    def load_file(self):
        """
        Validate and open the PDF file, returning the fitz Document object.
        """
        if not self.validate_file():
            raise FileNotFoundError(f"PDF file not found: {self.file_path}")

        try:
            self.doc = fitz.open(self.file_path)
            print(f"PDF loaded from {self.file_path}")
            return self.doc
        except Exception as e:
            raise RuntimeError(f"Failed to open PDF: {e}")
