#!/bin/bash

# ========================================================
# SCRIPT DE RESET ULTRA-CONFIÁVEL (LOCAL -> NUVEM)
# ========================================================

PROJ_DIR="$HOME/Armazenamento/Documentos/Projetos Pessoais/controle_estoque"
cd "$PROJ_DIR"

# 1. Carrega variáveis
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "Erro: Arquivo .env não encontrado."
    exit 1
fi

echo "--- [$(date)] INICIANDO RESET NO NEON ---"

# 2. Define senha para automação
export PGPASSWORD=$NEON_PASS

# 3. PG_RESTORE COM FLAGS DE SEGURANÇA
# -n public: Garante que caia no schema certo
# --no-owner: Remove vínculos com seu usuário local 'adryel'
# --no-privileges: Ignora permissões de sistema do seu PC
# --clean: Apaga as tabelas antes de restaurar
# --if-exists: Evita erro se a tabela ainda não existir no Neon

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

# 4. Limpeza de rastro de senha
unset PGPASSWORD

echo "--- [$(date)] RESET CONCLUÍDO COM SUCESSO ---"