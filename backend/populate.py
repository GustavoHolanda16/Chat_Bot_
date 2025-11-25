# populate.py - PRODUTOS OTIMIZADOS
from database import Base, engine, SessionLocal
from models import Produto

def popular():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # Cores expandidas
    cores = ["preto", "branco", "azul", "azul marinho", "vermelho", "verde", "verde musgo", 
             "cinza", "cinza chumbo", "bege", "vinho", "rosa", "laranja"]

    produtos = []

    # CAMISAS POLO - Descrições otimizadas
    for cor in cores:
        produtos.append(Produto(
            tipo='Polo',
            variante='Básica',
            manga="curta",
            cor=cor,
            preco=79.90,
            estoque=150,
            descricao=f"Camisa polo básica manga curta cor {cor}, tecido piquet de algodão, acabamento premium, ideal para o dia a dia"
        ))

        produtos.append(Produto(
            tipo='Polo',
            variante="Premium",
            manga="curta",
            cor=cor,
            preco=129.90,
            estoque=80,
            descricao=f"Camisa polo premium manga curta cor {cor}, tecido malha de algodão egípcio, logo bordado, conforto superior"
        ))

        produtos.append(Produto(
            tipo='Polo',
            variante="Esportiva",
            manga="longa",
            cor=cor,
            preco=99.90,
            estoque=60,
            descricao=f"Camisa polo esportiva manga longa cor {cor}, tecido dry-fit, tecnologia anti-odor, ideal para atividades físicas"
        ))

    # CAMISAS CASUAIS
    for cor in cores:
        produtos.append(Produto(
            tipo="Casual",
            variante="Básica Lisa",
            manga="curta",
            cor=cor,
            preco=49.90,
            estoque=200,
            descricao=f"Camisa casual básica lisa manga curta cor {cor}, tecido cotton, corte reto, versátil para qualquer ocasião"
        ))

        produtos.append(Produto(
            tipo="Casual",
            variante="Estampada",
            manga="curta",
            cor=cor,
            preco=69.90,
            estoque=120,
            descricao=f"Camisa casual estampada manga curta cor {cor}, estampa exclusiva, tecido leve, estilo urbano contemporâneo"
        ))

        produtos.append(Produto(
            tipo="Casual",
            variante="Social Casual",
            manga="longa",
            cor=cor,
            preco=89.90,
            estoque=90,
            descricao=f"Camisa casual social manga longa cor {cor}, tecido popeline, colarinho reforçado, transição dia para noite"
        ))

    # CAMISAS SOCIAIS
    for cor in cores:
        produtos.append(Produto(
            tipo="Social",
            variante="Executiva",
            manga="longa",
            cor=cor,
            preco=159.90,
            estoque=75,
            descricao=f"Camisa social executiva manga longa cor {cor}, tecido oxford 100% algodão, colarinho clássico, para reuniões formais"
        ))

        produtos.append(Produto(
            tipo="Social",
            variante="Slim Fit",
            manga="longa",
            cor=cor,
            preco=179.90,
            estoque=65,
            descricao=f"Camisa social slim fit manga longa cor {cor}, corte ajustado, tecido twill, botões mother of pearl, elegância moderna"
        ))

        produtos.append(Produto(
            tipo="Social",
            variante="Manga Curta",
            cor=cor,
            manga="curta",
            preco=139.90,
            estoque=85,
            descricao=f"Camisa social manga curta cor {cor}, tecido microfibra, colarinho italiano, ideal para climas quentes e escritório"
        ))

    # NOVAS CATEGORIAS
    # Camisas Esportivas
    for cor in ["preto", "branco", "azul", "cinza", "verde"]:
        produtos.append(Produto(
            tipo="Esportiva",
            variante="Dry-Fit",
            manga="curta",
            cor=cor,
            preco=89.90,
            estoque=110,
            descricao=f"Camisa esportiva dry-fit manga curta cor {cor}, tecnologia de secagem rápida, ventilação otimizada, para exercícios"
        ))

    # Camisas Premium
    for cor in ["branco", "azul marinho", "vinho", "preto"]:
        produtos.append(Produto(
            tipo="Premium",
            variante="Algodão Egípcio",
            manga="longa",
            cor=cor,
            preco=299.90,
            estoque=40,
            descricao=f"Camisa premium algodão egípcio manga longa cor {cor}, fios longos 200S, costura reforçada, luxo e conforto"
        ))

    db.add_all(produtos)
    db.commit()
    print(f"Banco populado com sucesso! {len(produtos)} produtos criados.")

if __name__ == "__main__":
    popular()