import docx
from .file_loader import FileLoader

class DOCXLoader(FileLoader):
    """Loads and processes DOCX files using python-docx"""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.doc: docx.Document = docx.Document()  # type: ignore # Type hint for python-docx document

    def load_file(self) -> None:
        """Opens a DOCX file using python-docx"""
        try:
            self.doc = docx.Document(self.file_path)
            print("DOCX loaded")
        except Exception as e:
            raise RuntimeError(f"Failed to open DOCX: {e}")
        
# test = DOCXLoader("data/demo.docx")
# test.load_file()
