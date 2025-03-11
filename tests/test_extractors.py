import unittest
import os
from src.loaders.pdf_loader import PDFLoader
from src.loaders.docx_loader import DOCXLoader
from src.loaders.ppt_loader import PPTLoader

# Import your new extractors
from src.extractors.data_extractor import (
    PDFDataExtractor,
    DOCXDataExtractor,
    PPTDataExtractor
)

class TestExtractors(unittest.TestCase):

    def setUp(self):
        self.pdf_loader = PDFLoader("data/sample.pdf")
        self.pdf_doc = self.pdf_loader.load_file()
        self.pdf_extractor = PDFDataExtractor(self.pdf_doc, "data/sample.pdf")

        self.docx_loader = DOCXLoader("data/sample.docx")
        self.docx_doc = self.docx_loader.load_file()
        self.docx_extractor = DOCXDataExtractor(self.docx_doc, "data/sample.docx")

        self.ppt_loader = PPTLoader("data/sample.pptx")
        self.ppt_doc = self.ppt_loader.load_file()
        self.ppt_extractor = PPTDataExtractor(self.ppt_doc, "data/sample.pptx")

    def test_pdf_text_extraction(self):
        text_data = self.pdf_extractor.extract_text()
        self.assertIn("text", text_data)
        self.assertIn("metadata", text_data)

    def test_pdf_links_extraction(self):
        links = self.pdf_extractor.extract_links()
        self.assertIsInstance(links, list)

    def test_docx_text_extraction(self):
        text_data = self.docx_extractor.extract_text()
        self.assertIn("text", text_data)
        self.assertIn("metadata", text_data)

    def test_docx_links_extraction(self):
        links = self.docx_extractor.extract_links()
        self.assertIsInstance(links, list)

    def test_ppt_text_extraction(self):
        text_data = self.ppt_extractor.extract_text()
        self.assertIn("text", text_data)
        self.assertIn("metadata", text_data)

    def test_ppt_links_extraction(self):
        links = self.ppt_extractor.extract_links()
        self.assertIsInstance(links, list)


if __name__ == "__main__":
    unittest.main()