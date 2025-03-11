import unittest
import os
import shutil
from src.storage.file_storage import FileStorage
from src.storage.sql_storage import SQLStorage

class TestStorage(unittest.TestCase):

    def setUp(self):
        # Prepare some fake data that mimics extractor output
        self.sample_data = {
            "text": {
                "text": {
                    1: ["Hello world!", "Sample line."],
                    2: ["Another page text"]
                },
                "metadata": {
                    "headings": {1: ["Heading 1"]},
                    "font_styles": [
                        {"page_number": 1, "text": "Hello world!", "font": "Arial", "size": 12}
                    ]
                }
            },
            "links": [
                {"page_number": 1, "url": "http://example.com", "text": "Example"}
            ],
            "images": [
                {"page_number": 1, "image_path": "some/path/image.png"}
            ],
            "tables": [
                {"page_number": 1, "table_data": [["Cell1","Cell2"]], "table_path": "some/path/table1.csv"}
            ]
        }
        self.file_name = "test_doc"

        # Clean up output folders before each run
        if os.path.exists("final_output"):
            shutil.rmtree("final_output")
        if os.path.exists("test_data.db"):
            os.remove("test_data.db")

    def test_file_storage(self):
        storage = FileStorage()
        storage.save(self.sample_data, self.file_name)

        # Check that files were created
        out_dir = os.path.join("final_output", self.file_name)
        self.assertTrue(os.path.isdir(out_dir))
        self.assertTrue(os.path.isfile(os.path.join(out_dir, "extracted_text.txt")))
        self.assertTrue(os.path.isfile(os.path.join(out_dir, "extracted_links.csv")))

    def test_sql_storage(self):
        storage = SQLStorage(db_path="test_data.db")
        storage.save(self.sample_data, self.file_name)

        # Check that db file exists
        self.assertTrue(os.path.isfile("test_data.db"))

if __name__ == "__main__":
    unittest.main()
