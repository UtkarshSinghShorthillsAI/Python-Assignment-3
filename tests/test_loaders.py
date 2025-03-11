import unittest
import os
from src.loaders.pdf_loader import PDFLoader
from src.loaders.docx_loader import DOCXLoader
from src.loaders.ppt_loader import PPTLoader

class TestLoaders(unittest.TestCase):

    def setUp(self):
        # Provide paths to small test files in your 'data/' folder
        self.pdf_path = "data/sample.pdf"
        self.docx_path = "data/sample.docx"
        self.pptx_path = "data/sample.pptx"

    def test_pdf_loader(self):
        loader = PDFLoader(self.pdf_path)
        self.assertTrue(loader.validate_file())
        doc_obj = loader.load_file()
        self.assertIsNotNone(doc_obj)  # PyMuPDF Document

    def test_docx_loader(self):
        loader = DOCXLoader(self.docx_path)
        self.assertTrue(loader.validate_file())
        doc_obj = loader.load_file()
        self.assertIsNotNone(doc_obj)  # python-docx Document

    def test_ppt_loader(self):
        loader = PPTLoader(self.pptx_path)
        self.assertTrue(loader.validate_file())
        doc_obj = loader.load_file()
        self.assertIsNotNone(doc_obj)  # python-pptx Presentation


if __name__ == "__main__":
    unittest.main()