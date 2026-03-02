from fastapi import FastAPI
from src.app.core.database import engine, Base

app = FastAPI()


# Este comando cria o arquivo .db (SQLite) ou as tabelas (Postgres) se não existirem
@app.on_event("startup")
def configure_db():
    print("Conectando ao banco e criando tabelas...")
    Base.metadata.create_all(bind=engine)
    print("Banco de dados pronto!")


@app.get("/")
def read_root():
    return {"status": "API de Treinamento Online"}


# Seus endpoints virão aqui...
