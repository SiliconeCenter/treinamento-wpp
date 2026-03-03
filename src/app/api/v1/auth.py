from fastapi import APIRouter, Depends, HTTPException, status
from src.app.core.database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from src.app.models.user import User
from src.app.schemas.auth.user_create import UserCreate
from src.app.security.password import get_password_hash


auth_router = APIRouter(prefix="/auth", tags=["auth"])


# Rota de criar e fazer login
@auth_router.post("/", responses={400: {"description": "Email já cadastrado"}})
def sing_up(db: Annotated[Session, Depends(get_db)], user_data: UserCreate):
    # Verificando se o usuario existe.
    usuario_existe = db.query(User).filter(User.email == user_data.email).first()

    if usuario_existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado"
        )

    # Aqui vou criar a criptografia
    password_hased = get_password_hash(user_data.password)

    new_user = User(
        nome=user_data.nome,
        email=user_data.email,
        password_hash=password_hased,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuário criado com sucesso!", "user_id": new_user.id}
