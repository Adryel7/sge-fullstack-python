import sys
import os
import random
from datetime import date, timedelta

# Ajuste de PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from crud.departments import insert_department, list_departments
from crud.categories import insert_category, list_categories
from crud.inventory_managers import insert_manager, list_managers
from crud.representatives import insert_representative, list_representatives
from crud.products import insert_product, list_products
from crud.transactions import register_transaction

# --- GERADOR DE NOMES REAIS ---
NOMES = [
    "Ana", "Bruno", "Carlos", "Daniela", "Eduardo", "Fernanda", "Gabriel", "Helena", "Igor", "Juliana", 
    "Lucas", "Mariana", "Nicolas", "Patrícia", "Rafael", "Sofia", "Thiago", "Vanessa", "Wagner", "Yasmin",
    "Ricardo", "Beatriz", "Cláudio", "Larissa", "Felipe", "Renata", "Gustavo", "Cecília", "Marcelo", "Letícia"
]
SOBRENOMES = [
    "Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves", "Pereira", "Lima", "Gomes", 
    "Costa", "Ribeiro", "Martins", "Carvalho", "Almeida", "Lopes", "Soares", "Barbosa", "Vieira", "Dias",
    "Moura", "Teixeira", "Mendes", "Nunes", "Cardoso", "Ramos", "Rocha", "Machado", "Reis", "Guimarães"
]

def gerar_nome_completo():
    return f"{random.choice(NOMES)} {random.choice(SOBRENOMES)}"

# --- DADOS MESTRES ---
DEPARTAMENTOS = [
    "TI - Infraestrutura", "TI - Desenvolvimento", "Recursos Humanos", "Financeiro", 
    "Marketing", "Comercial", "Operações", "Jurídico", "Logística", "Diretoria", 
    "Manutenção Predial", "Segurança do Trabalho", "ESTOQUE GERAL"
]

CATEGORIAS = [
    "Hardware", "Periféricos", "Material de Escritório", "Redes & Conectividade", 
    "Copa & Cozinha", "Limpeza & Higiene", "Mobiliário Corporativo", 
    "Ferramentas & Manutenção", "EPI & Segurança"
]

GERENTES = [
    "Carlos Eduardo (Diretor)", "Fernanda Lima (RH)", 
    "Roberto Justos (Auditor)", "Amanda Souza (Gerente Adm)"
]

