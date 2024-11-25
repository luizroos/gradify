#!/bin/bash
source $GPE_DIR/scripts/functions.sh

echo "Atualizando arquivos do gradle..."

# Arquivos de templating
tpl_build_gradle_file="$GPE_DIR/templates/gradle/build.gradle.j2"
tpl_settings_gradle_file="$GPE_DIR/templates/gradle/settings.gradle.j2"

# arqivo de configuracao do sistema
config_file="$HOST_PROJECT_DIR/system-config.yaml"

# arquivos de configuracao do projeto (serão gerados)
prj_build_gradle_file="$HOST_PROJECT_DIR/build.gradle"
prj_settings_gradle_file="$HOST_PROJECT_DIR/settings.gradle"

# gera o arquivo build.gradle
gen_file_from_template $tpl_build_gradle_file $config_file $prj_build_gradle_file

# gera o arquivo settings.gradle
gen_file_from_template $tpl_settings_gradle_file $config_file $prj_settings_gradle_file

# copia o gradle para dentro do diretorio do projeto
copy_dir_content "$GPE_DIR/gradle-8.11.1" $HOST_PROJECT_DIR

echo "Arquivos do gradle atualizados!"