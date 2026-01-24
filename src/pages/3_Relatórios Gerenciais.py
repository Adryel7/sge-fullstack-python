import streamlit as st
import pandas as pd
from datetime import date, timedelta
import time

# IMPORTS
from crud.products import list_products, delete_product
from crud.categories import list_categories, delete_category
from crud.departments import list_departments
from crud.representatives import list_representatives, delete_representative
from crud.inventory_managers import list_managers
from crud.transactions import list_transactions, delete_transaction, update_transaction

st.info(
    "📢 **Aviso:** Este é um ambiente de demonstração compartilhado. "
    "Sinta-se à vontade para testar as funcionalidades. "
    "Os dados podem ser resetados periodicamente. "
    "Senha para a Área Administrativa: 1234"
)

# --------------------------

st.set_page_config(page_title="Relatórios e Gestão", layout="wide")
st.title("📑 Relatórios e Gestão")

# Carregamento de dados
try:
    raw_prods = list_products()
    raw_cats = list_categories()
    raw_depts = list_departments()
    raw_reps = list_representatives()
    raw_mgrs = list_managers()
    raw_trans_objs = list_transactions()

    df_trans = pd.DataFrame([{
        "id": t.id, "type": t.type, "quantity": t.quantity, "date": t.transaction_date, 
        "obs": t.obs, "product_id": t.product_id, "department_id": t.department_id, 
        "representative_id": t.representative_id, "inventory_manager_id": t.inventory_manager_id
    } for t in raw_trans_objs]) if raw_trans_objs else pd.DataFrame()

except Exception as e:
    st.error(f"Erro de conexão: {e}")
    st.stop()

# Abas Principais
tab_view, tab_admin = st.tabs(["📊 Visualização Geral", "🛡️ Área Administrativa"])

# ==============================================================================
# ABA 1: VISUALIZAÇÃO GERAL (Nova Estrutura)
# ==============================================================================
with tab_view:
    # Sub-abas para organizar a visualização
    sub_tab_trans, sub_tab_cadastros = st.tabs(["🚚 Transações", "👥 Cadastros Auxiliares (RH/Setores)"])

    # --- 1.1 TRANSAÇÕES ---
    with sub_tab_trans:
        st.markdown("#### Histórico de Movimentações")
        c1, c2 = st.columns(2)
        dt_inicio = c1.date_input("De", date.today() - timedelta(days=30))
        dt_fim = c2.date_input("Até", date.today())

        if not df_trans.empty:
            df_full = df_trans.copy()
            
            # Mapeamentos (ID -> Nome)
            map_prod = {p['id']: p['name'] for p in raw_prods}
            map_dept = {d['id']: d['name'] for d in raw_depts}
            map_rep = {r['id']: r['name'] for r in raw_reps}
            map_mgr = {m['id']: m['name'] for m in raw_mgrs}

            df_full['Produto'] = df_full['product_id'].map(map_prod)
            df_full['Setor'] = df_full['department_id'].map(map_dept)
            df_full['Solicitante'] = df_full['representative_id'].map(map_rep)
            df_full['Autorizou'] = df_full['inventory_manager_id'].map(map_mgr)
            
            # Filtro Data
            df_full['date'] = pd.to_datetime(df_full['date']).dt.date
            mask = (df_full['date'] >= dt_inicio) & (df_full['date'] <= dt_fim)
            
            # Exibição
            df_show = df_full.loc[mask][['id', 'date', 'type', 'quantity', 'Produto', 'Setor', 'Solicitante', 'Autorizou', 'obs']]
            
            st.dataframe(
                df_show, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "date": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
                    "type": "Tipo",
                    "quantity": "Qtd"
                }
            )
        else:
            st.info("Sem dados.")

    # --- 1.2 CADASTROS AUXILIARES (O que você pediu) ---
    with sub_tab_cadastros:
        col_reps, col_depts, col_mgrs = st.columns(3)

        with col_reps:
            st.markdown("##### 👤 Representantes")
            if raw_reps:
                # Cria DF enriquecido com nome do departamento
                data_reps = []
                map_dept = {d['id']: d['name'] for d in raw_depts}
                for r in raw_reps:
                    if r['name'] != "SISTEMA DE ENTRADA":
                        data_reps.append({
                            "Nome": r['name'],
                            "Departamento": map_dept.get(r['department_id'], "N/A")
                        })
                st.dataframe(pd.DataFrame(data_reps), hide_index=True, use_container_width=True)
            else:
                st.info("Vazio")

        with col_depts:
            st.markdown("##### 🏢 Departamentos")
            if raw_depts:
                # Filtra Estoque Geral da visualização se quiser, ou mantém
                df_d = pd.DataFrame(raw_depts)[['name']]
                df_d.columns = ["Nome do Setor"]
                st.dataframe(df_d, hide_index=True, use_container_width=True)
            else:
                st.info("Vazio")

        with col_mgrs:
            st.markdown("##### 👔 Gerentes / Auditores")
            if raw_mgrs:
                df_m = pd.DataFrame(raw_mgrs)[['name']]
                df_m.columns = ["Nome"]
                st.dataframe(df_m, hide_index=True, use_container_width=True)
            else:
                st.info("Vazio")

