# 📊 Sistema de Controle de Estoque Automatizado

> Uma solução simples de gestão de inventário baseada em lógica de Banco de Dados Relacional, desenvolvida para otimizar o fluxo de materiais e eliminar erros manuais.

![Status do Projeto](https://img.shields.io/badge/Status-Concluído-green)
![Plataforma](https://img.shields.io/badge/Plataforma-LibreOffice%20%7C%20Excel-blue)

## 📸 Visão Geral

<img width="1318" height="747" alt="DASHBOARD-PRINT" src="https://github.com/user-attachments/assets/c5eed63f-c661-4d43-b54e-c8297fe1878e" />


Este projeto nasceu da necessidade de transformar um controle de estoque manual em um **sistema unificado**. Utilizando recursos avançados de planilhas, o sistema automatiza o cálculo de saldos, previne erros de digitação e gera inteligência de dados para tomada de decisão.

## 🚀 Funcionalidades Principais

* **Dashboard em Tempo Real:** Monitoramento automático do saldo atual vs. estoque mínimo.
* **Alertas Visuais:** Sistema de "Semáforo" (Formatação Condicional) que avisa automaticamente quando é necessário comprar (`COMPRAR URGENTE` / `ATENÇÃO` / `OK`).
* **Integridade de Dados:** Uso de validação de dados (Drop-downs) para impedir erros de digitação em nomes de setores e categorias.
* **Relatórios Dinâmicos:** Uso de Tabelas Dinâmicas (Pivot Tables) para análise de consumo mensal por centro de custo (Destino).
* **Rastreabilidade:** Histórico completo de Entradas e Saídas centralizado.

## 🛠️ Tecnologias e Conceitos Aplicados

Embora construído em planilha, o projeto segue princípios de Engenharia de Software e Banco de Dados:

* **LibreOffice Calc / Excel:** Ferramentas base.
* **Modelagem de Dados:** Separação estrita entre Camada de Dados (Entradas/Saídas), Camada de Regras (Informações Padrão) e Camada de Apresentação (Dashboard).
* **Fórmulas Avançadas:** `SOMASES` (SUMIFS) para agregação de dados e lógicas condicionais aninhadas (`SE`).
* **Normalização:** Padronização de nomes e categorias para evitar redundância.

## 📂 Estrutura do Arquivo

O sistema é composto por abas interconectadas:

1.  **Controle Detalhado (Dashboard):** A "Home" do sistema. Exibe o SKU, descrição, saldos calculados e status de compra.
2.  **Entradas:** Log de recebimento de notas fiscais e fornecedores.
3.  **Saídas:** Log de requisições internas.
4.  **Relatório de Saídas:** Matriz dinâmica que cruza *Produtos* x *Destinos* para análise de custos.
5.  **Informações Padrão:** Banco de dados auxiliar para alimentar as listas suspensas.

## 💻 Como Usar

1.  Baixe o arquivo `.xlsx` neste repositório.
2.  Abra no **LibreOffice Calc** ou **Microsoft Excel**.
3.  Cadastre novos produtos na aba `Controle Detalhado`.
4.  Lance as movimentações nas abas `Entradas` e `Saídas`.
5.  Verifique os indicadores de compra mudarem automaticamente no Painel Principal.

---

### 👤 Autor

Desenvolvido por **Adryel Almeida**
* [LinkedIn](https://www.linkedin.com/in/adryel-almeida-052365321/)
* [Portfólio](https://github.com/Adryel7)
