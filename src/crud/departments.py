from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from database import engine
from models import Department

def insert_department(name_input: str):
    """
    Insere um novo departamento.
    Usa o objeto Department definido no models.py.
    """
    with Session(engine) as session:
        try:
            # Criamos a instância da classe (Objeto)
            new_dept = Department(name=name_input)
            
            # Adicionamos à sessão (staging area)
            session.add(new_dept)
            
            # Persistimos no banco
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            # Propaga o erro para ser tratado no frontend
            raise e

def list_departments():
    """
    Lista todos os departamentos ordenados por nome.
    Retorna uma lista de dicionários para fácil visualização.
    """
    with Session(engine) as session:
        # SELECT * FROM departments ORDER BY name
        stmt = select(Department).order_by(Department.name)
        
        # scalars().all() pega os objetos Department resultantes da consulta
        results = session.scalars(stmt).all()
        
        # Convertendo objetos para dicionários
        return [{"id": dept.id, "name": dept.name} for dept in results]

def delete_department(dept_id: int):
    """
    Deleta um departamento pelo ID.
    Retorna True se deletou, False se não encontrou.
    """
    with Session(engine) as session:
        try:
            # delete(Tabela).where(Condição)
            stmt = delete(Department).where(Department.id == dept_id)
            
            result = session.execute(stmt)
            session.commit()
            
            return result.rowcount > 0
                
        except Exception as e:
            session.rollback()
            raise e