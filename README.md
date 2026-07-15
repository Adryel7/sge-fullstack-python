# 📊 SGE-Analytics (v2.0) - Inteligência de Estoque

> **De Planilhas Estruturadas para uma Arquitetura de Dados em Nuvem.**
> Uma solução *Full-Stack* de gerenciamento de inventário migrada de arquivos planos (`.xlsx`) para Banco de Dados Relacional, com foco em integridade transacional e análise em tempo real.

[![App Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sge-fullstack-python-qnayvqgpad6lnabr9yea35.streamlit.app)
![Status](https://img.shields.io/badge/Status-Produção-brightgreen)
![DB](https://img.shields.io/badge/Database-PostgreSQL%2016-336791)
![ETL](https://img.shields.io/badge/Data-ETL%20%26%20Seeding-orange)

---

## 🎯 Visão Geral do Projeto

Este projeto demonstra a **modernização de um processo de dados**, saindo de controles manuais suscetíveis a falhas para uma aplicação web robusta. O sistema garante que cada movimentação de estoque respeite as regras de negócio e integridade referencial (ACID), permitindo análises confiáveis.

👉 **[Acesse a Demonstração Online Aqui](https://sge-fullstack-python-qnayvqgpad6lnabr9yea35.streamlit.app)**

---

## 🔄 A Migração: Engenharia de Dados Aplicada

O principal desafio deste projeto foi reestruturar dados que viviam em silos (planilhas isoladas) para um modelo unificado.

| Característica | ❌ Versão Excel v1 | ✅ Versão Atual (SGE v2.0) |
| :--- | :--- | :--- |
| **Armazenamento** | Arquivo Local (`.xlsx`) | **PostgreSQL (Neon Tech Serverless)** |
| **Modelagem** | Tabela Flat (Desnormalizada) | **Modelo Relacional (3NF)** |
| **Integridade** | Validação manual / Visual | **Constraint Check & Foreign Keys** |
| **Escalabilidade** | Limitada pelo arquivo/memória | **Nuvem / Consultas SQL Otimizadas** |
| **Segurança** | Arquivo aberto | **Credenciais de Ambiente (.env)** |

### 📸 Comparativo Visual
**v1.0: Planilha Original (Excel)**
<img width="800" alt="Dashboard Excel v1" src="https://github.com/user-attachments/assets/c5eed63f-c661-4d43-b54e-c8297fe1878e" />
> O arquivo Excel(v1.0) foi preservado na pasta [`/legacy_v1`](./legacy_v1) para fins de auditoria e comparação histórica.

**V2.0(atual): Dashboard Analítico (Python & Plotly):**
![Dashboard Analytics](docs/assets/dashboard.png)

---

## 🛠️ Stack Tecnológica e Arquitetura

O sistema foi desenhado com foco em **modularidade** e **abstração de dados**:

* **Camada de Dados (Storage):** PostgreSQL (NeonDB).
* **Camada de Aplicação (ORM):** [SQLAlchemy](https://www.sqlalchemy.org/) - Utilizado para mapeamento objeto-relacional, garantindo que o código Python manipule o banco de forma segura contra *SQL Injection*.
* **Camada de Visualização (Frontend):** Streamlit - Escolhido pela capacidade de prototipagem rápida de Dashboards de Dados.
* **Análise Exploratória:** Pandas para manipulação de DataFrames e Plotly para visualização dinâmica.

---

## 🗄️ Modelagem de Dados (Schema Design)

O banco de dados foi normalizado para garantir a **Terceira Forma Normal (3NF)**, eliminando redundâncias e anomalias de atualização.

![DER do Sistema](docs/database/sge_der_v2.png)

> 🔗 O esquema completo documentado em código encontra-se em [`docs/database/sge_schema.dbml`](docs/database/sge_schema.dbml).

---

## ⚙️ Scripts de Governança e Carga de Dados

Além da aplicação principal, foram desenvolvidos scripts utilitários na pasta [`/Scripts`](./Scripts) para gerenciar o ciclo de vida dos dados (Data Lifecycle):

1.  **`create_system_entities.py` (Bootstrapping):**
    * Responsavel por criar as primeiras entidadesdo sistema.

2.  **`seed_corporate.py` (Data Seeding / Mock):**
    * Script de ETL que popula o banco com dados fictícios corporativos. Fundamental para testes de carga e para validar a performance das queries analíticas no dashboard sem expor dados reais.

3.  **`reset_bd.py` (Infrastructure):**
    * Automação para limpar o BAnco de dados. Utilizado em ambiente de desenvolvimento para garantir testes limpos e iterativos.

---

## 📂 Estrutura do Repositório

```text

├── docs/                  
│   ├── assets/            # Prints de tela
│   └── database/          # Documentação do Schema (DER e DBML)
├── legacy_v1/             # Histórico: Versão antiga em Excel
├── Scripts/               # Automação de Banco de Dados
│   ├── create_system_entities.py
│   ├── reset_bd.py
│   └── seed_corporate.py
├── src/                   # Core da Aplicação
│   ├── crud/              # Controllers e Regras de Negócio
│   ├── pages/             # Interfaces do Usuário
│   ├── database.py        # Conector Singleton (Engine SQLAlchemy)
│   ├── models.py          # Definição das Tabelas (Schema)
│   └── Home.py            # [Entry Point] Dashboard
├── requirements.txt       # Dependências
└── README.md              # Documentação Técnica
```

## 👤 Autor

Desenvolvido por **Adryel Almeida**
* 💼 [LinkedIn](https://www.linkedin.com/in/adryel-almeida-052365321/)
* 📂 [Portfólio GitHub](https://github.com/Adryel7)


