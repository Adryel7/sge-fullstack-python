import sys
import os

# Adiciona a raiz do projeto ao Python Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import engine
# IMPORTANTE: Importamos o Base e TODAS as classes do models.py
# Sem importar as classes, o SQLAlchemy não sabe quais tabelas apagar/criar.
from src.models import Base, Category, Product, Department, Representative, InventoryManager, InventoryTransaction

def reset_database():
    print("🔌 Conectando ao PostgreSQL (192.168.56.101)...")
    
    # Confirmação de segurança
    confirm = input("⚠️  ATENÇÃO: Isso vai DESTRUIR todas as tabelas do banco 'estoque_db'. Confirmar? (s/n): ")
    if confirm.lower() != 's':
        print("Cancelado.")
        return

    try:
        print("🔥 Apagando tabelas antigas...")
        # O drop_all olha para os modelos importados acima e apaga as tabelas correspondentes
        Base.metadata.drop_all(bind=engine)
        
        print("✨ Criando novas tabelas...")
        # Recria as tabelas baseadas nos modelos
        Base.metadata.create_all(bind=engine)
        
        print("✅ Banco de dados zerado e pronto para uso!")
        
    except Exception as e:
        print(f"❌ Erro ao resetar banco: {e}")
        print("Verifique se o arquivo src/models.py contém a variável 'Base'.")

if __name__ == "__main__":
    reset_database()