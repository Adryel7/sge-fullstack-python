# 📊 SGE-Analytics (v2.0) - Sistema de Gestão de Estoque Full-Stack

> **De Planilhas Manuais para uma Aplicação Web Escalável.**
> Uma solução robusta de gerenciamento de inventário migrada de Excel para Python, focada em integridade de dados e visualização em tempo real.

![Status](https://img.shields.io/badge/Status-Concluído-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Stack](https://img.shields.io/badge/Backend-PostgreSQL%20%7C%20SQLAlchemy-336791)
![Frontend](https://img.shields.io/badge/Frontend-Streamlit%20%7C%20Plotly-FF4B4B)

---

## 🚀 A Evolução: Do Excel para Full-Stack
Este projeto representa a **versão 2.0** de um sistema de controle de estoque. O objetivo foi refatorar uma solução baseada em planilhas (`.xlsx`) para uma arquitetura de software profissional, resolvendo problemas de escalabilidade, concorrência e integridade de dados.

### 🆚 Antes e Depois

| **Versão 1.0 (Legado)** | **Versão 2.0 (Atual)** |
| :--- | :--- |
| **Tecnologia:** Excel / LibreOffice | **Tecnologia:** Python (Streamlit) + PostgreSQL |
| **Dados:** Arquivo local plano (Flat file) | **Dados:** Banco Relacional na Nuvem (Neon Tech) |
| **Risco:** Erros manuais e falta de log | **Segurança:** Tipagem forte, ORM e Transações Atômicas |
| **Acesso:** Monousuário / Arquivo travado | **Acesso:** Web App Multiúsuário |

#### 📸 Visualização da Mudança

**v2.0: Dashboard Interativo (Python & Plotly)**

Clique na imagem abaixo para ver a demonstração em vídeo (arquivo .webm):

[![](docs/assets/dashboard.png)](docs/assets/dashboard.webm)

> *O vídeo acima demonstra a interatividade dos filtros e a atualização dos gráficos em tempo real.*

**v1.0: Planilha Original (Excel)**
<img width="800" alt="Dashboard Excel v1" src="https://github.com/user-attachments/assets/c5eed63f-c661-4d43-b54e-c8297fe1878e" />

> 📂 **Nota:** O projeto original em Excel foi mantido para fins de histórico e comparação. Você pode acessá-lo na pasta [`/legacy_v1`](./legacy_v1).

---

## 🛠️ Stack Tecnológica (v2.0)

O sistema foi construído seguindo princípios de **Engenharia de Software** e **Engenharia de Dados**:

* **Frontend/App:** [Streamlit](https://streamlit.io/) (Framework Python para Data Apps).
* **Banco de Dados:** PostgreSQL 17 (Hospedagem Serverless via Neon).
* **ORM (Object-Relational Mapping):** [SQLAlchemy](https://www.sqlalchemy.org/) para abstração e segurança das queries.
* **Análise & Visualização:** Pandas (Manipulação de DataFrames) e Plotly (Gráficos Interativos).
* **Versionamento:** Git & GitHub.

---

## 🗄️ Modelagem de Dados e Arquitetura

Diferente da versão em planilha, a v2.0 utiliza um banco de dados normalizado (3NF) para garantir a consistência das transações.

**Diagrama Entidade-Relacionamento (DER):**

![DER do Sistema](docs/database/sge_der_v2.png)

> 🔗 **Fonte:** O código DBML do esquema está disponível em [`docs/database/sge_schema.dbml`](docs/database/sge_schema.dbml).

---

## 📂 Estrutura do Repositório

```text
/
├── docs/                  # Documentação Técnica
│   ├── assets/            # Mídias (Vídeos de demo, Logos)
│   └── database/          # Arquivos do Banco (DER imagem e código .dbml)
├── legacy_v1/             # Versão antiga do projeto (Excel/LibreOffice)
├── scripts/               # Scripts auxiliares (Reset de DB, Carga de Dados)
├── src/                   # Código Fonte da Aplicação
│   ├── crud/              # Lógica de Negócio (Controllers)
│   ├── pages/             # Páginas do Streamlit (Movimentações, Cadastros)
│   ├── database.py        # Conexão Singleton com PostgreSQL
│   ├── models.py          # Definição das Tabelas (SQLAlchemy Models)
│   └── Home.py            # [Entry Point] Dashboard Principal
├── requirements.txt       # Dependências do projeto
└── README.md              # Documentação Principal
```
## 💻 Como Rodar o Projeto Localmente

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Adryel7/sge-analytics-v2.git](https://github.com/Adryel7/sge-analytics-v2.git)
    cd sge-analytics-v2
    ```

2.  **Crie um ambiente virtual:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/Mac
    # .venv\Scripts\activate   # Windows
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as Credenciais:**
    Crie uma pasta `.streamlit` na raiz e um arquivo `secrets.toml` dentro dela. Adicione a string de conexão do seu banco (Postgres Local ou Neon):
    ```toml
    # .streamlit/secrets.toml
    DATABASE_URL = "postgresql://usuario:senha@host:5432/nome_do_banco"
    ```

5.  **Execute a aplicação:**
    ```bash
    streamlit run src/Home.py
    ```

---

## 👤 Autor

Desenvolvido por **Adryel Almeida**
* 💼 [LinkedIn](https://www.linkedin.com/in/adryel-almeida-052365321/)
* 📂 [Portfólio GitHub](https://github.com/Adryel7)

---

*Este projeto é parte do meu portfólio de transição para Engenharia de Dados.*