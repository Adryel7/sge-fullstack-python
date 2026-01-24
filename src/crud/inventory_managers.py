from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from database import engine
from models import InventoryManager

def insert_manager(name_input: str):
    """Insere um novo gerente de inventário."""
    with Session(engine) as session:
        try:
            new_manager = InventoryManager(name=name_input)
            session.add(new_manager)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            # Propaga o erro para ser tratado no frontend
            raise e

def list_managers():
    """Lista todos os gerentes cadastrados (Ordenados por nome)."""
    with Session(engine) as session:
        stmt = select(InventoryManager).order_by(InventoryManager.name)
        results = session.scalars(stmt).all()
        
        # Retorna lista limpa de dicionários
        return [{"id": m.id, "name": m.name} for m in results]

def delete_manager(m_id: int):
    """Deleta um gerente pelo ID."""
    with Session(engine) as session:
        try:
            stmt = delete(InventoryManager).where(InventoryManager.id == m_id)
            result = session.execute(stmt)
            session.commit()
            
            # Retorna True se deletou, False se não achou
            return result.rowcount > 0
            
        except Exception as e:
            session.rollback()
            raise e