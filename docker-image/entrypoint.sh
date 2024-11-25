#!/bin/bash

source $GPE_DIR/scripts/functions.sh

# valida que as variaveis foram preenchidas
if [[ -z "$JAVA_HOME" || -z "$HOST_USER_UID" || -z "$HOST_USER_GID" ]]; then
  echo "Error: Variáveis de ambiente devem ser informadas."
  exit 1
fi

# coloca o java do host no path (TODO ver se isso é uma coisa que vale a pena pensar em fazer, acho que não, e ai talvez mudar a imagem para alpine)
export PATH="$JAVA_HOME/bin:$PATH"

# garante que todos arquivos estejam setados com owner do host
set_host_owner "$GPE_DIR"

if [[ "$1" == "gradle-update" ]]; then
  $GPE_DIR/scripts/gradle-update.sh 
  exit 0
elif [[ "$1" == "create" ]]; then
  $GPE_DIR/scripts/project-create.sh "${@:2}" && $GPE_DIR/scripts/gradle-update.sh
  exit 0
elif [[ "$1" == "bash" ]]; then  
  bash
elif [[ "$1" == "completion" ]]; then
  cat $GPE_DIR/scripts/completion.sh
else
  echo "Comando desconhecido: $1"
  exit 1
fi