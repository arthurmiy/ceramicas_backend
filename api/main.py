from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped, mapped_column,MappedAsDataclass
from pydantic import BaseModel
from contextlib import asynccontextmanager
from typing import List


class Ceramica(BaseModel):
    inventario: str
    data: str
    designacao: str
    nome_local: str
    ano_fab: int
    ano_uso: str
    fab_lugar: str
    fab_freguesia: str
    fab_Vila: str
    fab_concelho: str
    fab_distrito: str
    regiao: str
    funcao: str
    autor: str
    alt_mm: int
    diam_maior_mm: int
    largura_mm: int
    diam_boca_mm: str
    diam_base_mm: str
    cap_cl: str
    peso_gr: int
    asas: int
    patas: int
    bico: int
    rabo: int
    orificios: int
    decoracao: str
    fonte: str
    observacoes: str
    lat: float
    lon: float
    filter_fields_: str
    filter_fields_title_: str
    infos_to_show_: str
    info_titles_: str
    marker_bgcolor_: str
    marker_size_: str
    marker_color_: str
    photo1: str
    marker_format_: str
    photo2: str
    photo_amount_: int


class CeramicaCreate(BaseModel):
    inventario: str
    data: str
    designacao: str
    nome_local: str
    ano_fab: int
    ano_uso: str
    fab_lugar: str
    fab_freguesia: str
    fab_Vila: str
    fab_concelho: str
    fab_distrito: str
    regiao: str
    funcao: str
    autor: str
    alt_mm: int
    diam_maior_mm: int
    largura_mm: int
    diam_boca_mm: str
    diam_base_mm: str
    cap_cl: str
    peso_gr: int
    asas: int
    patas: int
    bico: int
    rabo: int
    orificios: int
    decoracao: str
    fonte: str
    observacoes: str
    lat: float
    lon: float
    filter_fields_: str
    filter_fields_title_: str
    infos_to_show_: str
    info_titles_: str
    marker_bgcolor_: str
    marker_size_: str
    marker_color_: str
    photo1: str
    marker_format_: str
    photo2: str
    photo_amount_: int


class CeramicaUpdate(BaseModel):
    inventario: str
    data: str
    designacao: str
    nome_local: str
    ano_fab: int
    ano_uso: str
    fab_lugar: str
    fab_freguesia: str
    fab_Vila: str
    fab_concelho: str
    fab_distrito: str
    regiao: str
    funcao: str
    autor: str
    alt_mm: int
    diam_maior_mm: int
    largura_mm: int
    diam_boca_mm: str
    diam_base_mm: str
    cap_cl: str
    peso_gr: int
    asas: int
    patas: int
    bico: int
    rabo: int
    orificios: int
    decoracao: str
    fonte: str
    observacoes: str
    lat: float
    lon: float
    filter_fields_: str
    filter_fields_title_: str
    infos_to_show_: str
    info_titles_: str
    marker_bgcolor_: str
    marker_size_: str
    marker_color_: str
    photo1: str
    marker_format_: str
    photo2: str
    photo_amount_: int


DATABASE_URL = "sqlite:///:memory:"


class Base(DeclarativeBase, MappedAsDataclass):
    pass


