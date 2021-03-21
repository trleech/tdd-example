import uuid


def test_create_ale(client):
    res = client.post(
        "/ales",
        json={
            "name": "Hobgoblin",
            "alcohol_by_volume": 4.5,
        },
    )
    assert res.status_code == 201
    assert res.get_json()["name"] == "Hobgoblin"
    assert res.get_json()["alcohol_by_volume"] == 4.5
    assert res.get_json()["id"] is not None


def test_update_ale(client):
    res = client.post(
        "/ales",
        json={
            "name": "Hobgoblin",
            "alcohol_by_volume": 4.5,
        },
    )
    res = client.put(
        f"/ales/{res.get_json()['id']}",
        json={
            "name": "London Pride",
            "alcohol_by_volume": 4.7,
        },
    )
    assert res.status_code == 200
    assert res.get_json()["name"] == "London Pride"
    assert res.get_json()["alcohol_by_volume"] == 4.7


def test_get_ale_404(client):
    res = client.get(f"/ales/{uuid.uuid4()}")
    assert res.status_code == 404


def test_delete_ale(client):
    res = client.post(
        "/ales",
        json={
            "name": "Hobgoblin",
            "alcohol_by_volume": 4.5,
        },
    )
    ale_id = res.get_json()["id"]
    res = client.delete(f"/ales/{ale_id}")
    assert res.status_code == 204

    res = client.get(f"/ales/{ale_id}")
    assert res.status_code == 404


def test_get_ales_list_empty(client):
    res = client.get("/ales")
    assert res.status_code == 200
    assert len(res.get_json()) == 0


def test_get_ales_list_two(client):
    client.post(
        "/ales",
        json={
            "name": "Hobgoblin",
            "alcohol_by_volume": 4.5,
        },
    )
    client.post(
        "/ales",
        json={
            "name": "London Pride",
            "alcohol_by_volume": 4.7,
        },
    )
    res = client.get("/ales")
    assert res.status_code == 200
    assert len(res.get_json()) == 2


def test_create_ale_negative_alcohol_by_volume(client):
    res = client.post(
        "/ales",
        json={
            "name": "Hobgoblin",
            "alcohol_by_volume": -1.0,
        },
    )
    assert res.status_code == 422

    res = client.get("/ales")
    assert len(res.get_json()) == 0


def test_create_ale_120_alcohol_by_volume(client):
    res = client.post(
        "/ales",
        json={
            "name": "Hobgoblin",
            "alcohol_by_volume": 120,
        },
    )
    assert res.status_code == 422

    res = client.get("/ales")
    assert len(res.get_json()) == 0
