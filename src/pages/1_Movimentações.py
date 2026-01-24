import streamlit as st
from datetime import date

# --- IMPORTS ---
from crud.products import list_products
from crud.departments import list_departments
from crud.representatives import list_representatives
from crud.inventory_managers import list_managers
from crud.transactions import register_transaction

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
    
    st.markdown("---")
    st.info(
        "**SGE-Analytics v2.0**\n\n"
        "Sistema migrado de planilhas Excel para "
        "uma arquitetura escalável em Python e SQL na Nuvem."
    )

# --------------------------

# Configuração da Página
st.set_page_config(page_title="Controle de Movimentações", layout="wide")

st.title("📦 Controle de Estoque")
st.markdown("Selecione o tipo de operação nas abas abaixo.")

# ==============================================================================
# 1. INICIALIZAÇÃO DE ESTADO (SESSION STATE)
# ==============================================================================
# Inicializamos as variáveis na memória antes de criar os widgets.

campos_padrao = {
    'prod_out': None,
    'qtd_out': 1,
    'dt_out': date.today(),
    'dept_out': None,
    'rep_out': None,
    'mgr_out': None,
    'obs_out': ""
}

for chave, valor in campos_padrao.items():
    if chave not in st.session_state:
        st.session_state[chave] = valor

# ==============================================================================
# 2. CARREGAMENTO DE DADOS
# ==============================================================================
try:
    lista_depts = list_departments()
    lista_reps_bruta = list_representatives()
    
    # Criando mapas para busca rápida (O(1))
    mapa_produtos = {p['name']: p['id'] for p in list_products()}
    mapa_gerentes = {m['name']: m['id'] for m in list_managers()}
    mapa_depts = {d['name']: d['id'] for d in lista_depts}
    mapa_reps_geral = {r['name']: r['id'] for r in lista_reps_bruta}

    # Busca IDs das Entidades de Sistema (Estoque Geral / Sistema de Entrada)
    try:
        nome_dept_sistema = "ESTOQUE GERAL"
        nome_rep_sistema = "SISTEMA DE ENTRADA"
        
        id_dept_sistema = next(d['id'] for d in lista_depts if d['name'] == nome_dept_sistema)
        id_rep_sistema = next(r['id'] for r in lista_reps_bruta if r['name'] == nome_rep_sistema)
    except StopIteration:
        st.error("⛔ ERRO CRÍTICO: Entidades de Sistema não encontradas. Por favor, rode o script 'scripts/create_system_entities.py'.")
        st.stop()

except Exception as e:
    st.error(f"❌ Erro ao carregar dados do banco: {e}")
    st.stop()

# ==============================================================================
# 3. LÓGICA DE NEGÓCIO (CALLBACKS)
# ==============================================================================

def processar_saida():
    """
    Função chamada ao clicar no botão de Saída.
    Responsável por validar, persistir no banco e limpar o formulário.
    """
    # 1. Recupera valores do estado
    prod = st.session_state.prod_out
    qtd = st.session_state.qtd_out
    dt = st.session_state.dt_out
    dept_nome = st.session_state.dept_out
    rep_nome = st.session_state.rep_out
    mgr_nome = st.session_state.mgr_out
    obs = st.session_state.obs_out

    # 2. Validação de Campos Obrigatórios
    if not prod or not dept_nome or not rep_nome or not mgr_nome:
        st.error("⚠️ Preencha todos os campos obrigatórios (*).")
        return

    # 3. Persistência
    try:
        register_transaction(
            type='OUT',
            product_id=mapa_produtos[prod],
            quantity=qtd,
            transaction_date=dt,
            department_id=mapa_depts[dept_nome],
            representative_id=mapa_reps_geral[rep_nome],
            inventory_manager_id=mapa_gerentes[mgr_nome],
            obs=obs
        )
        st.toast(f"✅ Saída de '{prod}' registrada com sucesso!", icon="📤")
        
        # 4. Limpeza (Resetando o Session State para os valores padrão)
        st.session_state.prod_out = None
        st.session_state.qtd_out = 1
        st.session_state.dt_out = date.today()
        st.session_state.dept_out = None
        st.session_state.rep_out = None
        st.session_state.mgr_out = None
        st.session_state.obs_out = ""
        
    except ValueError as ve:
        st.error(f"⛔ {ve}")
    except Exception as e:
        st.error(f"Erro inesperado no sistema: {e}")

