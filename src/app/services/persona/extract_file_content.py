import shutil
from pathlib import Path
from fastapi import UploadFile
import pathlib
from PyPDF2 import PdfReader
import docx


def read_file(file: UploadFile):
    # verifica a extensão do arquivo:
    upload_dir = Path("data/")
    upload_dir.mkdir(parents=True, exist_ok=True)  # Cria a pasta se não existir

    dest = upload_dir / file.filename
    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    path = str(dest)

    tipo = pathlib.Path(path).suffix
    print(tipo)

    match tipo:
        case ".txt":
            with open(path, "r", encoding="utf-8") as f:
                conteudo = f.read()
                return conteudo

        case ".pdf":
            reader = PdfReader(path)
            texto = ""

            for pagina in reader.pages:
                texto += pagina.extract_text() + "\n"

            return texto

        case ".doc":
            doc = docx.Document(path)
            texto = ""

            for paragrafo in doc.paragraphs:
                texto += paragrafo.text + "\n"

            return texto
        case _:
            return "O tipo do arquivo não é suportado!"