# ~90 PRODUTOS REAIS
PRODUTOS_POR_CATEGORIA = {
    "Hardware": [
        ("Notebook Dell Latitude 5420", "i5 16GB SSD 512GB", 10),
        ("Notebook Dell XPS 13", "i7 Ultra Slim", 5),
        ("Notebook Lenovo ThinkPad", "Corporativo Resistente", 8),
        ("Monitor Dell 24 Polegadas", "P2419H Full HD", 15),
        ("Monitor LG Ultrawide 29", "IPS HDR10", 5),
        ("Monitor Samsung Curvo 27", "Para Designers", 3),
        ("Desktop HP ProDesk", "Mini PC i5", 10),
        ("Tablet Samsung Tab S7", "Para Vendas Externas", 5),
        ("iPad Pro 11", "Uso da Diretoria", 2),
        ("HD Externo Seagate 2TB", "Backup USB 3.0", 10),
        ("SSD Externo Sandisk 1TB", "Portátil USB-C", 5)
    ],
    "Periféricos": [
        ("Teclado Logitech K120", "ABNT2 USB", 40),
        ("Teclado Mecânico Redragon", "Switch Brown", 10),
        ("Kit Teclado e Mouse Sem Fio", "Logitech MK220", 25),
        ("Mouse Óptico Dell", "USB Preto", 50),
        ("Mouse Ergonômico Vertical", "Logitech Lift", 5),
        ("Headset Jabra Evolve 20", "USB Profissional", 20),
        ("Headset Logitech H390", "USB Noise Cancelling", 15),
        ("Webcam Logitech C920", "Full HD 1080p", 10),
        ("Webcam C925e", "Empresarial com Capa", 5),
        ("Caixa de Som USB", "Pequena para PC", 10)
    ],
    "Material de Escritório": [
        ("Papel A4 Chamex (Caixa)", "5 resmas 75g", 80),
        ("Caneta Bic Azul (Cx)", "50 unidades", 50),
        ("Caneta Bic Preta (Cx)", "50 unidades", 50),
        ("Caneta Marca Texto Amarela", "Cx 12 unidades", 20),
        ("Bloco Post-it Amarelo", "76x76mm", 100),
        ("Grampeador Metal 26/6", "Grande", 15),
        ("Grampos 26/6 (Cx)", "5000 unidades", 30),
        ("Pasta Suspensa Kraft", "Cx 50 unidades", 40),
        ("Pasta L Transparente", "Pacote 10un", 30),
        ("Cola Bastão 20g", "Pritt", 20),
        ("Tesoura 21cm", "Aço Inox", 15),
        ("Calculadora Científica", "Casio", 5),
        ("Envelope Pardo A4", "Cx 100un", 10),
        ("Crachá com Cordão", "Unidade", 100)
    ],
    "Redes & Conectividade": [
        ("Patch Cord CAT6 1.5m", "Azul Furukawa", 100),
        ("Patch Cord CAT6 3.0m", "Vermelho Furukawa", 60),
        ("Switch Ubiquiti 24p", "Gerenciável PoE", 3),
        ("Switch TP-Link 8p", "Gigabit Mesa", 10),
        ("Access Point Wi-Fi 6", "UniFi Lite", 5),
        ("Cabo HDMI 2.0 3m", "Blindado 4K", 20),
        ("Adaptador USB-C para HDMI", "Dell Original", 10),
        ("Adaptador USB-C para RJ45", "Rede Gigabit", 10),
        ("Filtro de Linha 6 Tomadas", "Clamper Energia", 30),
        ("Nobreak SMS 1200VA", "Estação de Trabalho", 5)
    ],
    "Copa & Cozinha": [
        ("Café em Pó (500g)", "Melitta Tradicional", 50),
        ("Açúcar Refinado (1kg)", "União", 50),
        ("Adoçante Líquido", "Zero Cal", 30),
        ("Copo Descartável 200ml", "Cx 2500un", 30),
        ("Copo Café 50ml", "Cx 3000un", 30),
        ("Mexedor de Café", "Pacote 500un", 20),
        ("Chá de Camomila", "Cx 25 sachês", 15),
        ("Garrafa Térmica 1.8L", "Inox Pressão", 5)
    ],
    "Limpeza & Higiene": [
        ("Álcool 70% (1L)", "Líquido", 40),
        ("Papel Toalha Interfolha", "Fardo Luxo", 60),
        ("Papel Higiênico Rolão", "Fardo 8 rolos", 40),
        ("Detergente Neutro", "Ypê 500ml", 40),
        ("Sabonete Líquido 5L", "Erva Doce", 10),
        ("Saco de Lixo 100L", "Pacote 100un", 20),
        ("Esponja Dupla Face", "Pacote 4un", 15),
        ("Pano Multiuso", "Rolo Azul", 10)
    ],
    "Mobiliário Corporativo": [
        ("Cadeira Ergonômica Mesh", "Presidente Preta", 5),
        ("Cadeira Secretária", "Com braços", 10),
        ("Suporte Monitor Articulado", "Pistão a Gás", 10),
        ("Apoio de Pés", "Plástico Ajustável", 20),
        ("Luminária de Mesa", "LED USB", 5)
    ],
    "Ferramentas & Manutenção": [
        ("Parafusadeira Bosch", "Bateria 12V", 2),
        ("Jogo de Chaves Fenda/Philips", "Tramontina", 3),
        ("Alicate Universal", "Isolado", 3),
        ("Fita Isolante 20m", "3M Imperial", 20),
        ("Abraçadeira Nylon (Enforca Gato)", "Pct 100un", 30),
        ("WD-40 Spray", "Lubrificante", 10)
    ],
    "EPI & Segurança": [
        ("Capacete de Segurança", "Branco Aba Frontal", 10),
        ("Óculos de Proteção", "Incolor", 20),
        ("Luva Pigmentada", "Par", 50),
        ("Protetor Auricular", "Plug Silicone", 50),
        ("Colete Refletivo", "Tamanho G", 10)
    ]
}

# Funções Auxiliares "Get or Create" para evitar duplicatas
def get_or_create_dept(name):
    existentes = list_departments()
    for d in existentes:
        if d['name'] == name: return d['id']
    insert_department(name)
    return next(d['id'] for d in list_departments() if d['name'] == name)

def get_or_create_cat(name):
    existentes = list_categories()
    for c in existentes:
        if c['name'] == name: return c['id']
    insert_category(name)
    return next(c['id'] for c in list_categories() if c['name'] == name)

def get_or_create_mgr(name):
    existentes = list_managers()
    for m in existentes:
        if m['name'] == name: return m['id']
    insert_manager(name)
    return next(m['id'] for m in list_managers() if m['name'] == name)

