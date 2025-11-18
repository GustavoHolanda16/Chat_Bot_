from database import Base
from sqlalchemy import Column, Integer, String, Float

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String)
    variante = Column(String)
    manga = Column(String)
    cor = Column(String)
    preco = Column(Float)
    estoque = Column(Integer)
    descricao = Column(String)

