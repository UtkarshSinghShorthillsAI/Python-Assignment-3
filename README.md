# Document Extraction & Storage

This assignment demonstrates how to:
1. **Load** PDF, DOCX, and PPTX files.
2. **Extract** text, links, images, and tables with metadata.
3. **Store** the extracted data either in files or in an SQL database.

---

## Project Structure

```
.
├── data
│   ├── sample.pdf
│   ├── sample.docx
│   └── sample.pptx
├── output
├── src
│   ├── loaders
│   │   ├── file_loader.py
│   │   ├── pdf_loader.py
│   │   ├── docx_loader.py
│   │   └── ppt_loader.py
│   ├── extractors
│   │   └── data_extractor.py
│   └── storage
│       ├── storage.py
│       ├── file_storage.py
│       └── sql_storage.py
├── tests
│   ├── test_loaders.py
│   ├── test_extractors.py
│   └── test_storage.py
├── main.py
├── README.md
└── requirements.txt
```

- **`data/`**: Contains sample input files for testing (PDF, DOCX, PPTX).  
- **`src/loaders/`**: Classes to open/validate different file types.  
- **`src/extractors/`**: Classes that handle all extraction logic from the loaded documents.  
- **`src/storage/`**: Classes to store extracted data (file-based or SQL-based).  
- **`tests/`**: Unit tests for loaders, extractors, and storage modules.  
- **`main.py`**: Optional entry point showing how to tie everything together.  

---

## Getting Started

1. **Clone this repository** (or download the ZIP):
   ```bash
   git clone https://github.com/your-username/document-extraction.git
   cd python-assignment-3
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Typical requirements include:
   - `python-docx`
   - `python-pptx`
   - `PyMuPDF` (also referred to as `fitz`)
   - `pdfplumber`
   - `Pillow`
   - `unittest` or `pytest` (for tests)
   - `sqlite3` (bundled with Python but ensure your environment supports it)

3. **Verify folder structure** so that `data/` contains the input files you want to test with (`.pdf`, `.docx`, `.pptx`).

---

## Usage

### 1) Running Extraction with `main.py`

If you have a `main.py` that demonstrates loading and extracting, you can run:
```bash
python main.py
```
Inside `main.py`, you might specify which file to process or accept a command-line argument, for example:
```bash
python main.py data/sample.pdf
```
**Results**:
- **Extracted data** goes into folders like `output/sample/images/`, etc. if you’re using `FileStorage`.

### 2) Storing Data in SQL

If you prefer storing extracted data in an SQLite database:

1. In your code, create an instance of `SQLStorage`:
   ```python
   from src.storage.sql_storage import SQLStorage
   storage = SQLStorage(db_path="extracted_data.db")
   ```
2. After extraction, call:
   ```python
   storage.save(extracted_data, "sample_file")
   ```
3. A file named `extracted_data.db` will appear. You can open it with any SQLite browser or by using `sqlite3` on the command line.

---

## Running Tests

We use **unittest** for testing. Each module (loaders, extractors, storage) has a corresponding test file in `tests/`.  

To run **all** tests at once:
```bash
python -m unittest discover -s tests
```
Or run a specific file:
```bash
python -m unittest tests/test_loaders.py
```

---

## Troubleshooting

- **WMF/EMF Image Errors**: If you see `cannot find loader for this WMF file`, it’s because Pillow doesn’t natively handle WMF. You can either skip such images or convert them to PNG/JPEG within PowerPoint.
- **Missing Dependencies**: Ensure you’ve installed everything from `requirements.txt`. If you are missing system libraries (e.g., on Linux for PyMuPDF), follow the library’s installation instructions.
- **File Not Found**: Double-check your path: for example, `data/sample.pdf` should exist if you’re passing that into the loaders.

---

**End of README**

