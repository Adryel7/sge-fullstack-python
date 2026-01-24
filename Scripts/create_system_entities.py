import sys
import os
from sqlalchemy.orm import Session
from sqlalchemy import select

# --- 1. Ajuste de Caminho (Path) ---
# Isso garante que o Python encontre a pasta 'src' mesmo rodando de dentro de 'scripts'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Imports do seu projeto
from database import engine
from models import Department, Representative

def criar_entidades_sistema():
    with Session(engine) as session:
        print("🛠️  Iniciando verificação de Entidades de Sistema...")

        # ======================================================================
        # 1. DEPARTAMENTO: "ESTOQUE GERAL"
        # ======================================================================
        nome_dept_sistema = "ESTOQUE GERAL"
        
        # Tenta buscar no banco
        dept = session.scalars(select(Department).where(Department.name == nome_dept_sistema)).first()
        
        if not dept:
            print(f"⚙️  Criando departamento '{nome_dept_sistema}'...")
            dept = Department(name=nome_dept_sistema)
            session.add(dept)
            session.commit() # Salva para gerar o ID
            print(f"✅ Sucesso! Departamento criado. ID: {dept.id}")
        else:
            print(f"ℹ️  Departamento '{nome_dept_sistema}' já existe. ID: {dept.id}")

        # ======================================================================
        # 2. REPRESENTANTE: "SISTEMA DE ENTRADA"
        # ======================================================================
        nome_rep_sistema = "SISTEMA DE ENTRADA"
        
        # Tenta buscar no banco
        rep = session.scalars(select(Representative).where(Representative.name == nome_rep_sistema)).first()
        
        if not rep:
            print(f"⚙️  Criando representante '{nome_rep_sistema}'...")
            # IMPORTANTE: Vinculamos este representante ao "Estoque Geral"
            rep = Representative(name=nome_rep_sistema, department_id=dept.id)
            session.add(rep)
            session.commit()
            print(f"✅ Sucesso! Representante criado. ID: {rep.id}")
        else:
            print(f"ℹ️  Representante '{nome_rep_sistema}' já existe. ID: {rep.id}")

        print("\n🚀 Configuração concluída! Pode testar a aba de Entradas agora.")

if __name__ == "__main__":
    criar_entidades_sistema()