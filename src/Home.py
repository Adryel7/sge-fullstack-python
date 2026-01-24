import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta

# --- IMPORTS CRUD ---
from crud.products import list_products
from crud.transactions import list_transactions
from crud.departments import list_departments

# --- AVISO DE PORTFÓLIO ---
st.info(
    "📢 **Aviso:** Este é um ambiente de demonstração compartilhado. "
    "Sinta-se à vontade para testar as funcionalidades. "
    "Os dados podem ser resetados periodicamente."
)
# --------------------------

# Configuração da Página
st.set_page_config(page_title="Dashboard Gerencial", layout="wide")

# ==============================================================================
# 1. FUNÇÃO DE CARGA E TRATAMENTO DE DADOS
# ==============================================================================
def carregar_dados_seguros():
    """
    Carrega dados do banco e converte para DataFrame com segurança.
    """
    # Produtos
    raw_prods = list_products()
    if not raw_prods:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    df_prods = pd.DataFrame(raw_prods)

    # Departamentos
    raw_depts = list_departments()
    df_depts = pd.DataFrame(raw_depts) if raw_depts else pd.DataFrame()

    # Transações
    raw_trans = list_transactions()
    data_trans = []
    if raw_trans:
        for t in raw_trans:
            data_trans.append({
                "type": t.type,
                "quantity": t.quantity,
                "transaction_date": t.transaction_date,
                "product_id": t.product_id,
                "department_id": t.department_id,
            })
    df_trans = pd.DataFrame(data_trans)
    
    return df_prods, df_trans, df_depts

# Executa a carga
df_prods, df_trans, df_depts = carregar_dados_seguros()

if df_prods.empty:
    st.warning("⚠️ Nenhum dado encontrado. Cadastre produtos e movimentações.")
    st.stop()

# ==============================================================================
# 2. BARRA LATERAL (FILTROS)
# ==============================================================================
st.sidebar.header("📅 Filtro de Período")
data_inicio = st.sidebar.date_input("Data Inicial", date.today() - timedelta(days=30), format="DD/MM/YYYY")
data_fim = st.sidebar.date_input("Data Final", date.today(), format="DD/MM/YYYY")

# Aplicação do Filtro nas Transações
df_trans_filtrado = pd.DataFrame()
if not df_trans.empty:
    df_trans['transaction_date'] = pd.to_datetime(df_trans['transaction_date']).dt.date
    mask = (df_trans['transaction_date'] >= data_inicio) & (df_trans['transaction_date'] <= data_fim)
    df_trans_filtrado = df_trans.loc[mask]

st.title(f"📊 Dashboard Gerencial")
st.caption(f"Período: {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}")

# ==============================================================================
# 3. CÁLCULO DE ALERTAS E KPIs
# ==============================================================================
# Define ponto de alerta: Mínimo + 20%
df_prods['ponto_alerta'] = df_prods['min_balance'].fillna(0) * 1.20
df_alertas = df_prods[df_prods['stock'] <= df_prods['ponto_alerta']].copy()

col_kpi1, col_kpi2 = st.columns(2)
col_kpi1.metric("📦 Total de Produtos", len(df_prods))
col_kpi2.metric("🚨 Alerta de Reposição (+20%)", len(df_alertas), delta_color="inverse")

st.markdown("---")

# ==============================================================================
# 4. TABELA RESUMO DE MOVIMENTAÇÕES (NOVIDADE AQUI) 🆕
# ==============================================================================
st.subheader("📋 Resumo de Movimentações por Produto")
st.caption("Total de entradas e saídas no período selecionado vs. Saldo Atual.")

# Prepara os dados agrupados do período filtrado
if not df_trans_filtrado.empty:
    # Soma entradas do período
    entradas_periodo = df_trans_filtrado[df_trans_filtrado['type'] == 'IN'].groupby('product_id')['quantity'].sum()
    # Soma saídas do período
    saidas_periodo = df_trans_filtrado[df_trans_filtrado['type'] == 'OUT'].groupby('product_id')['quantity'].sum()
else:
    entradas_periodo = pd.Series()
    saidas_periodo = pd.Series()

# Merge com a tabela de produtos (Left Join para manter todos os produtos)
# Usamos set_index('id') em df_prods para facilitar o mapeamento
df_resumo = df_prods.set_index('id').copy()
df_resumo['Entradas (Período)'] = entradas_periodo
df_resumo['Saídas (Período)'] = saidas_periodo

# Limpeza: Preenche NaN com 0 (produtos sem movimento no período)
df_resumo['Entradas (Período)'] = df_resumo['Entradas (Período)'].fillna(0).astype(int)
df_resumo['Saídas (Período)'] = df_resumo['Saídas (Período)'].fillna(0).astype(int)

# Seleção e Renomeação de Colunas
df_tabela_final = df_resumo[['name', 'category', 'Entradas (Período)', 'Saídas (Período)', 'stock']].reset_index(drop=True)
df_tabela_final = df_tabela_final.rename(columns={
    'name': 'Produto',
    'category': 'Categoria',
    'stock': 'Saldo Atual'
})

