from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from database import engine
from models import Category

def insert_category(name_input: str):
    """Insere uma nova categoria de produtos."""
    with Session(engine) as session:
        try:
            new_cat = Category(name=name_input)
            session.add(new_cat)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            # Propaga o erro para que o frontend (st.error) possa exibi-lo
            raise e

def list_categories():
    """Lista todas as categorias cadastradas (Ordenadas por nome)."""
    with Session(engine) as session:
        # Adicionei order_by para facilitar a leitura nos selects
        stmt = select(Category).order_by(Category.name)
        results = session.scalars(stmt).all()
        
        # Retorna lista de dicionários pronta para uso
        return [{"id": cat.id, "name": cat.name} for cat in results]

def delete_category(cat_id: int):
    """Deleta uma categoria pelo ID."""
    with Session(engine) as session:
        try:
            stmt = delete(Category).where(Category.id == cat_id)
            result = session.execute(stmt)
            session.commit()
            
            # Retorna True se deletou algo, False se não achou
            return result.rowcount > 0
        except Exception as e:
            session.rollback()
            raise e