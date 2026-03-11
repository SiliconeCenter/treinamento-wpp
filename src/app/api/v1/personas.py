from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from src.app.core.database import get_db
from src.app.models.models_treinmento_wpp import Persona
from src.app.schemas.persona.persona_create import PersonaResponse
from src.app.security.password import get_admin_user
from src.app.services.persona.estrutured_data_ia import preencher_persona
from src.app.services.persona.extract_file_content import read_file

persona_router = APIRouter(prefix="/personas", tags=["personas"])


@persona_router.post(
    "/creat_persona",
    response_model=PersonaResponse,
    status_code=status.HTTP_201_CREATED,
)
def generate_persona(
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[dict, Depends(get_admin_user)],
    file: UploadFile = File(...),
):
    file_path = file
    conteudo = read_file(file_path)
    result = preencher_persona(conteudo)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="A IA não conseguiu processar o arquivo. Verifique o conteúdo.",
        )

    nova_persona = Persona(
        nome=result.nome,
        perfil=result.perfil,
        objetivo=result.objetivo,
        instrucao=result.instrucao,
    )

    try:
        db.add(nova_persona)
        db.commit()
        db.refresh(nova_persona)
        return nova_persona

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar no banco: {str(e)}",
        )


@persona_router.delete(
    "/delete_persona/{persona_id}",
    responses={404: {"description": "Nenhuma persona com esse id encontrado."}},
)
def delete_persona(
    persona_id: str,
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[dict, Depends(get_admin_user)],
):

    persona = db.query(Persona).filter(Persona.id == persona_id).first()

    if not persona:
        raise HTTPException(
            status_code=404, detail="Nenhuma persona com esse id encontrado."
        )

    db.delete(persona)
    db.commit()
    return {"mensagem": "Persona deletada"}
