# src/storage/file_storage.py
import os
import csv
from typing import Dict, Any
from .storage import Storage

class FileStorage(Storage):
    """
    A simple file-based storage that writes text, links, headings,
    etc. into local files. (Images/tables are usually saved in the
    extractor stage, but we can still handle metadata here.)
    """

    def save(self, data: Dict[str, Any], file_name: str):
        output_dir = os.path.join("output", file_name)
        os.makedirs(output_dir, exist_ok=True)

        # 1) Save text
        text_data = data.get("text", {})
        text_path = os.path.join(output_dir, "extracted_text.txt")
        with open(text_path, "w", encoding="utf-8") as tf:
            for page_num, lines in text_data.get("text", {}).items():
                tf.write(f"--- Page {page_num} ---\n")
                for line in lines:
                    tf.write(line + "\n")
                tf.write("\n")

        # 2) Save headings
        headings_path = os.path.join(output_dir, "headings.txt")
        with open(headings_path, "w", encoding="utf-8") as hf:
            for page_num, hdgs in text_data.get("metadata", {}).get("headings", {}).items():
                hf.write(f"--- Page {page_num} Headings ---\n")
                for h in hdgs:
                    hf.write(h + "\n")
                hf.write("\n")

        # 3) Save links
        links_list = data.get("links", [])
        links_path = os.path.join(output_dir, "extracted_links.csv")
        with open(links_path, "w", newline="", encoding="utf-8") as lf:
            writer = csv.writer(lf)
            writer.writerow(["Page Number", "URL", "Link Text"])
            for link in links_list:
                writer.writerow([
                    link.get("page_number", ""),
                    link.get("url", ""),
                    link.get("text", "")
                ])

        # 4) Save font styles
        font_styles = text_data.get("metadata", {}).get("font_styles", [])
        font_path = os.path.join(output_dir, "font_styles.csv")
        with open(font_path, "w", newline="", encoding="utf-8") as ff:
            writer = csv.writer(ff)
            writer.writerow(["Page Number", "Text", "Font", "Size"])
            for fs in font_styles:
                writer.writerow([
                    fs.get("page_number", ""),
                    fs.get("text", ""),
                    fs.get("font", ""),
                    fs.get("size", "")
                ])

        print(f"Extraction data saved to folder: {output_dir}")
