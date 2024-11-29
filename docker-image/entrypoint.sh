#!/bin/bash
source $GRADIFY_DIR/scripts/functions.sh

# valida que as variaveis foram preenchidas
if [[ -z "$HOST_USER_UID" || -z "$HOST_USER_GID" ]]; then
  log_error "missing required env vars."
  exit 1
fi

echo "UID_MIN 1000" > /etc/login.defs
echo "UID_MAX 268511072" >> /etc/login.defs

# Cria um grupo com GID fornecido
groupadd -g "$HOST_USER_GID" hostgroup || log_warn "Grupo já existe"

# Cria o usuário com UID fornecido e adiciona ao grupo
useradd -u "$HOST_USER_UID" -g "$HOST_USER_GID" -m hostuser || log_warn "Usuário já existe"

# Ajusta permissões dos diretórios compartilhados
chown -R "$HOST_USER_UID":"$HOST_USER_GID" "$GRADIFY_DIR"
chown -R "$HOST_USER_UID":"$HOST_USER_GID" "/tmp"

# Executa o main com o usuário criado
exec gosu hostuser $GRADIFY_DIR/scripts/main.sh "$@"