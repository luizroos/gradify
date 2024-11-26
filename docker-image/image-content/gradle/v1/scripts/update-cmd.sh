#!/bin/bash
source $GRADIFY_DIR/scripts/functions.sh

echo "Updating gradle files..."

# copia o gradle para dentro do diretorio do projeto
copy_dir_content "$GRADIFY_DIR/gradle/v1/gradle-8.11.1" $PRJ_HOST_DIR

# arqivo de configuracao do sistema
PRJ_CONFIG_FILE="$PRJ_HOST_DIR/$PRJ_CONFIG_FILENAME"

# Arquivo build.gradle
echo "Updating build.gradle..."
TPL_BUILD_GRADLE_FILE="$GRADIFY_DIR/gradle/v1/templates/build.gradle.j2"
PRJ_BUILD_GRADLE_FILE="$PRJ_HOST_DIR/build.gradle"
gen_file_from_template $TPL_BUILD_GRADLE_FILE $PRJ_CONFIG_FILE $PRJ_BUILD_GRADLE_FILE

# Arquivo settings.gradle
echo "Updating settings.gradle..."
TPL_SETTINGS_GRADLE_FILE="$GRADIFY_DIR/gradle/v1/templates/settings.gradle.j2"
PRJ_SETTINGS_GRADLE_FILE="$PRJ_HOST_DIR/settings.gradle"
gen_file_from_template $TPL_SETTINGS_GRADLE_FILE $PRJ_CONFIG_FILE $PRJ_SETTINGS_GRADLE_FILE

# Arquivo libs.versions.toml
echo "Updating libs.versions.toml..."
TPL_LIBS_VERS_TOML_FILE="$GRADIFY_DIR/gradle/v1/templates/libs.versions.toml.j2"
PRJ_LIBS_VERS_TOML_FILE="$PRJ_HOST_DIR/gradle/libs.versions.toml"
gen_file_from_template $TPL_LIBS_VERS_TOML_FILE $PRJ_CONFIG_FILE $PRJ_LIBS_VERS_TOML_FILE

echo "Gradle files updated!"