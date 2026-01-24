from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from database import engine
from models import Representative

def list_representatives():
    """Retorna lista de representantes ordenados por nome."""
    with Session(engine) as session:
        stmt = select(Representative).order_by(Representative.name)
        results = session.scalars(stmt).all()
        
        data = []
        for r in results:
            data.append({
                "id": r.id, 
                "name": r.name,
                "department_id": r.department_id 
            })
        return data

def insert_representative(name: str, dept_id: int):
    """Insere um novo representante."""
    with Session(engine) as session:
        try:
            new_rep = Representative(name=name, department_id=dept_id)
            session.add(new_rep)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e

# --- ADICIONE ESTA FUNÇÃO NOVA ---
def delete_representative(rep_id: int):
    """Deleta um representante pelo ID."""
    with Session(engine) as session:
        try:
            stmt = delete(Representative).where(Representative.id == rep_id)
            result = session.execute(stmt)
            session.commit()
            return result.rowcount > 0
        except Exception as e:
            session.rollback()
            raise e