# Exibição da Tabela
st.dataframe(
    df_tabela_final,
    use_container_width=True,
    column_config={
        "Saldo Atual": st.column_config.NumberColumn(format="%d"),
        "Entradas (Período)": st.column_config.NumberColumn(format="%d 📥"),
        "Saídas (Período)": st.column_config.NumberColumn(format="%d 📤")
    },
    hide_index=True
)

st.markdown("---")

# ==============================================================================
# 5. GRÁFICOS GERAIS
# ==============================================================================
# Preparação dos dados para gráficos
df_completo = pd.DataFrame()
if not df_trans_filtrado.empty:
    if not df_depts.empty:
        df_depts_clean = df_depts.rename(columns={'name': 'department_name', 'id': 'dept_id_ref'})
        df_completo = pd.merge(df_trans_filtrado, df_depts_clean, left_on='department_id', right_on='dept_id_ref', how='left')
    else:
        df_completo = df_trans_filtrado.copy()
        df_completo['department_name'] = "N/A"

col_graph1, col_graph2 = st.columns([2, 1])
df_saidas = pd.DataFrame()

if not df_completo.empty:
    df_saidas = df_completo[
        (df_completo['type'] == 'OUT') & 
        (df_completo['department_name'] != 'ESTOQUE GERAL')
    ].copy()

with col_graph1:
    st.subheader("Fluxo Geral de Saídas por Setor")
    if not df_saidas.empty:
        kpi_custo = df_saidas.groupby('department_name')['quantity'].sum().reset_index().sort_values(by='quantity', ascending=True)
        fig1 = px.bar(
            kpi_custo, x='quantity', y='department_name', orientation='h', text_auto=True,
            labels={'quantity': 'Qtd', 'department_name': 'Departamento'},
            color='quantity', color_continuous_scale='Reds'
        )
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Sem dados de saída no período.")

with col_graph2:
    st.subheader("Entradas vs Saídas")
    if not df_completo.empty:
        kpi_mov = df_completo.groupby('type')['quantity'].sum().reset_index()
        color_map = {'IN': '#2ecc71', 'in': '#2ecc71', 'OUT': '#e74c3c', 'out': '#e74c3c'}
        fig2 = px.pie(kpi_mov, names='type', values='quantity', hole=0.4, color='type', color_discrete_map=color_map)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Sem movimentações.")

# ==============================================================================
# 6. DETALHAMENTO E ANÁLISE (MATRIZ)
# ==============================================================================
st.markdown("---")
st.header("🔍 Detalhamento e Análise")

if not df_saidas.empty:
    # Merge com Produtos para ter o nome
    df_prods_clean = df_prods.rename(columns={'name': 'product_name', 'id': 'prod_id_ref'})[['prod_id_ref', 'product_name']]
    df_saidas_nomes = pd.merge(df_saidas, df_prods_clean, left_on='product_id', right_on='prod_id_ref', how='left')

    st.subheader("📋 Matriz de Consumo (Setor x Produto)")
    
    df_pivot = None
    try:
        df_pivot = pd.pivot_table(
            df_saidas_nomes, values='quantity', index='department_name', 
            columns='product_name', aggfunc='sum', fill_value=0
        )
        # Filtro de linhas/colunas zeradas
        df_pivot = df_pivot.loc[(df_pivot.sum(axis=1) != 0), (df_pivot.sum(axis=0) != 0)]

        styler = df_pivot.style\
            .background_gradient(cmap="Reds", axis=None)\
            .format("{:.0f}")\
            .set_properties(**{'border': '1px solid #d3d3d3', 'color': 'black', 'text-align': 'center'})
            
        st.dataframe(styler, use_container_width=True)
    except Exception:
        if df_pivot is not None:
            st.dataframe(df_pivot, use_container_width=True)
else:
    st.info("Dados insuficientes para gerar matriz.")

# ==============================================================================
# 7. LISTA DE REPOSIÇÃO (ALERTAS)
# ==============================================================================
st.markdown("---")
st.subheader("⚠️ Lista de Reposição")
st.caption("Produtos com estoque CRÍTICO ou em ATENÇÃO.")

def definir_status(row):
    if row['stock'] <= row['min_balance']: return "CRÍTICO 🔴"
    else: return "ATENÇÃO 🟡"

if not df_alertas.empty:
    df_alertas['status'] = df_alertas.apply(definir_status, axis=1)
    df_show = df_alertas[['status', 'name', 'category', 'stock', 'min_balance', 'ponto_alerta']]
    
    st.dataframe(
        df_show,
        column_config={
            "status": "Situação",
            "name": "Produto",
            "category": "Categoria",
            "stock": st.column_config.NumberColumn("Estoque Atual", format="%d"),
            "min_balance": st.column_config.NumberColumn("Mínimo", format="%d"),
            "ponto_alerta": st.column_config.NumberColumn("Margem (+20%)", format="%.1f"),
        },
        use_container_width=True,
        hide_index=True
    )
else:
    st.success("✅ Tudo certo! Estoque saudável.")