import os
import pypdf
from docx import Document

def extract_text_from_file(file_path: str) -> str:
    """
    Extrae texto plano de archivos PDF o DOCX.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo '{file_path}' no existe.")

    ext = os.path.splitext(file_path)[1].lower()
    extracted_text = ""

    if ext == ".pdf":
        reader = pypdf.PdfReader(file_path)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"

    elif ext in [".docx", ".doc"]:
        doc = Document(file_path)
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                extracted_text += paragraph.text + "\n"

    else:
        raise ValueError("Formato no soportado. Por favor sube un archivo .pdf o .docx")

    return extracted_text.strip()