import os
import csv
from src.storage.storage import Storage

class FileStorage(Storage):
    """Stores extracted data into files"""

    def __init__(self, extractor, output_dir: str = "output") -> None: #type: ignore
        super().__init__(extractor) #type: ignore   
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(f"{self.output_dir}/images", exist_ok=True)

    def store_text(self) -> None:
        """Saves extracted text to a file"""
        text = self.extractor.extract_text()
        file_path = os.path.join(self.output_dir, "extracted_text.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)

    def store_links(self) -> None:
        """Saves extracted links to a CSV file"""
        links = self.extractor.extract_links()
        file_path = os.path.join(self.output_dir, "extracted_links.csv")
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["text", "url"])
            writer.writeheader()
            writer.writerows(links)

    def store_images(self) -> None:
        """Saves extracted images to the images/ directory"""
        images = self.extractor.extract_images()
        for img in images:
            image_path = os.path.join(self.output_dir, "images", f"image_{img['index']}.{img['format']}")
            with open(image_path, "wb") as img_file:
                img_file.write(img["image_data"])

    def store_tables(self) -> None:
        """Saves extracted tables to CSV files"""
        tables = self.extractor.extract_tables()
        for idx, table in enumerate(tables, start=1):
            file_path = os.path.join(self.output_dir, f"table_{idx}.csv")
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(table["table_data"])

    def store_data(self) -> None:
        """Stores all extracted data"""
        self.store_text()
        self.store_links()
        self.store_images()
        self.store_tables()
