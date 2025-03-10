from typing import Dict, Any, List, Union
from src.loaders.file_loader import FileLoader
from src.loaders.pdf_loader import PDFLoader
from src.loaders.docx_loader import DOCXLoader
from src.loaders.ppt_loader import PPTLoader

class DataExtractor:
    """Extracts text, links, images, and tables from a FileLoader instance"""

    def __init__(self, loader: FileLoader) -> None:
        if not isinstance(loader, FileLoader):
            raise TypeError("DataExtractor requires a FileLoader instance")
        self.loader = loader
        self.loader.load_file()

    def extract_text(self) -> str:
        """Extracts text from the file"""
        if isinstance(self.loader, PDFLoader):
            return "\n".join([page.get_text("text") for page in self.loader.pdf])
        elif isinstance(self.loader, DOCXLoader):
            return "\n".join([para.text for para in self.loader.doc.paragraphs if para.text])
        elif isinstance(self.loader, PPTLoader):
            return "\n".join(
                [shape.text for slide in self.loader.ppt.slides for shape in slide.shapes if hasattr(shape, "text")]
            )
        return ""

    def extract_links(self) -> List[Dict[str, Any]]:
        """Extracts hyperlinks from the file"""
        links = []

        if isinstance(self.loader, PDFLoader):
            for page_num, page in enumerate(self.loader.pdf, start=1):
                for link in page.get_links():   #type: ignore
                    if link.get("uri"):
                        links.append({"page": page_num, "text": link.get("text", ""), "url": link["uri"]})

        elif isinstance(self.loader, DOCXLoader):
            for para in self.loader.doc.paragraphs:
                for run in para.runs:
                    if run.hyperlink:
                        links.append({"text": run.text, "url": run.hyperlink.target})

        elif isinstance(self.loader, PPTLoader):
            for slide_num, slide in enumerate(self.loader.ppt.slides, start=1):
                for shape in slide.shapes:
                    if hasattr(shape, "text") and hasattr(shape, "hyperlink") and shape.hyperlink:
                        links.append({"slide": slide_num, "text": shape.text, "url": shape.hyperlink.address})

        return links

    def extract_images(self) -> List[Dict[str, Any]]:
        """Extracts images with metadata"""
        images = []

        if isinstance(self.loader, PDFLoader):
            for page_num, page in enumerate(self.loader.pdf, start=1):
                for img_index, img in enumerate(page.get_images(full=True), start=1):
                    xref = img[0]
                    base_image = self.loader.pdf.extract_image(xref)
                    images.append({
                        "page": page_num,
                        "index": img_index,
                        "width": base_image["width"],
                        "height": base_image["height"],
                        "format": base_image["ext"],
                        "image_data": base_image["image"]
                    })

        elif isinstance(self.loader, DOCXLoader):
            for rel in self.loader.doc.part.rels:
                if "image" in self.loader.doc.part.rels[rel].target_ref:
                    images.append({"image_ref": self.loader.doc.part.rels[rel].target_ref})

        elif isinstance(self.loader, PPTLoader):
            for slide_num, slide in enumerate(self.loader.ppt.slides, start=1):
                for shape in slide.shapes:
                    if shape.shape_type == 13:  # Image type
                        images.append({"slide": slide_num, "image_ref": shape.image.blob})

        return images

    def extract_tables(self) -> List[Dict[str, Any]]:
        """Extracts tables from the file"""
        tables = []

        if isinstance(self.loader, PDFLoader):
            for page_num, page in enumerate(self.loader.pdf, start=1):
                text_blocks = page.get_text("blocks")  # Gets structured text blocks
                structured_text = [block[4] for block in text_blocks]  # Extract only text
                tables.append({"page": page_num, "table_data": structured_text})

        elif isinstance(self.loader, DOCXLoader):
            for table in self.loader.doc.tables:
                table_data = [[cell.text.strip() for cell in row.cells] for row in table.rows]
                tables.append({"table_data": table_data})

        elif isinstance(self.loader, PPTLoader):
            for slide_num, slide in enumerate(self.loader.ppt.slides, start=1):
                for shape in slide.shapes:
                    if hasattr(shape, "table"):
                        table_data = [
                            [cell.text.strip() for cell in row.cells] for row in shape.table.rows
                        ]
                        tables.append({"slide": slide_num, "table_data": table_data})

        return tables

# test = DataExtractor(PDFLoader("data/sample1.pdf"))
# print(test.extract_tables())