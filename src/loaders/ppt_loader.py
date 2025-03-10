import pptx
from .file_loader import FileLoader

class PPTLoader(FileLoader):
    """Loads and processes PPTX files using python-pptx"""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.ppt: pptx.Presentation = pptx.Presentation()  # type: ignore
    def load_file(self) -> None:
        """Opens a PPTX file using python-pptx"""
        try:
            self.ppt = pptx.Presentation(self.file_path)
            print("PPTX loaded")
        except Exception as e:
            raise RuntimeError(f"Failed to open PPTX: {e}")
        
# test = PPTLoader("data/samplepptx.pptx")
# test.load_file()
