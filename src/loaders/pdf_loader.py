import fitz  # type: ignore PyMuPDF
from .file_loader import FileLoader

class PDFLoader(FileLoader):
    """Loads and processes PDF files using PyMuPDF"""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.pdf: fitz.Document = fitz.Document()  # Type hint for PyMuPDF document

    def load_file(self) -> None:
        """Opens a PDF file using PyMuPDF"""
        try:
            self.pdf = fitz.open(self.file_path)
            print("PDF loaded")
        except Exception as e:
            raise RuntimeError(f"Failed to open PDF: {e}")


# test = PDFLoader("data/sample1.pdf")
# test.load_file()
