#!/bin/bash

#Por convenção, todo code template deve ter um diretorio data, que são os arquivos que serão copiados, e opcionalmente um arquivo var-questions.yaml, onde deve-se especificar as perguntas e o nome das variaveis que o template usa. 
#No momento do update, sera feito essas perguntas para o usuario e repassado as variaveis para o parser do template

source $GRADIFY_DIR/scripts/functions.sh
source $GRADIFY_DIR/scripts/ui.sh

# pergunta e aplica um template ao módulo
apply_code_template() {
  # nome do "modulo", o que pode ser qualquer diretorio especifico
  local module_path="$1"
  # ferramenta que esta sendo usada
  local tool=$2
  # valor padrao para não querer nenhum template
  local no_opt_label="Nenhum"
  # diretorio base dos code templates da tool
  local tool_code_template_base_dir="$GRADIFY_DIR/$tool/code-templates"

  # pergunta se quer aplicar algum template, basicamente listando os templates que existem
  options=$(
    {
      echo "$no_opt_label"
      find "$tool_code_template_base_dir"/* -maxdepth 0 -type d -printf "%f\n"
    } | paste -sd ',' -
  )
  temp_file=$(mktemp)
  python3 $GRADIFY_DIR/python/ui.py "ui_options" "$temp_file" "Deseja aplicar algum template para $module_path?" "$options"
  selected_template=$(cat "$temp_file")
  rm "$temp_file"  
  #local options=$({
  #  echo "$no_opt_label"
  #  find "$tool_code_template_base_dir"/* -maxdepth 0 -type d -printf "%f\n"
  #}) 
  #local selected_template=$(ui_options "Deseja aplicar algum template para $module_path?" "$options")   

  # por convencao, os code templates devem ter um diretorio "data" dentro deles
  local code_template_dir="$tool_code_template_base_dir/$selected_template"
  local code_template_data_dir="$code_template_dir/data"
  if [ -z "$selected_template" ] || [ "$selected_template" == $no_opt_label ] || [ ! -d "$code_template_data_dir" ]; then
      return;
  fi

  # gera um arquivo temporario para guardar o yaml das variaveis do template
  local temp_yaml_template_file="$(mktemp).yaml"
  if [ -f "$code_template_dir/var-questions.yaml" ]; then 
    log_debug "parsing var questions..."
    parse_code_template_vars "$code_template_dir/var-questions.yaml" $temp_yaml_template_file $code_template_data_dir
  else
    touch $temp_yaml_template_file
  fi
  
  # copia os arquivos do template
  log_info "applying code template $selected_template to $module_path..."
  copy_dir_content "$code_template_data_dir" "$module_path/"

  # para cada arquivo, aplica o template
  for template_file in $(find "$module_path/" -type f -name "*.j2"); do
    if [ ! -f "$template_file" ]; then
      continue;
    fi
    local dir_name=$(dirname "$template_file")
    local base_name=$(basename "$template_file" .j2)

    # gera o template
    log_debug "parsing template $template_file to $dir_name/$base_name"...
    gen_file_from_template $template_file $temp_yaml_template_file "$dir_name/$base_name"

    rm $template_file
  done  

  # remove o arquivo temporario
  rm "$temp_yaml_template_file"
}

# faz o parser de um var-questions.yaml, faz as perguntas e gera um arquivo de saida com o valor das variaveis 
parse_code_template_vars() {
    # arquivo onde estão as configurações das perguntas e variaveis
    local var_questions_file=$1
    # arquivo de saida, onde será gravado as variáveis
    local output_vars_file=$2
    # diretorio onde será executado os comandos de pre template script
    local base_dir=$3

    log_debug="var_questions_file=$var_questions_file, output_vars_file=$output_vars_file, base_dir=$base_dir"
    local var_names=$(yq '.questions[].varName' "$var_questions_file")
    mapfile -t var_names_arr <<< "$var_names"
    for var_name in "${var_names_arr[@]}"; do
        local question=$(yq eval ".questions[] | select(.varName == \"$var_name\") | .question" "$var_questions_file")
        local type=$(yq eval ".questions[] | select(.varName == \"$var_name\") | .type" "$var_questions_file")
        local default_value=$(yq eval ".questions[] | select(.varName == \"$var_name\") | .defaultValue" "$var_questions_file")

        ######
        temp_file=$(mktemp)
        python3 $GRADIFY_DIR/python/ui.py "ui_question" "$temp_file" "$question" "$type" "$default_value" 
        response=$(cat "$temp_file")
        rm "$temp_file"
        ##### local response=$(ui_question "$question" "$type" "$default_value")

        # grava a variavel no arquivo de parametro
        echo "$var_name: $response" >> "$output_vars_file"

        # seta a variavel para execução depois aplicar o preTemplateScript
        eval "$var_name=\"$response\""
    done

    
    # executa os comandos do var questions
    readarray -t preTemplateScript < <(yq '.preTemplateScript[]' "$var_questions_file")
    for script in "${preTemplateScript[@]}"; do
        cd $base_dir
        log_debug "applying pre template script: $script"
        eval "$script" || { log_error "Error applying: $script"; exit 1; }
        cd -
    done
}