#!/bin/bash

# Função para converter a string para lowercase
sanitize_and_lowercase() {
  local input=$1
  echo "$input" | tr -cd '[:alnum:]' | tr '[:upper:]' '[:lower:]'
}

# Função para converter a string para CamelCase
to_camel_case() {
  local input=$1
  echo "$input" | sed -e 's/[^a-zA-Z0-9]/ /g' -e 's/\b\(.\)/\U\1/g' | tr -d ' ' | sed 's/\b\(.\)/\U\1/'
}

# Monitora um arquivo e executa um script toda vez que o arquivo alterar
register_file_change_listener() {
  local file=$1
  local execScript=$2

  echo "Monitoring changes on $file..."
  while inotifywait -e modify "$file"; do
    bash $execScript
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

  # garante que o owner do arquivo é o usuário do host
  set_host_owner $destFile
}

# Elimina as linhas em branco do arquivo
strip_empty_lines() {
  local file="$1"
  sed -i '/^\s*$/d' $file
}

# Função para definir o dono do arquivo como o usuário do host
set_host_owner() {
  local fileOrDir="$1"
  chown -R $HOST_USER_UID:$HOST_USER_GID "$fileOrDir"
}

# Função para copiar um diretório
copy_dir_content() {
  local src="$1"
  local dest="$2"

  if [ ! -d "$src" ]; then
    echo "Erro: Diretório de origem '$src' não existe!"
    return 1
  fi

  if [ ! -d "$dest" ]; then
    mkdir -p "$dest"
  fi

  # -a preseva permissões
  cp -ra "$src"/* "$dest"

  return 0
}