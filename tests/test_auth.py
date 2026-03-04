def test_create_user_success(client):
    response = client.post(
        "/auth/",
        json={"nome": "Juan Teste", "email": "test@example.com", "password": "123"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Usuário criado com sucesso!"


def test_create_user_duplicate_email(client):
    # Primeiro cadastro
    client.post(
        "/auth/",
        json={"nome": "Juan 1", "email": "duplicate@example.com", "password": "123"},
    )
    # Tentativa duplicada
    response = client.post(
        "/auth/",
        json={"nome": "Juan 2", "email": "duplicate@example.com", "password": "abc"},
    )
    assert response.status_code == 400
