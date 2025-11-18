from database import Base
from sqlalchemy import Column, Integer, String, Float

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False, index=True)  
    variante = Column(String, nullable=False)
    manga = Column(String, nullable=False)
    cor = Column(String, nullable=False, index=True)  
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, nullable=False, default=0)  
    descricao = Column(String, nullable=False)
    
    def __repr__(self):
        return f"<Produto {self.tipo} {self.cor} - R${self.preco}>"