import streamlit as st

# --- IMPORTS DAS FUNÇÕES CRUD ---
from crud.products import insert_product
from crud.categories import insert_category, list_categories
from crud.departments import insert_department, list_departments
from crud.representatives import insert_representative
from crud.inventory_managers import insert_manager

# --- AVISO DE PORTFÓLIO ---
st.info(
    "📢 **Aviso:** Este é um ambiente de demonstração compartilhado. "
    "Sinta-se à vontade para testar as funcionalidades. "
    "Os dados podem ser resetados periodicamente."
)
# --------------------------

# --- ASSINATURA NO SIDEBAR ---
with st.sidebar:
    st.markdown("### 👨‍💻 Sobre o Desenvolvedor")
    
    st.markdown("**Adryel Almeida**")
    st.caption("Engenharia de Computação | Engenharia de Dados")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.link_button("💼 LinkedIn", "https://www.linkedin.com/in/adryel-almeida-052365321/")
    
    with col2:
        st.link_button("🐙 GitHub", "https://github.com/Adryel7")
        
    with col1:
        st.link_button("📂 Repositório", "https://github.com/Adryel7/sge-fullstack-python")
    
    st.markdown("---")
    st.info(
        "**SGE-Analytics v2.0**\n\n"
        "Sistema migrado de planilhas Excel para "
        "uma arquitetura escalável em Python e SQL na Nuvem."
    )

# --------------------------

# Configuração da Página
st.set_page_config(page_title="Cadastros Gerais", layout="wide")

st.title("📝 Central de Cadastros")
st.markdown("Utilize as abas abaixo para inserir novos registros no sistema.")

# Criação das Abas
tab_prod, tab_cat, tab_dept, tab_team = st.tabs([
    "📦 Produtos", 
    "🏷️ Categorias", 
    "🏢 Departamentos", 
    "👥 Equipe (Gerentes/Rep)"
])

# ==============================================================================
# ABA 1: PRODUTOS
# ==============================================================================
with tab_prod:
    st.header("Novo Produto")
    
    # Busca categorias para o dropdown
    try:
        categorias_disponiveis = list_categories()
    except Exception as e:
        st.error(f"Erro ao carregar categorias: {e}")
        categorias_disponiveis = []
    
    if not categorias_disponiveis:
        st.warning("⚠️ Atenção: Você precisa cadastrar Categorias antes de criar Produtos!")
    else:
        with st.form("form_produto", clear_on_submit=True):
            # Mapeamento: Nome -> ID
            mapa_cat = {c['name']: c['id'] for c in categorias_disponiveis}
            
            col1, col2 = st.columns(2)
            with col1:
                nome_prod = st.text_input("Nome do Produto *")
                cat_selecionada = st.selectbox("Categoria *", options=list(mapa_cat.keys()))
            
            with col2:
                estoque_min = st.number_input("Estoque Mínimo (Alerta)", min_value=0, value=5, help="Quantidade mínima para gerar alerta de reposição.")
            
            desc_prod = st.text_area("Descrição Detalhada")
            
            submitted_prod = st.form_submit_button("Salvar Produto")
            
            if submitted_prod:
                if not nome_prod:
                    st.error("O nome do produto é obrigatório.")
                else:
                    try:
                        insert_product(
                            name=nome_prod,
                            category_id=mapa_cat[cat_selecionada],
                            description=desc_prod,
                            min_balance=estoque_min
                        )
                        st.success(f"✅ Produto '{nome_prod}' cadastrado com sucesso!")
                    except Exception as e:
                        st.error(f"❌ Erro ao salvar produto: {e}")

# ==============================================================================
# ABA 2: CATEGORIAS
# ==============================================================================
with tab_cat:
    st.header("Nova Categoria")
    with st.form("form_categoria", clear_on_submit=True):
        nome_cat = st.text_input("Nome da Categoria *")
        submitted_cat = st.form_submit_button("Salvar Categoria")
        
        if submitted_cat:
            if not nome_cat:
                st.error("O nome da categoria não pode ser vazio.")
            else:
                try:
                    insert_category(nome_cat)
                    st.success(f"✅ Categoria '{nome_cat}' criada!")
                except Exception as e:
                    st.error(f"❌ Erro ao salvar categoria: {e}")

# ==============================================================================
# ABA 3: DEPARTAMENTOS
# ==============================================================================
with tab_dept:
    st.header("Novo Departamento")
    with st.form("form_dept", clear_on_submit=True):
        nome_dept = st.text_input("Nome do Departamento / Centro de Custo *")
        submitted_dept = st.form_submit_button("Salvar Departamento")
        
        if submitted_dept:
            if not nome_dept:
                st.error("Digite o nome do departamento.")
            else:
                try:
                    insert_department(nome_dept)
                    st.success(f"✅ Departamento '{nome_dept}' criado!")
                except Exception as e:
                    st.error(f"❌ Erro ao salvar departamento: {e}")

# ==============================================================================
# ABA 4: EQUIPE (Gerentes e Representantes)
# ==============================================================================
with tab_team:
    col_gerente, col_rep = st.columns(2)
    
    # --- GERENTES DE INVENTÁRIO ---
    with col_gerente:
        st.subheader("Novo Gerente de Inventário")
        st.caption("Responsáveis por dar entrada e autorizar saídas.")
        
        with st.form("form_gerente", clear_on_submit=True):
            nome_mgr = st.text_input("Nome do Gerente *")
            submit_mgr = st.form_submit_button("Salvar Gerente")
            
            if submit_mgr:
                if not nome_mgr:
                    st.error("Nome obrigatório.")
                else:
                    try:
                        insert_manager(nome_mgr)
                        st.success(f"✅ Gerente '{nome_mgr}' cadastrado!")
                    except Exception as e:
                        st.error(f"❌ Erro: {e}")

    # --- REPRESENTANTES (Retiram material) ---
    with col_rep:
        st.subheader("Novo Representante")
        st.caption("Pessoas autorizadas a retirar material para um setor.")
        
        try:
            # Filtramos "ESTOQUE GERAL" para evitar criar representantes para o sistema
            deptos_todos = list_departments()
            deptos_disponiveis = [d for d in deptos_todos if d['name'] != "ESTOQUE GERAL"]
        except Exception:
            deptos_disponiveis = []
        
        if not deptos_disponiveis:
            st.warning("⚠️ Cadastre Departamentos (Setores) primeiro.")
        else:
            with st.form("form_rep", clear_on_submit=True):
                nome_rep = st.text_input("Nome do Representante *")
                
                # Mapeamento Dept Nome -> ID
                mapa_dept = {d['name']: d['id'] for d in deptos_disponiveis}
                dept_rep = st.selectbox("Departamento Vinculado *", options=list(mapa_dept.keys()))
                
                submit_rep = st.form_submit_button("Salvar Representante")
                
                if submit_rep:
                    if not nome_rep:
                        st.error("Nome obrigatório.")
                    else:
                        try:
                            insert_representative(name=nome_rep, dept_id=mapa_dept[dept_rep])
                            st.success(f"✅ Representante '{nome_rep}' vinculado ao setor '{dept_rep}'!")
                        except Exception as e:
                            st.error(f"❌ Erro ao salvar: {e}")