from fastapi.testclient import TestClient
from sqlalchemy import StaticPool,create_engine
from sqlalchemy.orm import sessionmaker
from api.main import app, Base, get_db
import pytest

client = TestClient(app)

DATABASE_URL2 = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL2, 
    connect_args={
        "check_same_thread": False,
        },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    database = TestingSessionLocal()
    try:
        yield database
    finally:
        database.close()

app.dependency_overrides[get_db] = override_get_db


def setup() -> None:
    print("Setting up)")
    # Create the tables in the test database
    Base.metadata.create_all(bind=engine)

setup()


def teardown() -> None:
    # Drop the tables in the test database
    Base.metadata.drop_all(bind=engine)



def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Server is running"}


def test_create_item():
    response = client.post(
        "/ceramica",
        json={
            "inventario": "08.5.15",
            "data": "2021-06-16T00:00:00.000Z",
            "designacao": "",
            "nome_local": "Vinagreira grande",
            "ano_fab": 2008,
            "ano_uso": "",
            "fab_lugar": "Sergude",
            "fab_freguesia": "Oliveira",
            "fab_Vila": "",
            "fab_concelho": "Barcelos",
            "fab_distrito": "Braga",
            "regiao": "Minho",
            "funcao": "preparação e conserva de vinagre",
            "autor": "Oliveira",
            "alt_mm": 436,
            "diam_maior_mm": 268,
            "largura_mm": 285,
            "diam_boca_mm": "",
            "diam_base_mm": "",
            "cap_cl": "",
            "peso_gr": 3104,
            "asas": 1,
            "patas": 0,
            "bico": 0,
            "rabo": 0,
            "orificios": 0,
            "decoracao": "",
            "fonte": "",
            "observacoes": "",
            "lat": 41.5839542,
            "lon": -8.5431934,
            "filter_fields_": "",
            "filter_fields_title_": "",
            "infos_to_show_": "Data;inventário;nome_local",
            "info_titles_": "Data;Inventário;Nome Local",
            "marker_bgcolor_": "8800FFF0",
            "marker_size_": "40",
            "marker_color_": "",
            "photo1": "https://raw.githubusercontent.com/arthurmiy/ceramicas-repo/master/consolidado/08.5.15.png",
            "marker_format_": "https://raw.githubusercontent.com/arthurmiy/ceramicas-repo/master/consolidado/08.5.15.png",
            "photo2": "",
            "photo_amount_": 1,
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["data"] == "2021-06-16T00:00:00.000Z"
    assert data["inventario"] == "08.5.15"
    assert data["nome_local"] == "Vinagreira grande"
    assert data["ano_fab"] == 2008
    assert data["fab_lugar"] == "Sergude"
    assert data["fab_freguesia"] == "Oliveira"
    assert data["alt_mm"] == 436
    assert data["diam_maior_mm"] == 268
    assert data["largura_mm"] == 285
    assert data["peso_gr"] == 3104
    assert data["photo1"] == "https://raw.githubusercontent.com/arthurmiy/ceramicas-repo/master/consolidado/08.5.15.png"
    assert data["photo_amount_"] == 1           

def test_update_item():
    item_id = "08.5.15"
    response = client.put(
        f"/ceramica/{item_id}",
        json={
            "inventario": "08.5.15",
            "data": "2021-06-16T00:00:00.000Z",
            "designacao": "",
            "nome_local": "Vinagreira grande",
            "ano_fab": 2010,
            "ano_uso": "",
            "fab_lugar": "Sergude",
            "fab_freguesia": "Oliveira",
            "fab_Vila": "",
            "fab_concelho": "Barcelos",
            "fab_distrito": "Braga",
            "regiao": "Minho",
            "funcao": "preparação e conserva de vinagre",
            "autor": "Oliveira",
            "alt_mm": 436,
            "diam_maior_mm": 268,
            "largura_mm": 285,
            "diam_boca_mm": "",
            "diam_base_mm": "",
            "cap_cl": "",
            "peso_gr": 3104,
            "asas": 1,
            "patas": 0,
            "bico": 0,
            "rabo": 0,
            "orificios": 0,
            "decoracao": "",
            "fonte": "",
            "observacoes": "",
            "lat": 41.5839542,
            "lon": -8.5431934,
            "filter_fields_": "",
            "filter_fields_title_": "",
            "infos_to_show_": "Data;inventário;nome_local",
            "info_titles_": "Data;Inventário;Nome Local",
            "marker_bgcolor_": "8800FFF0",
            "marker_size_": "40",
            "marker_color_": "",
            "photo1": "https://raw.githubusercontent.com/arthurmiy/ceramicas-repo/master/consolidado/08.5.15.png",
            "marker_format_": "https://raw.githubusercontent.com/arthurmiy/ceramicas-repo/master/consolidado/08.5.15.png",
            "photo2": "",
            "photo_amount_": 1,
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["data"] == "2021-06-16T00:00:00.000Z"
    assert data["inventario"] == "08.5.15"
    assert data["nome_local"] == "Vinagreira grande"
    assert data["ano_fab"] == 2010
    assert data["fab_lugar"] == "Sergude"
    assert data["fab_freguesia"] == "Oliveira"
    assert data["alt_mm"] == 436
    assert data["diam_maior_mm"] == 268
    assert data["largura_mm"] == 285
    assert data["peso_gr"] == 3104
    assert data["photo1"] == "https://raw.githubusercontent.com/arthurmiy/ceramicas-repo/master/consolidado/08.5.15.png"
    assert data["photo_amount_"] == 1   


def test_get_item():

    response = client.get("/ceramicas")
    assert response.status_code == 200, response.text
    data = response.json()
    print(f"Got data: {data}")
    assert len(data) > 0
    first_item = data[0]
    assert first_item["data"] == "2021-06-16T00:00:00.000Z"
    assert first_item["inventario"] == "08.5.15"
    assert first_item["nome_local"] == "Vinagreira grande"
    assert first_item["ano_fab"] == 2010
    assert first_item["fab_lugar"] == "Sergude"
    assert first_item["fab_freguesia"] == "Oliveira"
    assert first_item["alt_mm"] == 436
    assert first_item["diam_maior_mm"] == 268
    assert first_item["largura_mm"] == 285
    assert first_item["peso_gr"] == 3104
    assert first_item["photo1"] == "https://raw.githubusercontent.com/arthurmiy/ceramicas-repo/master/consolidado/08.5.15.png"
    assert first_item["photo_amount_"] == 1   

def test_delete_item():
    item_id = "08.5.15"
    response = client.delete(f"/ceramica/{item_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["inventario"] == item_id
    # Try to get the deleted item
    response = client.get(f"/ceramicas/{item_id}")
    assert response.status_code == 404, response.text