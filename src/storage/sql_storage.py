import os
import sqlite3
import json
from typing import Dict, Any, List, Union
from .storage import Storage  # your abstract base class

class SQLStorage(Storage):
    """
    Concrete class for SQL-based storage (using SQLite). Stores text, headings,
    links, images, tables, etc. in relational tables.
    """

    def __init__(self, db_path="extracted_data.db"):
        """
        Initialize SQLStorage with a path to the SQLite database.
        """
        self.db_path = db_path
        self._create_tables()

    def _create_tables(self):
        """
        Create the necessary database tables if they do not exist already.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Documents: top-level table for each file processed
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')

        # Document text: stores text content, one row per page
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS document_text (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER,
                page_number INTEGER,
                content TEXT,
                FOREIGN KEY(document_id) REFERENCES documents(id)
            );
        ''')

        # Document headings: store headings, one row per heading
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS document_headings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER,
                page_number INTEGER,
                heading TEXT,
                FOREIGN KEY(document_id) REFERENCES documents(id)
            );
        ''')

        # Document links: store hyperlinks, one row per link
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS document_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER,
                page_number INTEGER,
                url TEXT,
                link_text TEXT,
                shape_name TEXT,
                FOREIGN KEY(document_id) REFERENCES documents(id)
            );
        ''')

        # Document images: store extracted image metadata, one row per image
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS document_images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER,
                page_number INTEGER,
                image_path TEXT,
                alt_text TEXT,
                FOREIGN KEY(document_id) REFERENCES documents(id)
            );
        ''')

        # Document tables: store table data (as JSON) plus CSV path
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS document_tables (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER,
                page_number INTEGER,
                table_data TEXT,
                table_path TEXT,
                FOREIGN KEY(document_id) REFERENCES documents(id)
            );
        ''')

        # Document font styles: store run-level font info
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS document_font_styles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER,
                page_number INTEGER,
                text_content TEXT,
                font_name TEXT,
                font_size REAL,
                FOREIGN KEY(document_id) REFERENCES documents(id)
            );
        ''')

        conn.commit()
        conn.close()

    def save(self, data: Dict[str, Any], file_name: str):
        """
        Save the extracted data dictionary for one file into the SQLite DB.

        Args:
            data: {
               "text": { "text": { page_num: [str, str, ...], ... },
                         "metadata": {"headings": {...}, "font_styles": [...], ...}
                       },
               "links": [...],
               "images": [...],
               "tables": [...]
            }
            file_name: "my_document" (base name, or however you prefer)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # 1) Insert a row into documents to represent this file
            cursor.execute(
                "INSERT INTO documents (file_name) VALUES (?);",
                (file_name,)
            )
            document_id = cursor.lastrowid

            # 2) Handle text
            text_data = data.get("text", {})
            #   => text_data["text"] is dict of page_num -> list of lines
            pages_dict = text_data.get("text", {})
            for page_num, lines_list in pages_dict.items():
                combined_text = "\n".join(lines_list)
                cursor.execute('''
                    INSERT INTO document_text (document_id, page_number, content)
                    VALUES (?, ?, ?);
                ''', (document_id, page_num, combined_text))

            # 3) Handle headings
            headings_dict = text_data.get("metadata", {}).get("headings", {})
            for page_num, heading_list in headings_dict.items():
                for heading_str in heading_list:
                    cursor.execute('''
                        INSERT INTO document_headings (document_id, page_number, heading)
                        VALUES (?, ?, ?);
                    ''', (document_id, page_num, heading_str))

            # 4) Handle links
            links_list = data.get("links", [])
            for link in links_list:
                cursor.execute('''
                    INSERT INTO document_links (document_id, page_number, url, link_text, shape_name)
                    VALUES (?, ?, ?, ?, ?);
                ''', (
                    document_id,
                    link.get("page_number", 0),
                    link.get("url", ""),
                    link.get("text", ""),
                    link.get("shape_name", "")
                ))

            # 5) Handle images
            images_list = data.get("images", [])
            for img in images_list:
                cursor.execute('''
                    INSERT INTO document_images (document_id, page_number, image_path, alt_text)
                    VALUES (?, ?, ?, ?);
                ''', (
                    document_id,
                    img.get("page_number", 0),
                    img.get("image_path", ""),
                    img.get("alt_text", "")
                ))

            # 6) Handle tables
            tables_list = data.get("tables", [])
            for tbl in tables_list:
                # Convert the table data into JSON if present
                table_data_json = ""
                if "table_data" in tbl:
                    table_data_json = json.dumps(tbl["table_data"])
                cursor.execute('''
                    INSERT INTO document_tables (document_id, page_number, table_data, table_path)
                    VALUES (?, ?, ?, ?);
                ''', (
                    document_id,
                    tbl.get("page_number", 0),
                    table_data_json,
                    tbl.get("table_path", "")
                ))

            # 7) Handle font styles
            font_styles_list = text_data.get("metadata", {}).get("font_styles", [])
            for fs in font_styles_list:
                cursor.execute('''
                    INSERT INTO document_font_styles 
                        (document_id, page_number, text_content, font_name, font_size)
                    VALUES (?, ?, ?, ?, ?);
                ''', (
                    document_id,
                    fs.get("page_number", 0),
                    fs.get("text", ""),
                    fs.get("font", ""),
                    fs.get("size", 0)
                ))

            conn.commit()
            print(f"[SQLStorage] Successfully saved data for '{file_name}' to {self.db_path}.")

        except Exception as e:
            conn.rollback()
            print(f"[SQLStorage] Error saving data to database: {e}")

        finally:
            conn.close()
