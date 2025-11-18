from database import Base, engine, SessionLocal
from models import Produto

def popular():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    cores = ["preto","branco","azul","amarelo","vermelho","verde","roxo","cinza"]

    produtos = []

    #camisa polo

    for cor in cores:
        produtos.append(Produto(
            tipo = 'Polo',
            variante = 'Sem estampa',
            manga = "curta",
            cor = cor,
            preco = 59.90,
            estoque = 101,
            descricao = f"Camisa polo manga curta sem estamapa, na cor {cor}, tecido leve e confortável, estilo casual"
        ))

        produtos.append(Produto(
            tipo = 'Polo',
            variante = "Com estampa",
            manga = "curta",
            cor = cor,
            preco = 69.90,
            estoque = 184,
            descricao = f"Camisa polo manga curta com estampa, na cor {cor}, tecido leve e confortavel, estilo casual"
        ))

        #Camisa normal

        produtos.append(Produto(
            tipo = "normal",
            variante = "Sem estampa",
            manga = "curta",
            cor = cor,
            preco = 39.99,
            estoque = 200,
            descricao = f"Camisa casual, gola normal sem estampa na cor {cor}, ideal para uso diário."            
        ))

        produtos.append(Produto(
            tipo = "normal",
            variante = "Com estampa",
            manga = "curta",
            cor = cor,
            preco = 49.99,
            estoque = 84,
            descricao = f"Camisa casual, gola normal sem estampa na cor {cor}, ideal para uso diário."
        ))

        #Camisa Social

        produtos.append(Produto(
            tipo = "social",
            variante = "lisa",
            manga = "curta",
            cor = cor,
            preco = 110.90,
            descricao = f"Camisa social de manga curta, na cor {cor}, ideal para ambientes formais."
        ))

        produtos.append(Produto(
            tipo = "social",
            variante = "lisa",
            manga = "longa",
            cor = cor,
            preco = 199.99,
            descricao = f"Camisa social de manga longa, na cor {cor}, com acabamento premium, material importado."
        ))    

    db.add_all(produtos)
    db.commit()
    print("Banco populado com sucesso!")

    if __name__ == "__main__":
        popular