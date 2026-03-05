from fastapi import APIRouter, UploadFile, File
from src.app.services.persona.extract_file_content import read_file

persona_router = APIRouter(prefix="/personas", tags=["personas"])

# Função que vai receber um arquivo, pode ser TXT, DOCS, PDF
# E preencher tres variaveis nome, perfil, objetivo, instrução
# Pegar o conteudo do arquivo


@persona_router.post("/creat_persona")
async def generate_persona(file: UploadFile = File(...)):
    file_path = file
    read_file(file_path)
    return
