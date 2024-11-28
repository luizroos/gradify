#!/bin/bash

# Caminho para o diretório de origem e destino
SRC_DIR="$1"
DEST_DIR="$2"

# Chama o script Python passando o nome do método 'copy_dir_content' e os parâmetros
python3 file_system.py copy_dir_content "$SRC_DIR" "$DEST_DIR"