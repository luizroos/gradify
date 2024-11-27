#!/bin/bash
source $GRADIFY_DIR/scripts/functions.sh
source $GRADIFY_DIR/scripts/code-template.sh

# funções #

# resolve o diretorio do modulo, use como local module_path=$(module_path 'abc')
module_path() {
    local module_name="$1"
    echo "$PRJ_HOST_DIR/$module_name"
}

# cria o diretorio de um modulo
create_module_dir() {
  local module_path="$1"

  # Verifica se o diretório existe
  if [ -d "$module_path" ]; then
    return 1;
  fi

  log_info "creating module $module_path directory..."

  directories=(
    "$module_path"
    "$module_path/src"
    "$module_path/src/main"
    "$module_path/src/main/java"
    "$module_path/src/main/resources"
    "$module_path/src/test"
    "$module_path/src/test/java"
  )

  # Itera sobre cada diretório e cria se não existir
  for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
      mkdir -p "$dir"
      set_host_owner $dir
    fi
  done
  return 0
}

# cria todos os modulos informados no arquivo de configuração
create_project_modules() {
  local module_names=$(yq '.project.modules[].name' "$PRJ_CONFIG_FILE")
  mapfile -t modules_names_arr <<< "$module_names"
  for module_name in "${modules_names_arr[@]}"; do
    
    local module_path=$(module_path $module_name)

    # cria o módulo, se não for possivel criar é pq ele já existe e não vamos mexe-lo
    if ! create_module_dir $module_name; then
      continue;
    fi
    
    # aplica o code template
    apply_code_template $module_path 'gradle'
    
    # garante que todos diretórios e arquivos estão com owner certo
    set_host_owner $module_path
  done
}

# atualiza os arquivos com base no template informado
update_project_file() {
  local template_file="$1"  
  local dest_file="$2"

  log_info "Updating $dest_file..."
  local template_file_path="$GRADIFY_DIR/gradle/v1/templates/$template_file"
  local dest_file_path="$PRJ_HOST_DIR/$dest_file"
  gen_file_from_template $template_file_path $PRJ_CONFIG_FILE $dest_file_path
}

# main #

log_info "Updating project..."

# arquivo de configuracao do sistema
PRJ_CONFIG_FILE="$PRJ_HOST_DIR/$PRJ_CONFIG_FILENAME"

create_project_modules

# copia/atualiza o gradle de referencia para dentro do diretorio do projeto
copy_dir_content "$GRADIFY_DIR/gradle/v1/gradle-8.11.1" $PRJ_HOST_DIR

# atualiza os arquivos do gradle
update_project_file "build.gradle.j2" "build.gradle"
update_project_file "settings.gradle.j2" "settings.gradle"
update_project_file "libs.versions.toml.j2" "gradle/libs.versions.toml"

log_info "Project files updated!"

