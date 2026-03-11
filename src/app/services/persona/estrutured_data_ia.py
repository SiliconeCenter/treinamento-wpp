import json
import os

from openai import OpenAI

from src.app.schemas.persona.persona_create import (
    PersonaCreate,
)  # Importe seu schema para validação

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def preencher_persona(texto_do_arquivo: str):
    prompt_sistema = """
    Você é um motor de extração de dados literal. Sua tarefa é ler um roteiro de persona e reorganizar o conteúdo original nos campos abaixo, SEM RESUMIR, parafrasear ou omitir qualquer detalhe.

    Transcreva o conteúdo exatamente como está no texto original para as seguintes chaves:

    1. nome: O nome da persona identificado.
    2. perfil: Transcreva integralmente as descrições demográficas, idade, localização, histórico e traços de personalidade.
    3. objetivo: Transcreva integralmente as motivações, o procedimento buscado, medos e todas as objeções listadas.
    4. instrucao: Transcreva integralmente todas as regras de comportamento, tom de voz, ritmo, comprimento de frases e comportamentos proibidos.

    Regra de Ouro: Se a informação está no texto, ela deve aparecer no JSON. Não gere explicações, retorne APENAS o JSON puro.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Recomendo o 4o-mini: é muito mais barato e excelente para extração
            messages=[
                {"role": "system", "content": prompt_sistema},
                {
                    "role": "user",
                    "content": f"Converta este texto em JSON: {texto_do_arquivo}",
                },
            ],
            response_format={
                "type": "json_object"
            },  # Isso garante que o retorno seja um JSON válido
            temperature=0,
        )

        # Converte a string de resposta em um dicionário Python
        dados_extraidos = json.loads(response.choices[0].message.content)

        # Retorna o objeto validado pelo seu Schema Pydantic
        return PersonaCreate(**dados_extraidos)

    except Exception as e:
        print(f"Erro na extração com IA: {e}")
        return None
