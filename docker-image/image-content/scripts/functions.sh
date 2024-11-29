#!/bin/bash

# funcoes de log
log_debug() {
    log "DEBUG" "$1"
}

log_info() {
    log "INFO" "$1"
}

log_warn() {
    log "WARN" "$1"
}

log_error() {
    log "ERROR" "$1"
}

log() {
    local level="$1"
    local message="$2"
    echo "$(date +"%Y-%m-%d %H:%M:%S.%3N") [$level] $message"
}

# Função para converter a string para lowercase
sanitize_and_lowercase() {
  local input=$1
  echo "$input" | tr -cd '[:alnum:]' | tr '[:upper:]' '[:lower:]'
}

# Função para converter a string para CamelCase
depre_to_camel_case() {
  local input=$1
  echo "$input" | sed -e 's/[^a-zA-Z0-9]/ /g' -e 's/\b\(.\)/\U\1/g' | tr -d ' ' | sed 's/\b\(.\)/\U\1/'
}

# Monitora um arquivo e executa um script toda vez que o arquivo alterar
register_file_change_listener() {
  local file=$1
  local execScript=$2

  log_debug "Monitoring changes on $file..."
  while inotifywait -e modify,move_self "$file"; do
    bash -c $execScript
  done
}

# gera o arquivo build.gradle do sistema
gen_file_from_template() {
  local templateFile="$1"
  local paramFile="$2"
  local destFile="$3"

  # faz o parser do template e gera o arquivo destino
  jinja2 $templateFile $paramFile -o $destFile

  # remove linhas em branco
  strip_empty_lines $destFile
}

# Elimina as linhas em branco do arquivo
strip_empty_lines() {
  local file="$1"
  sed -i '/^\s*$/d' $file
}
