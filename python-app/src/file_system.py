import os
import shutil
import sys
import yaml
from typing import Union, List
from logger_config import setup_logger
from utils.deprecated import deprecated

logger = setup_logger()

# Carrega um arquivo yaml
def load_yaml(path: str) -> Union[dict, list]: 
    if not os.path.isfile(path):
        return None
    with open(path, 'r') as file:
        return yaml.safe_load(file)       

# retorna um array com o nome dos sub diretorios de um diretorio
def get_sub_directories(base_dir: str) -> List[str]:
    sub_directories = []
    try:
        for entry in os.scandir(base_dir):
            if entry.is_dir():
                sub_directories.append(entry.name)
        return sub_directories
    except FileNotFoundError as e:
        logger.error(f"{base_dir} nao encontrado.")
        raise e        

# verifica se um diretorio existe
@deprecated
def is_directory_exists(path: str):
    return os.path.isdir(path)

# copia o conteudo de um diretio para outro
def copy_dir_content(src, dest):
    # Verifica se o diretório de origem existe
    if not os.path.isdir(src):
        logger.error(f"Diretório de origem '{src}' não existe!")
        return False
    
    # Verifica se o diretório de destino existe, cria se não existir
    if not os.path.isdir(dest):
        os.makedirs(dest)
    
    # Copia o conteúdo do diretório de origem para o diretório de destino
    try:
        # O `shutil.copytree` pode ser usado para copiar diretórios de maneira recursiva
        # mas ao invés de copiar o diretório todo, copiamos apenas os arquivos no diretório
        # e mantemos as permissões.
        for item in os.listdir(src):
            src_item = os.path.join(src, item)
            dest_item = os.path.join(dest, item)
            if os.path.isdir(src_item):
                shutil.copytree(src_item, dest_item, dirs_exist_ok=True)  # Copia subdiretórios recursivamente
            else:
                shutil.copy2(src_item, dest_item)  # Copia arquivos com metadados (permissões)
            st = os.stat(src_item)
        return True
    except Exception as e:
        logger.error(f"Erro ao copiar conteúdo de '{src}' para '{dest}': {e}")
        raise e

# para ser usado por sh script
if __name__ == "__main__":
    method = sys.argv[1]
    if method == 'copy_dir_content':
        src = sys.argv[2]
        dest = sys.argv[3]
        copy_dir_content(src, dest)