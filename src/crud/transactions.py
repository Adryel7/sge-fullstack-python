from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, desc
from database import engine
from models import InventoryTransaction, Product
from datetime import date

def list_transactions():
    """Retorna todas as transações."""
    with Session(engine) as session:
        stmt = select(InventoryTransaction).order_by(desc(InventoryTransaction.transaction_date), desc(InventoryTransaction.id))
        return session.scalars(stmt).all()

def register_transaction(type: str, product_id: int, quantity: int, transaction_date: date, department_id: int, representative_id: int, inventory_manager_id: int, obs: str = None):
    """Registra transação e atualiza estoque."""
    type_lower = type.lower()
    with Session(engine) as session:
        try:
            product = session.get(Product, product_id)
            if not product: raise ValueError(f"Produto {product_id} não encontrado.")

            if type_lower == 'out':
                if product.quantity_in_stock < quantity:
                    raise ValueError(f"Saldo insuficiente. Estoque: {product.quantity_in_stock}")
                new_balance = product.quantity_in_stock - quantity
            elif type_lower == 'in':
                new_balance = product.quantity_in_stock + quantity
            else:
                raise ValueError("Tipo inválido.")

            new_trans = InventoryTransaction(
                type=type, product_id=product_id, quantity=quantity, transaction_date=transaction_date,
                department_id=department_id, representative_id=representative_id, inventory_manager_id=inventory_manager_id, obs=obs
            )
            session.add(new_trans)
            session.execute(update(Product).where(Product.id == product_id).values(quantity_in_stock=new_balance))
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e

# --- NOVAS FUNÇÕES PARA ADMINISTRAÇÃO ---

def delete_transaction(trans_id: int):
    """Deleta uma transação e REVERTE o impacto no estoque."""
    with Session(engine) as session:
        try:
            trans = session.get(InventoryTransaction, trans_id)
            if not trans: return False
            
            product = session.get(Product, trans.product_id)
            
            # Lógica de Estorno (Reverso do original)
            if trans.type == 'IN':
                # Se foi entrada, temos que remover do estoque
                if product.quantity_in_stock < trans.quantity:
                    raise ValueError("Não é possível estornar esta entrada: O estoque atual é menor que a quantidade a remover.")
                new_balance = product.quantity_in_stock - trans.quantity
            else: # OUT
                # Se foi saída, devolvemos ao estoque
                new_balance = product.quantity_in_stock + trans.quantity
            
            # Atualiza produto
            session.execute(update(Product).where(Product.id == product.id).values(quantity_in_stock=new_balance))
            
            # Deleta transação
            session.execute(delete(InventoryTransaction).where(InventoryTransaction.id == trans_id))
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e

def update_transaction(trans_id: int, new_quantity: int, new_obs: str, new_date: date):
    """
    Atualiza uma transação. Se a quantidade mudar, recalcula o estoque.
    """
    with Session(engine) as session:
        try:
            trans = session.get(InventoryTransaction, trans_id)
            if not trans: return False
            
            # Se quantidade mudou, faz o ajuste fino no estoque
            if new_quantity != trans.quantity:
                product = session.get(Product, trans.product_id)
                diff = new_quantity - trans.quantity
                
                if trans.type == 'IN':
                    # Entrada aumentou? Soma a diferença. Diminuiu? Subtrai.
                    new_balance = product.quantity_in_stock + diff
                else: # OUT
                    # Saída aumentou? Subtrai do estoque. Diminuiu? Devolve pro estoque.
                    new_balance = product.quantity_in_stock - diff
                
                if new_balance < 0:
                     raise ValueError("A alteração deixaria o estoque negativo.")

                session.execute(update(Product).where(Product.id == product.id).values(quantity_in_stock=new_balance))

            # Atualiza os dados da transação
            session.execute(
                update(InventoryTransaction)
                .where(InventoryTransaction.id == trans_id)
                .values(quantity=new_quantity, obs=new_obs, transaction_date=new_date)
            )
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e