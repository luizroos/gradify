#!/bin/bash
source $GRADIFY_DIR/scripts/functions.sh

# gradifyctl bash
if [[ "$1" == "bash" ]]; then  
  bash
  exit 0
fi

# gradifyctl version
if [[ "$1" == "version" ]]; then  
  echo "version: $GRADIFY_VERSION"
  echo "build date: $BUILD_DATE"
  exit 0
fi

# gradifyctl completion
if [[ "$1" == "completion" ]]; then
  cat $GRADIFY_DIR/scripts/completion.sh
  exit 0  
fi

# gradifyctl {tool*}

TOOL_TYPE=$1
TOOL_COMMAND=$2
COMMAND_PARAM1=$3

if [ ! -d "$GRADIFY_DIR/$TOOL_TYPE" ]; then
  log_error "the $TOOL_TYPE is not supported."
  exit 1  
fi


# gradifyctl {tool*} project-config *
if [[ "$TOOL_COMMAND" == "project-config" ]]; then  
  if [ -z "$COMMAND_PARAM1" ] || [ ! -d "$GRADIFY_DIR/$TOOL_TYPE/$COMMAND_PARAM1" ]; then
    log_error "invalid $COMMAND_PARAM1 option."
    exit 1  
  fi
  cat $GRADIFY_DIR/$TOOL_TYPE/$COMMAND_PARAM1/demo-project-config.yaml
  exit 0
fi

# checa se o arquivo de configuracao do projeto existe
if [ ! -f $PRJ_CONFIG_FILENAME ]; then
    log_error "missing project config file."
    exit 1
fi

# TODO pegar do arquivo
VERSION=v1
UPDATE_SCRIPT=$GRADIFY_DIR/$TOOL_TYPE/$VERSION/scripts/update-cmd.sh

if [ ! -d "$GRADIFY_DIR/$TOOL_TYPE/$VERSION" ]; then
  log_error "the $TOOL_TYPE tool does not support version $VERSION."
  exit 1  
fi

# gradifyctl {tool*} update *
if [[ "$TOOL_COMMAND" == "update" ]]; then
  python3 -m gradle.gradle_project "$PRJ_HOST_DIR" "$PRJ_CONFIG_FILENAME"
  if [[ "$COMMAND_PARAM1" == "keep-alive" ]]; then
    while inotifywait -e modify,move_self "$PRJ_HOST_DIR/$PRJ_CONFIG_FILENAME" 2>/dev/null; do
      python3 -m gradle.gradle_project "$PRJ_HOST_DIR" "$PRJ_CONFIG_FILENAME"
    done
  fi
  exit 0
fi

log_error "invalid tool command: $TOOL_COMMAND"
exit 1




