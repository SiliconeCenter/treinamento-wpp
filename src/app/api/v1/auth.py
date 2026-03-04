from fastapi import APIRouter, Depends, HTTPException, status
from src.app.core.database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from src.app.models.user import User
from src.app.schemas.auth.user_create import UserCreate
from src.app.security.password import (
    get_password_hash,
    verify_password,
    criar_token_acesso,
)
from fastapi.security import OAuth2PasswordRequestForm


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


# Roda de login.
@auth_router.post(
    "/sign_in",
    responses={
        401: {"description": "E-mail ou senha incorretos"},
        403: {"description": "Conta inativa"},
    },
)
def sing_in(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    # O OAuth2PasswordRequestForm usa 'username', então buscamos pelo email lá
    usuario = db.query(User).filter(User.email == data.username).first()

    if not usuario or not verify_password(data.password, usuario.password_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")

    # Incluímos o user_id no payload do token
    token = criar_token_acesso(
        data={"sub": usuario.email, "role": usuario.role, "user_id": str(usuario.id)}
    )

    # Retornamos o user_id e a role na resposta para o frontend salvar no LocalStorage
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": str(usuario.id),
        "role": usuario.role,
    }