def get_or_create_prod(name, cat_id, desc, min_bal):
    existentes = list_products()
    for p in existentes:
        if p['name'] == name: return p['id']
    insert_product(name, cat_id, desc, min_bal)
    return next(p['id'] for p in list_products() if p['name'] == name)

def seed_data_v2():
    print("🚀 Iniciando Carga de Dados V2 (80+ Itens, Nomes Reais)...")

    # 1. MESTRES
    map_dept_ids = {d: get_or_create_dept(d) for d in DEPARTAMENTOS}
    map_cat_ids = {c: get_or_create_cat(c) for c in CATEGORIAS}
    mgr_ids = [get_or_create_mgr(m) for m in GERENTES]
    id_estoque_geral = map_dept_ids["ESTOQUE GERAL"]

    # 2. REPRESENTANTES
    # Verifica sistema
    all_reps = list_representatives()
    id_rep_sistema = next((r['id'] for r in all_reps if r['name'] == "SISTEMA DE ENTRADA"), None)
    if not id_rep_sistema:
        insert_representative("SISTEMA DE ENTRADA", id_estoque_geral)
        all_reps = list_representatives()
        id_rep_sistema = next(r['id'] for r in all_reps if r['name'] == "SISTEMA DE ENTRADA")

    # Cria pessoas reais por departamento (se tiver pouca gente)
    print("👥 Verificando Equipes...")
    for dept_name, dept_id in map_dept_ids.items():
        if dept_name == "ESTOQUE GERAL": continue
        
        reps_do_dept = [r for r in all_reps if r['department_id'] == dept_id]
        
        # Garante pelo menos 4 pessoas por setor
        qtd_atual = len(reps_do_dept)
        qtd_meta = 4
        
        if qtd_atual < qtd_meta:
            for _ in range(qtd_meta - qtd_atual):
                novo_nome = gerar_nome_completo()
                # Verifica se nome já existe para não duplicar pessoa
                if not any(r['name'] == novo_nome for r in all_reps):
                    insert_representative(novo_nome, dept_id)
                    print(f"   + Contratado: {novo_nome} para {dept_name}")

    # Atualiza lista
    all_reps = list_representatives()
    reps_reais = [r for r in all_reps if r['name'] != "SISTEMA DE ENTRADA"]

    # 3. PRODUTOS & TRANSAÇÕES
    print("📦 Processando Catálogo e Estoque...")
    
    for cat_nome, lista_prods in PRODUTOS_POR_CATEGORIA.items():
        cat_id = map_cat_ids.get(cat_nome)
        
        for p_name, p_desc, p_min in lista_prods:
            p_id = get_or_create_prod(p_name, cat_id, p_desc, p_min)
            
            # Pega produto atualizado
            prod_atual = next(p for p in list_products() if p['id'] == p_id)
            
            # Se estiver zerado, faz a mágica acontecer
            if prod_atual['stock'] == 0:
                # Estratégia: Entrada = Saída + Reserva
                reserva = random.randint(p_min + 2, p_min + 30)
                qtd_saidas_total = 0
                transacoes_saida = []

                # Define entre 5 e 20 saídas históricas
                num_movimentos = random.randint(5, 20)

                for _ in range(num_movimentos):
                    # Qtd varia pelo tipo
                    if "Notebook" in p_name or "Cadeira" in p_name:
                        q = 1
                    elif "Papel" in p_name or "Copo" in p_name:
                        q = random.randint(2, 10)
                    else:
                        q = random.randint(1, 5)
                    
                    transacoes_saida.append(q)
                    qtd_saidas_total += q
                
                entrada_inicial = qtd_saidas_total + reserva

                # 1. Entrada (90 dias atrás)
                register_transaction(
                    'IN', p_id, entrada_inicial, date.today() - timedelta(days=random.randint(80, 90)),
                    id_estoque_geral, id_rep_sistema, random.choice(mgr_ids), "Inventário Inicial"
                )

                # 2. Saídas (Espalhadas)
                for q in transacoes_saida:
                    rep = random.choice(reps_reais)
                    dias_atras = random.randint(1, 79)
                    try:
                        register_transaction(
                            'OUT', p_id, q, date.today() - timedelta(days=dias_atras),
                            rep['department_id'], rep['id'], random.choice(mgr_ids), f"Req. {rep['name']}"
                        )
                    except: pass
    
    print("✅ Carga Completa: 80+ Produtos, Nomes Reais e Estoque Positivo.")

if __name__ == "__main__":
    seed_data_v2()