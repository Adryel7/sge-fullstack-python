#!/bin/bash

# ========================================================
# SCRIPT DE RESET BLINDADO (RESTAURAÇÃO + PERMISSÕES)
# ========================================================

PROJ_DIR="$HOME/Projetos/sge-analytics-v2"
cd "$PROJ_DIR"

# 1. Carrega variáveis do .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "Erro: Arquivo .env não encontrado."
    exit 1
fi

echo "--- [$(date)] 1. INICIANDO RESTAURAÇÃO ---"

export PGPASSWORD=$NEON_PASS

# 2. Restaura os dados (Forçando Schema Public)
/usr/lib/postgresql/17/bin/pg_restore \
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

echo "--- [$(date)] 2. CORRIGINDO PERMISSÕES (FIX) ---"

# 3. O PULO DO GATO: Comandos SQL para garantir acesso total
# Isso garante que o usuário do App consiga ler as tabelas recém-criadas
psql "postgres://$NEON_USER:$NEON_PASS@$NEON_HOST/$NEON_DB?sslmode=require" -c "
    GRANT USAGE ON SCHEMA public TO neondb_owner;
    GRANT CREATE ON SCHEMA public TO neondb_owner;
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO neondb_owner;
    GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public TO neondb_owner;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO neondb_owner;
"

unset PGPASSWORD
echo "--- [$(date)] PROCESSO FINALIZADO ---"