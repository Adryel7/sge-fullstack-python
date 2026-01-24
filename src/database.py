import os
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env se ele existir (uso local)
load_dotenv()

def get_engine():
    # 1. Tenta usar os Secrets do Streamlit (Produção/Nuvem)
    if "postgres" in st.secrets:
        creds = st.secrets["postgres"]
        url = (f"postgresql+psycopg2://{creds['username']}:{creds['password']}"
               f"@{creds['host']}:{creds['port']}/{creds['database']}?sslmode=require")
    
    # 2. Se não houver secrets, usa as variáveis do arquivo .env (Local)
    else:
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASS")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        database = os.getenv("DB_NAME")
        
        url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

    return create_engine(url)

engine = get_engine()