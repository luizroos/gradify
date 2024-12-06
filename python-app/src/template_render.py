import os
import yaml
from typing import Union, Dict
from jinja2 import Environment, FileSystemLoader

# gera arquivo a partir de um template com parametros vindo de um map
def gen_file_from_map(template_path, output_path: str, params: Dict[str, str]):
    env = Environment(loader=FileSystemLoader(template_path.parent))
    template = env.get_template(template_path.name)
    with open(output_path, 'w') as f:
        f.write(template.render(params))
    strip_empty_lines(output_path)

# gera template com base num arquivo yaml ja carregado
def gen_file_from_loaded_template(template_path: str, output_path: str, yaml_param_file: Union[dict, list]):
    # Carregar o ambiente Jinja2 e o template
    env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
    template = env.get_template(os.path.basename(template_path))

    # Renderiza o template com os parâmetros e escreve no arquivo de destino
    with open(output_path, 'w') as f:
        f.write(template.render(yaml_param_file))

    # Remove linhas em branco no arquivo de destino
    strip_empty_lines(output_path)

# gera template com base num arquivo yaml 
def DEP_gen_file_from_template(template_path: str, output_path: str, yaml_param_file: str):
    with open(yaml_param_file, 'r') as f:
        params = yaml.safe_load(f)
    gen_file_from_loaded_template(template_path, output_path, params)

# apaga as linhas em branco do arquivo
def strip_empty_lines(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Filtra as linhas não vazias
    non_empty_lines = [line for line in lines if line.strip()]

    # Escreve as linhas não vazias de volta no arquivo
    with open(file_path, 'w') as f:
        f.writelines(non_empty_lines)