# ==============================================================================
# ABA 2: ÁREA ADMINISTRATIVA (Mantida Igual)
# ==============================================================================
with tab_admin:
    st.error("⚠️ Área de Risco: Ações aqui são irreversíveis.")
    senha = st.text_input("Digite a senha de administrador:", type="password")
    
    if senha == "1234": 
        st.success("Acesso Liberado ✅")
        op_admin = st.radio("Gerenciar:", ["Movimentações (Corrigir Erros)", "Cadastros (Excluir Itens)"], horizontal=True)
        st.divider()

        if op_admin.startswith("Movimentações"):
            st.subheader("📝 Editar ou Excluir Transação")
            trans_id = st.number_input("ID da Transação", min_value=1, step=1)
            
            trans_atual = next((t for t in raw_trans_objs if t.id == trans_id), None)
            
            if trans_atual:
                prod_nome = next((p['name'] for p in raw_prods if p['id'] == trans_atual.product_id), "Desconhecido")
                st.info(f"Selecionado: {trans_atual.type} de {trans_atual.quantity}x {prod_nome}")
                
                c_edit, c_del = st.columns(2)
                with c_edit:
                    with st.form("edit_trans"):
                        nq = st.number_input("Qtd", min_value=1, value=trans_atual.quantity)
                        nd = st.date_input("Data", value=trans_atual.transaction_date)
                        no = st.text_area("Obs", value=trans_atual.obs)
                        if st.form_submit_button("Salvar"):
                            try:
                                update_transaction(trans_id, nq, no, nd)
                                st.toast("Sucesso!"); time.sleep(1); st.rerun()
                            except Exception as e: st.error(e)
                with c_del:
                    st.warning("Excluir estorna o estoque.")
                    if st.button("❌ Excluir"):
                        try:
                            delete_transaction(trans_id)
                            st.success("Excluído!"); time.sleep(1); st.rerun()
                        except Exception as e: st.error(e)
            elif trans_id:
                st.warning("ID não encontrado.")

        else:
            st.subheader("🗑️ Exclusão de Cadastros")
            tipo_del = st.selectbox("Tipo", ["Produto", "Categoria", "Representante"])
            
            sel = None # Inicializa variavel
            id_sel = None
            func = None

            if tipo_del == "Produto":
                names = [p['name'] for p in raw_prods]
                sel = st.selectbox("Item", names)
                func = delete_product
                if sel:
                    id_sel = next(p['id'] for p in raw_prods if p['name'] == sel)

            elif tipo_del == "Categoria":
                names = [c['name'] for c in raw_cats]
                sel = st.selectbox("Item", names)
                func = delete_category
                if sel:
                    id_sel = next(c['id'] for c in raw_cats if c['name'] == sel)

            elif tipo_del == "Representante":
                # LÓGICA NOVA SOLICITADA
                # 1. Mapear Setores
                dept_dict = {d['name']: d['id'] for d in raw_depts}
                
                # 2. Escolher Setor Primeiro
                dept_escolhido = st.selectbox("Filtrar por Setor:", list(dept_dict.keys()))
                id_dept_escolhido = dept_dict[dept_escolhido]

                # 3. Filtrar Representantes daquele setor (Excluindo Sistema)
                reps_filtrados = [
                    r for r in raw_reps 
                    if r['department_id'] == id_dept_escolhido 
                    and r['name'] != "SISTEMA DE ENTRADA"
                ]

                if not reps_filtrados:
                    st.warning(f"Não há representantes cadastrados no setor {dept_escolhido}.")
                    st.stop() # Interrompe aqui para não dar erro no botão abaixo
                else:
                    names = [r['name'] for r in reps_filtrados]
                    sel = st.selectbox("Selecione o Representante:", names)
                    func = delete_representative
                    if sel:
                        id_sel = next(r['id'] for r in reps_filtrados if r['name'] == sel)

            if sel and st.button(f"Excluir '{sel}'"):
                try:
                    if func(id_sel): st.success("Feito!"); time.sleep(1); st.rerun()
                    else: st.warning("Erro ao excluir (possui vínculos?).")
                except Exception as e: st.error(f"Erro: {e}")
    elif senha:
        st.error("Senha incorreta.")