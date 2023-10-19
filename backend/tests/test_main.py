from fastapi import FastAPI
from fastapi.testclient import TestClient

from main import app
from models import Journey

client = TestClient(app)


def test_get_journeys_returns_the_loaded_tree(mocker):
    journey = Journey(id="id", title="title", invitable=True, keyValues={})
    mocker.patch("models.Journey.load_tree_from_path", return_value=journey)

    response = client.get("/get-journeys")

    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "id": "id",
            "clone": None,
            "title": "title",
            "invitable": True,
            "keyValues": {},
            "clones": [],
        }
    }


def test_get_journeys_returns_the_loaded_tree_from_disc(mocker, tmp_path):
    mocker.patch("main.YAML_DIR", tmp_path)
    (tmp_path / "client-a-journey.yaml").write_text(
        """
title: Client A
invitable: true
keyValues:
    client: client-a
    joint: hip
"""
    )
    (tmp_path / "client-a-child-journey.yaml").write_text(
        """
clone: client-a
title: Client A child
invitable: true
keyValues:
    client: client-a-child
"""
    )

    response = client.get("/get-journeys")

    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "id": "client-a",
            "clone": None,
            "title": "Client A",
            "invitable": True,
            "keyValues": {
                "client": "client-a",
                "joint": "hip",
            },
            "clones": [
                {
                    "id": "client-a-child",
                    "clone": "client-a",
                    "title": "Client A child",
                    "invitable": True,
                    "keyValues": {
                        "client": "client-a-child",
                        "joint": "hip",
                    },
                    "clones": [],
                }
            ],
        }
    }
