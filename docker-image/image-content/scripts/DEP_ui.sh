#!/bin/bash
### SUBSTITUIDO POR ui.py

source $GRADIFY_DIR/scripts/type-formats.sh
source $GRADIFY_DIR/scripts/functions.sh

ui_options() {
  local question="$1"
  local options="$2"

  local option=$(echo "$options" | fzf --header="Selecione entre as opções" --prompt="$question ")
  
  echo $option
}

# Faz uma pergunta para o usuario
ui_question() {
  local question=$1
  local type=$2
  local default_value=$3
  local alert_msg=$4

  local response
  if [[ "$type" == "boolean" ]]; then
    response=$(
      printf "true\nfalse" |
      fzf --header="$alert_msg Selecione entre as opções" --prompt="$question " |
      awk '{printf "%s", $0}'
    ) 
  else
    response=$(
      echo "$default_value" |
      fzf --header="$alert_msg Responda" --prompt="$question " --print-query |
      awk '{printf "%s", $0}'
    )
  fi    

  local trim_response=$(echo "$response" | xargs)

  if ! validate_type "$trim_response" "$type"; then
    ui_question "$question" "$type" "$default_value" "Valor inválido! -" 
  else 
    echo $trim_response
  fi
}

#resposta=$(ui_question "Digite um número" "string" "a.b.c" "Erro: valor inválido.")
#echo "Resposta final: $resposta"