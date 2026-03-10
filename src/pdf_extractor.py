import pdfplumber

class PDFExtractor:

    def extract_text(self, pdf_path: str) -> str:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    def extract_tables(self, pdf_path: str):
        tables = []

        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                page_tables = page.extract_tables()

                for table in page_tables:
                    tables.append({
                        "page": page_num + 1,
                        "data": table
                    })

        return tables