from sqlalchemy.orm import Session
from sqlalchemy import select, delete, update
from database import engine
from models import Product, Category

def insert_product(name: str, category_id: int, description: str = None, min_balance: int = 0):
    """Insere um novo produto no banco de dados."""
    with Session(engine) as session:
        try:
            # Verificação de integridade
            cat = session.execute(select(Category).where(Category.id == category_id)).scalar_one_or_none()
            if not cat:
                # Lança erro para o frontend capturar
                raise ValueError(f"Categoria ID {category_id} não existe.")

            new_prod = Product(
                name=name,
                category_id=category_id,
                description=description,
                min_balance=min_balance,
                quantity_in_stock=0 # Sempre começa zerado
            )
            session.add(new_prod)
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            raise e

def list_products():
    """Retorna lista de dicionários com dados dos produtos (Ordenados por nome)."""
    with Session(engine) as session:
        # Adicionei order_by para facilitar busca no selectbox
        stmt = select(Product).order_by(Product.name)
        results = session.scalars(stmt).all()
        
        data = []
        for p in results:
            info = {
                "id": p.id, 
                "name": p.name, 
                "category": p.category.name if p.category else "Sem Categoria", 
                "stock": p.quantity_in_stock,
                "min_balance": p.min_balance
            }
            data.append(info)
        return data

def update_product(prod_id: int, **kwargs):
    """
    Atualiza o produto. Impede a alteração manual de 'quantity_in_stock'.
    """
    # Remove quantity_in_stock por segurança
    kwargs.pop('quantity_in_stock', None)
    
    if not kwargs:
        return False

    with Session(engine) as session:
        try:
            # Validação de Categoria se ela for alterada
            if 'category_id' in kwargs:
                cat = session.execute(select(Category).where(Category.id == kwargs['category_id'])).scalar_one_or_none()
                if not cat:
                    raise ValueError(f"Categoria {kwargs['category_id']} não existe.")

            stmt = update(Product).where(Product.id == prod_id).values(**kwargs)
            result = session.execute(stmt)
            session.commit()
            
            return result.rowcount > 0
            
        except Exception as e:
            session.rollback()
            raise e

def delete_product(prod_id: int):
    """Deleta o produto pelo ID."""
    with Session(engine) as session:
        try:
            stmt = delete(Product).where(Product.id == prod_id)
            result = session.execute(stmt)
            session.commit()
            
            return result.rowcount > 0
            
        except Exception as e:
            session.rollback()
            raise e