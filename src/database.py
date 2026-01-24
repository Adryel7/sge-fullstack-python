from sqlalchemy import create_engine

USER = #seu usuário      
PASS = #Sua senha     
IP = #Seu endereçoIP     
DB = #Nome do BD  

URL = f'postgresql://{USER}:{PASS}@{IP}:5432/{DB}'

engine = create_engine(URL)