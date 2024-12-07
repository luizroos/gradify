#!/bin/bash

# gradifyctl bash
if [[ "$1" == "bash" ]]; then  
  bash
  exit 0
fi

# gradifyctl version
if [[ "$1" == "version" ]]; then  
  python -m ui print_info "version: $GRADIFY_VERSION"
  python -m ui print_info "build date: $BUILD_DATE"
  exit 0
fi

# gradifyctl completion
if [[ "$1" == "completion" ]]; then
  cat $GRADIFY_SHELL_SCRIPTS_DIR/completion.sh
  exit 0  
fi

# gradifyctl {tool*}

TOOL_NAME=$1
TOOL_COMMAND=$2
COMMAND_PARAM1=$3

if [ ! -d "$GRADIFY_TOOLS_DIR/$TOOL_NAME" ]; then
  python -m ui print_error "Não sei o que fazer com $TOOL_NAME"
  exit 1  
fi


# gradifyctl {tool*} project-config *
if [[ "$TOOL_COMMAND" == "project-config" ]]; then  
  if [ -z "$COMMAND_PARAM1" ] || [ ! -d "$GRADIFY_TOOLS_DIR/$TOOL_NAME/$COMMAND_PARAM1" ]; then
    python -m ui print_error "$COMMAND_PARAM1 não reconheço como uma versão válida para o $TOOL_COMMAND de $TOOL_NAME"
    exit 1  
  fi
  cat $GRADIFY_TOOLS_DIR/$TOOL_NAME/$COMMAND_PARAM1/demo-project-config.yaml
  exit 0
fi

# checa se o arquivo de configuracao do projeto existe
if [ ! -f $PRJ_CONFIG_FILENAME ]; then
    python -m ui print_error "Eu não encontrei $PRJ_CONFIG_FILENAME no seu diretório, tente gerar um usando a project-config."
    exit 1
fi

# gradifyctl {tool*} update *
if [[ "$TOOL_COMMAND" == "update" ]]; then
  python3 -m gradle.gradle_project "$PRJ_HOST_DIR" "$PRJ_CONFIG_FILENAME" "$GRADIFY_TOOLS_DIR"
  if [ $? -ne 0 ]; then
    exit 0
  fi
  if [[ "$COMMAND_PARAM1" == "keep-alive" ]]; then
    while inotifywait -e modify,move_self "$PRJ_HOST_DIR/$PRJ_CONFIG_FILENAME" 2>/dev/null; do
      python3 -m gradle.gradle_project "$PRJ_HOST_DIR" "$PRJ_CONFIG_FILENAME" "$GRADIFY_TOOLS_DIR"
      if [ $? -ne 0 ]; then
        exit 0
      fi      
    done
  fi
  exit 0
fi

python -m ui print_error "Não reconheci o comando $TOOL_COMMAND para $TOOL_NAME"
exit 1




