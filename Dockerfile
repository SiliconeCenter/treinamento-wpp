FROM python:3.13-slim

WORKDIR /app

# Copia apenas arquivos de dependência primeiro (melhora cache)
COPY pyproject.toml poetry.lock* ./

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . .

CMD ["python", "-m", "treinamento-wpp"]