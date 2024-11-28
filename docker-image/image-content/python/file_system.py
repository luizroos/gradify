import os
import shutil
import sys
from logger_config import setup_logger

logger = setup_logger()

def is_directory_exists(path):
    return os.path.isdir(path)

def copy_dir_content(src, dest):
    # Verifica se o diretório de origem existe
    if not is_directory_exists(src):
        logger.error(f"Diretório de origem '{src}' não existe!")
        return False
    
    # Verifica se o diretório de destino existe, cria se não existir
    if not is_directory_exists(dest):
        os.makedirs(dest)
    
    # Copia o conteúdo do diretório de origem para o diretório de destino
    try:
        # O `shutil.copytree` pode ser usado para copiar diretórios de maneira recursiva
        # mas ao invés de copiar o diretório todo, copiamos apenas os arquivos no diretório
        # e mantemos as permissões.
        for item in os.listdir(src):
            src_item = os.path.join(src, item)
            dest_item = os.path.join(dest, item)
            if is_directory_exists(src_item):
                shutil.copytree(src_item, dest_item)  # Copia subdiretórios recursivamente
            else:
                shutil.copy2(src_item, dest_item)  # Copia arquivos com metadados (permissões)
        return True
    except Exception as e:
        logger.error(f"Erro ao copiar conteúdo de '{src}' para '{dest}': {e}")
        return False


# para ser usado por sh script
def main():
    if len(sys.argv) < 3:
        logger.error("Uso: python3 run_method.py <method_name> <param1> [<param2> ... <paramN>]")
        sys.exit(1)

    method_name = sys.argv[1]
    params = sys.argv[2:]

    # Verifica se o método existe
    if method_name in globals():
        method = globals()[method_name]
        result = method(*params)
        if result:
            print(f"Execução do método {method_name} foi bem-sucedida.")
        else:
            print(f"Execução do método {method_name} falhou.")
    else:
        print(f"Método {method_name} não encontrado!")
        sys.exit(1)

if __name__ == "__main__":
    main()