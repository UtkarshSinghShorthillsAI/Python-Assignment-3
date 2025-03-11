# main.py
import os
from src.loaders.pdf_loader import PDFLoader
from src.loaders.docx_loader import DOCXLoader
from src.loaders.ppt_loader import PPTLoader

# Import your “extractor” classes
from src.extractors.data_extractor import (
    PDFDataExtractor,
    DOCXDataExtractor,
    PPTDataExtractor
)

from src.storage.file_storage import FileStorage

def run_extraction(file_path: str):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == ".pdf":
        loader = PDFLoader(file_path)
        doc_obj = loader.load_file()  # doc_obj is a PyMuPDF Document
        extractor = PDFDataExtractor(doc_obj, file_path)
    elif ext == ".docx":
        loader = DOCXLoader(file_path)
        doc_obj = loader.load_file()  # doc_obj is a python-docx Document
        extractor = DOCXDataExtractor(doc_obj, file_path)
    elif ext == ".pptx":
        loader = PPTLoader(file_path)
        doc_obj = loader.load_file()  # doc_obj is a pptx Presentation
        extractor = PPTDataExtractor(doc_obj, file_path)
    else:
        raise ValueError("Unsupported file type.")

    # Extract:
    text_data = extractor.extract_text()
    links_data = extractor.extract_links()
    images_data = extractor.extract_images()
    tables_data = extractor.extract_tables()

    # Combine in one big dictionary for storage
    final_data = {
        "text": text_data,
        "links": links_data,
        "images": images_data,
        "tables": tables_data
    }

    # Example: file-based storage
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    storage = FileStorage()
    storage.save(final_data, base_name)


if __name__ == "__main__":
    # run_extraction("data/sample.pdf")
    run_extraction("data/sample.docx")
    # run_extraction("data/sample.pptx")
