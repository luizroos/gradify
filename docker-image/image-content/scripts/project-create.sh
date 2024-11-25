#!/bin/bash
source $GPE_DIR/scripts/functions.sh

create_module_dir() {
  local module_dir="$1"
  local package_name="$2"
  
  directories=(
    "$module_dir"
    "$module_dir/src"
    "$module_dir/src/main"
    "$module_dir/src/main/java"
    "$module_dir/src/main/java/$package_name"
    "$module_dir/src/main/resources"
    "$module_dir/src/test"
    "$module_dir/src/test/java"
  )

  # Itera sobre cada diretório e cria se não existir
  for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
      mkdir -p "$dir"
      set_host_owner $dir
    fi
  done
}

configure_spring_boot_app() {
  local module_dir="$1"
  local package_name="$2"
  local class_name="$3"

  # cria a classe Main (provavelmente depois substituem ela)
  tpl_spring_boot_file="$GPE_DIR/templates/java/SpringBootApp.java.j2"
  prj_spring_boot_file="$module_dir/src/main/java/$package_name/$class_name.java"
  jinja2 "$tpl_spring_boot_file" -D packageName="$package_name" -D className="$class_name" -o "$prj_spring_boot_file"
  set_host_owner "$prj_spring_boot_file"
}

# Parametros validos: 'spring-app' ou 'empty'
if [[ "$1" != "spring-app" && "$1" != "empty" ]]; then
  echo "Erro: deve-se informar o tipo: 'spring-app' ou 'empty'."
  exit 1
fi

# arquivo de configuracao do sistema
config_file="$HOST_PROJECT_DIR/system-config.yaml"

# cria os modulos
project_name=$(yq '.project.name' "$config_file")
module_names=$(yq '.project.modules[].name' "$config_file")

for module_name in $module_names; do
  # diretorio que o modulo sera criado
  module_dir="$HOST_PROJECT_DIR/$module_name"
  # pacote que sera criado dentro do modulo
  package_name=$(sanitize_and_lowercase "$project_name")
  # tipo de modulo
  module_type=$(yq eval ".project.modules[] | select(.name == \"$module_name\").type" "$config_file")

  # cria o diretorio do modulo
  create_module_dir $module_dir $package_name

  if [[ "$1" == "spring-app" ]]; then
    if [[ "$module_type" == "app" ]]; then
      # nome da classe
      class_name=$(to_camel_case "$module_name")

      # configura o modulo para uma app spring boot
      configure_spring_boot_app $module_dir $package_name $class_name 
    fi

  fi
done

echo "Projeto criado"