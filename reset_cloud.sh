#!/bin/bash

# ========================================================
# SCRIPT DE RESET BLINDADO (VERSÃO SEM URL DE CONEXÃO)
# ========================================================

# Configuração de segurança: Para o script se der erro em qualquer comando
set -e

# Caminhos Absolutos
PG_BIN="/usr/lib/postgresql/17/bin"
PROJ_DIR="/home/adryel/Armazenamento/Documentos/Projetos Pessoais/controle_estoque"

# Entra na pasta
cd "$PROJ_DIR"

echo "--- [$(date)] INICIO DA AUTOMACAO ---"

# 1. Carregamento seguro do .env
# Se o arquivo não existir, para tudo.
if [ ! -f .env ]; then
    echo "ERRO CRÍTICO: .env não encontrado em $PROJ_DIR"
    exit 1
fi

# Exporta as variáveis uma a uma (mais seguro que xargs para o Cron)
export NEON_HOST=$(grep ^NEON_HOST .env | cut -d '=' -f2- | tr -d '"' | tr -d "'")
export NEON_USER=$(grep ^NEON_USER .env | cut -d '=' -f2- | tr -d '"' | tr -d "'")
export NEON_PASS=$(grep ^NEON_PASS .env | cut -d '=' -f2- | tr -d '"' | tr -d "'")
export NEON_DB=$(grep ^NEON_DB .env | cut -d '=' -f2- | tr -d '"' | tr -d "'")

# Define a senha para AMBOS os comandos
export PGPASSWORD=$NEON_PASS

echo "--- [$(date)] 1. RESTAURANDO DADOS (PG_RESTORE) ---"

"$PG_BIN/pg_restore" \
    -h $NEON_HOST \
    -p 5432 \
    -U $NEON_USER \
    -d $NEON_DB \
    -n public \
    --clean \
    --if-exists \
    --no-owner \
    --no-privileges \
    -v \
    "backup_padrao.backup"

echo "--- [$(date)] 2. APLICANDO PERMISSOES (PSQL) ---"

# MUDANÇA AQUI: Usamos flags (-h, -U) igual ao pg_restore
# Isso evita erros de URL mal formatada no Cron
"$PG_BIN/psql" \
    -h $NEON_HOST \
    -p 5432 \
    -U $NEON_USER \
    -d $NEON_DB \
    -c "
    GRANT USAGE ON SCHEMA public TO neondb_owner;
    GRANT CREATE ON SCHEMA public TO neondb_owner;
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO neondb_owner;
    GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public TO neondb_owner;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO neondb_owner;
"

# Limpa a senha da memória
unset PGPASSWORD

echo "--- [$(date)] SUCESSO TOTAL ---"