import os
import sys
from src.loaders.pdf_loader import PDFLoader
from src.loaders.docx_loader import DOCXLoader
from src.loaders.ppt_loader import PPTLoader

from src.extractors.data_extractor import (
    PDFDataExtractor,
    DOCXDataExtractor,
    PPTDataExtractor
)

from src.storage.file_storage import FileStorage
from src.storage.sql_storage import SQLStorage

def run_extraction(file_path: str):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == ".pdf":
        loader = PDFLoader(file_path)
        doc_obj = loader.load_file()
        extractor = PDFDataExtractor(doc_obj, file_path)
    elif ext == ".docx":
        loader = DOCXLoader(file_path)
        doc_obj = loader.load_file()
        extractor = DOCXDataExtractor(doc_obj, file_path)
    elif ext == ".pptx":
        loader = PPTLoader(file_path)
        doc_obj = loader.load_file()
        extractor = PPTDataExtractor(doc_obj, file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    text_data = extractor.extract_text()
    links_data = extractor.extract_links()
    images_data = extractor.extract_images()
    tables_data = extractor.extract_tables()

    final_data = {
        "text": text_data,
        "links": links_data,
        "images": images_data,
        "tables": tables_data
    }

    base_name = os.path.splitext(os.path.basename(file_path))[0]

    # File-based storage
    file_storage = FileStorage()
    file_storage.save(final_data, base_name)

    # SQL-based storage
    sql_storage = SQLStorage(db_path="extracted_data.db")
    sql_storage.save(final_data, base_name)

    print(f"Extraction complete for: {file_path}")

if __name__ == "__main__":
    # Use sys.argv to check if a custom path was provided
    if len(sys.argv) > 1:
        input_file = sys.argv[1]  # user-provided path
    else:
        # fallback if no argument given
        input_file = "data/sample.pdf"

    run_extraction(input_file)
