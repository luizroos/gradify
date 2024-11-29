import os
import yaml
from jinja2 import Environment, FileSystemLoader

# melhorar isso, tem que entender os tipos e acertar
def gen_file_from_template2(template_path, params, output_path: str):
    env = Environment(loader=FileSystemLoader(template_path.parent))
    template = env.get_template(template_path.name)
    with open(output_path, 'w') as f:
        f.write(template.render(params))
    strip_empty_lines(output_path)

def gen_file_from_loaded_template(template_path: str, output_path: str, yaml_param_file: any):
    # Carregar o ambiente Jinja2 e o template
    env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
    template = env.get_template(os.path.basename(template_path))

    # Renderiza o template com os parâmetros e escreve no arquivo de destino
    with open(output_path, 'w') as f:
        f.write(template.render(yaml_param_file))

    # Remove linhas em branco no arquivo de destino
    strip_empty_lines(output_path)

def gen_file_from_template(template_path: str, output_path: str, yaml_param_file: str):
    with open(yaml_param_file, 'r') as f:
        params = yaml.safe_load(f)
    gen_file_from_loaded_template(template_path, output_path, params)

def strip_empty_lines(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Filtra as linhas não vazias
    non_empty_lines = [line for line in lines if line.strip()]

    # Escreve as linhas não vazias de volta no arquivo
    with open(file_path, 'w') as f:
        f.writelines(non_empty_lines)


# Exemplo de uso
#gen_file_from_template('template.jinja2', 'params.json', 'output.gradle')