# ==============================================================================
# 4. INTERFACE DO USUÁRIO
# ==============================================================================
tab_entrada, tab_saida = st.tabs(["📥 Entrada (Abastecimento)", "📤 Saída (Requisição)"])

# --- ABA DE ENTRADA ---
with tab_entrada:
    st.header("Registrar Entrada")
    st.info(f"O material será registrado automaticamente no '{nome_dept_sistema}'.")
    
    # Utilizamos st.form aqui pois não há necessidade de interatividade dinâmica entre campos
    with st.form("form_entrada", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Pesquisar Produto *", options=list(mapa_produtos.keys()), index=None, placeholder="Digite para buscar...", key="prod_in")
            st.number_input("Quantidade *", min_value=1, key="qtd_in")
        with col2:
            st.date_input("Data *", value=date.today(), format="DD/MM/YYYY", key="dt_in")
            st.selectbox("Recebido por (Gerente) *", options=list(mapa_gerentes.keys()), index=None, placeholder="Quem recebeu?", key="mgr_in")

        st.text_area("Observações", key="obs_in")
        
        if st.form_submit_button("✅ Confirmar Entrada"):
            p_in = st.session_state.get('prod_in')
            g_in = st.session_state.get('mgr_in')
            
            if not p_in or not g_in:
                st.warning("⚠️ Preencha Produto e Gerente.")
            else:
                try:
                    register_transaction(
                        type='IN',
                        product_id=mapa_produtos[p_in],
                        quantity=st.session_state['qtd_in'],
                        transaction_date=st.session_state['dt_in'],
                        department_id=id_dept_sistema,
                        representative_id=id_rep_sistema,
                        inventory_manager_id=mapa_gerentes[g_in],
                        obs=st.session_state['obs_in']
                    )
                    st.toast(f"✅ Entrada registrada!", icon="📥")
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")

# --- ABA DE SAÍDA ---
with tab_saida:
    st.header("Registrar Saída")
    st.warning("Selecione o Departamento para ver os Representantes disponíveis.")
    
    c1, c2 = st.columns(2)
    
    with c1:
        # Widgets controlados puramente pelo Session State (sem value=... ou index=...)
        st.selectbox("Pesquisar Produto *", options=list(mapa_produtos.keys()), placeholder="Digite para buscar...", key="prod_out")
        st.number_input("Quantidade *", min_value=1, key="qtd_out")
        st.date_input("Data *", format="DD/MM/YYYY", key="dt_out")
        
    with c2:
        depts_reais = [name for name in mapa_depts.keys() if name != nome_dept_sistema]
        
        # 1. Seleção de Departamento
        dept_selecionado = st.selectbox(
            "Departamento Destino *", 
            options=depts_reais, 
            placeholder="Selecione o setor...", 
            key="dept_out"
        )
        
        # 2. Filtro Dinâmico de Representantes
        opcoes_reps_filtradas = []
        if dept_selecionado:
            id_dept_selecionado = mapa_depts[dept_selecionado]
            opcoes_reps_filtradas = [r['name'] for r in lista_reps_bruta if r['department_id'] == id_dept_selecionado]
        
        st.selectbox(
            "Retirado por (Rep.) *", 
            options=opcoes_reps_filtradas, 
            placeholder="Quem retirou?" if dept_selecionado else "Selecione o Depto...", 
            key="rep_out",
            disabled=(dept_selecionado is None)
        )

        st.selectbox("Autorizado por (Gerente) *", options=list(mapa_gerentes.keys()), placeholder="Quem autorizou?", key="mgr_out")

    st.text_area("Motivo / Ordem de Serviço", key="obs_out")
    
    # Botão com callback para processar e limpar
    st.button("🔻 Registrar Saída", type="primary", on_click=processar_saida)