class DBCeramica(Base):
    __tablename__ = "ceramicas"
    inventario: Mapped[str] = mapped_column(String(255), primary_key=True)
    data: Mapped[str] = mapped_column(String(255))
    designacao: Mapped[str] = mapped_column(String(255))
    nome_local: Mapped[str] = mapped_column(String(255))
    ano_fab: Mapped[int] = mapped_column()
    ano_uso: Mapped[str] = mapped_column(String(255))
    fab_lugar: Mapped[str] = mapped_column(String(255))
    fab_freguesia: Mapped[str] = mapped_column(String(255))
    fab_Vila: Mapped[str] = mapped_column(String(255))
    fab_concelho: Mapped[str] = mapped_column(String(255))
    fab_distrito: Mapped[str] = mapped_column(String(255))
    regiao: Mapped[str] = mapped_column(String(255))
    funcao: Mapped[str] = mapped_column(String(255))
    autor: Mapped[str] = mapped_column(String(255))
    alt_mm: Mapped[int] = mapped_column()
    diam_maior_mm: Mapped[int] = mapped_column()
    largura_mm: Mapped[int] = mapped_column()
    diam_boca_mm: Mapped[str] = mapped_column(String(255))
    diam_base_mm: Mapped[str] = mapped_column(String(255))
    cap_cl: Mapped[str] = mapped_column(String(255))
    peso_gr: Mapped[int] = mapped_column()
    asas: Mapped[int] = mapped_column()
    patas: Mapped[int] = mapped_column()
    bico: Mapped[int] = mapped_column()
    rabo: Mapped[int] = mapped_column()
    orificios: Mapped[int] = mapped_column()
    decoracao: Mapped[str] = mapped_column(String(255))
    fonte: Mapped[str] = mapped_column(String(255))
    observacoes: Mapped[str] = mapped_column(String(255))
    lat: Mapped[float] = mapped_column()
    lon: Mapped[float] = mapped_column()
    filter_fields_: Mapped[str] = mapped_column(String(255))
    filter_fields_title_: Mapped[str] = mapped_column(String(255))
    infos_to_show_: Mapped[str] = mapped_column(String(255))
    info_titles_: Mapped[str] = mapped_column(String(255))
    marker_bgcolor_: Mapped[str] = mapped_column(String(255))
    marker_size_: Mapped[str] = mapped_column(String(255))
    marker_color_: Mapped[str] = mapped_column(String(255))
    photo1: Mapped[str] = mapped_column(String(255))
    marker_format_: Mapped[str] = mapped_column(String(255))
    photo2: Mapped[str] = mapped_column(String(255))
    photo_amount_: Mapped[int] = mapped_column()


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


# Dependency to get the database session
def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


@app.get("/")
async def root():
    return {"message": "Server is running"}

@app.post("/ceramica")
def create_ceramica(ceramica: CeramicaCreate, db: Session = Depends(get_db)) -> Ceramica:
    db_ceramica = DBCeramica(**ceramica.model_dump())
    db.add(db_ceramica)
    db.commit()
    db.refresh(db_ceramica)
    return Ceramica(**db_ceramica.__dict__)

@app.get("/ceramicas")
def read_ceramica(db: Session = Depends(get_db)) -> List[Ceramica]:
    db_ceramicas = db.query(DBCeramica).all()
    return [Ceramica(**db_ceramica.__dict__) for db_ceramica in db_ceramicas]


@app.get("/ceramica/{inventario}")
def read_ceramica(inventario: str, db: Session = Depends(get_db)) -> Ceramica:
    db_ceramica = db.query(DBCeramica).filter(DBCeramica.inventario == inventario).first()
    if db_ceramica is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return Ceramica(**db_ceramica.__dict__)


@app.put("/ceramica/{inventario}")
def update_ceramica(inventario: str, ceramica: CeramicaUpdate, db: Session = Depends(get_db)) -> Ceramica:
    db_ceramica = db.query(DBCeramica).filter(DBCeramica.inventario == inventario).first()
    if db_ceramica is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in ceramica.model_dump().items():
        setattr(db_ceramica, key, value)
    db.commit()
    db.refresh(db_ceramica)
    return Ceramica(**db_ceramica.__dict__)


@app.delete("/ceramica/{inventario}")
def delete_ceramica(inventario: str, db: Session = Depends(get_db)) -> Ceramica:
    db_ceramica = db.query(DBCeramica).filter(DBCeramica.inventario == inventario).first()
    if db_ceramica is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_ceramica)
    db.commit()
    return Ceramica(**db_ceramica.__dict__)
