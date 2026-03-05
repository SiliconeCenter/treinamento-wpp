# Deletar usuario
# Atualizar senha
# Alterar nome

from src.app.core.database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from src.app.security.password import get_admin_user
from src.app.models.user import User

users_router = APIRouter(prefix="/users", tags=["users"])


# Rota para deletar o usuário
@users_router.delete(
    "/{user_email}",
    responses={404: {"description": "Nenhuma usuario com {user_email} encontrado."}},
)
def delete_user(
    user_email: str,
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[dict, Depends(get_admin_user)],
):

    if admin.get("email") == user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Operação inválida: você não pode deletar sua própria conta.",
        )

    user = db.query(User).filter(User.email == user_email).first()

    if not user:
        raise HTTPException(
            status_code=404, detail=f"Nenhuma usuario com {user_email} encontrado."
        )

    db.delete(user)
    db.commit()
    return {"mensagem": "Usuário deletado"}


# Rota para aleterar as informações do uruário
