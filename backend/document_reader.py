import os

from pypdf import PdfReader
from docx import Document


def extract_text_from_file(file_path: str) -> str:

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    extension = os.path.splitext(file_path)[1].lower()


    # ==========================================
    # TXT
    # ==========================================

    if extension == ".txt":

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            return file.read()


    # ==========================================
    # PDF
    # ==========================================

    if extension == ".pdf":

        reader = PdfReader(file_path)

        pages = []

        for page in reader.pages:

            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n\n".join(pages)


    # ==========================================
    # DOCX
    # ==========================================

    if extension == ".docx":

        document = Document(file_path)

        paragraphs = []

        for paragraph in document.paragraphs:

            if paragraph.text.strip():

                paragraphs.append(
                    paragraph.text
                )

        return "\n\n".join(paragraphs)


    # ==========================================
    # UNSUPPORTED FILE
    # ==========================================

    raise ValueError(
        f"Unsupported file type: {extension}"
    )