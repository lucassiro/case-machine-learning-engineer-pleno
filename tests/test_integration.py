import json
from http import HTTPStatus

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": "ok"}


def test_history():
    response = client.get("/model/history/")
    assert response.status_code == HTTPStatus.OK


def test_load():
    with open("../notebook/model.pkl", "rb") as f:
        model = f.read()

    files = {"model": model}
    response = client.post(
        url="/model/load/",
        files=files,
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": "ok"}


def test_predict():
    response = client.post(
        url="/model/predict/",
        data=json.dumps({"origin_wind_speed": 1.0, "dest_wind_speed": 1.0})
    )
    assert response.status_code == HTTPStatus.OK
