import os
from dataclasses import dataclass, field
from typing import Dict, Union, Optional
from pathlib import Path
from file_system import get_sub_directories, copy_dir_content, load_yaml
from ui import ui_options, ui_question, print_error
from shell import execute_shell_commands
from template_render import gen_file_from_map, gen_file_from_loaded_template

NO_TEMPLATE_OPTION_LABEL = "Não"

# um template deve ter um diretorio chamado /data com os dados que serão copiados para o destino e opcionalmente um arquivo chamado
# var-questions.yaml com as perguntas de variaveis do template
# template-dir/
#    - data/
#    - var-questions.yaml
@dataclass
class Template:

    # diretorio onde deve aplicar o template
    dest_path: str

    # path do template
    path: str

    # nome do template
    name: str

    # aplica o template com parametros informados do carregamento de um arquivo yaml
    def apply_from_yaml_param_file(self, yaml_param_file: Union[dict, list]):
        template_path = f"{self.path}/{self.name}"
        template_data_path = f"{template_path}/data"
        if not os.path.isdir(template_data_path):
            print_error(f"Template {self.name} configurado errado, faltando diretório data...")
            return False
        
        # copia todos arquivos 
        copy_dir_content(template_data_path, self.dest_path)

        for template_file in Path(self.dest_path).rglob("*.j2"):
            if not template_file.is_file():
                continue
        
            dir_name = template_file.parent
            base_name = template_file.stem  # Nome do arquivo sem extensão .j2
            output_file = dir_name / base_name

            gen_file_from_loaded_template(template_file, output_file, yaml_param_file)
            template_file.unlink()
        return True        

    # aplica o template com os parametros perguntados no var-questions
    def apply_from_var_questions_param(self) -> bool:
        template_path = f"{self.path}/{self.name}"
        template_data_path = f"{template_path}/data"
        if not os.path.isdir(template_data_path):
            print_error(f"Template {self.name} configurado errado, faltando diretório data...")
            return False

        # copia todos arquivos 
        copy_dir_content(template_data_path, self.dest_path)
        
        # faz todas as perguntas definidas em var-questions.yaml para o usuario
        var_questions_yaml = load_yaml(f"{template_path}/var-questions.yaml")
        env_vars: Dict[str, str] = {}
        if var_questions_yaml is not None:
            for question_data in var_questions_yaml['questions']:
                var_name = question_data['varName']
                question = question_data['question']
                var_type = question_data['type']
                default_value = question_data.get('defaultValue', '')
                response = ui_question(question, var_type, str(default_value))
                env_vars[var_name] = response       
            # executa os comandos antes de aplicar o template.
            # o problema ta no working_directory, quando executa no primeiro, a gente move isso para outro diretorio, e ai da ruim 
            # para executar a segunda vez. Talvez precisa primeiro copiar para o destino e ai aplicar os comandos
            execute_shell_commands(var_questions_yaml['preTemplateScript'], self.dest_path, env_vars)

        for template_file in Path(self.dest_path).rglob("*.j2"):
            if not template_file.is_file():
                continue
        
            dir_name = template_file.parent
            base_name = template_file.stem  # Nome do arquivo sem extensão .j2
            output_file = dir_name / base_name

            gen_file_from_map(template_file, output_file, env_vars)
            template_file.unlink()

        return True


@dataclass
class TemplateDir:
    
    # diretorio base onde o template sera aplicado
    dest_path: str

    # diretorio onde existem os templates
    templates_path: str

    # indica se existe a opção do usuário escolher não aplicar nenhum template
    enable_no_template: bool = True

    def select_template(self) -> Optional[Template]:         
        # pergunta para o usuario se ele quer aplicar algum template
        template_options = get_sub_directories(self.templates_path)
        template_options_qty = len(template_options)
        if template_options_qty == 0:
            # sem template para aplicar
            return None
        
        selected_template: str
        if self.enable_no_template:
            # o usuário pode escolher não aplicar nenhum template, isso por si só já da uma a mais para ele
            options = [NO_TEMPLATE_OPTION_LABEL] + template_options
            selected_template = ui_options(f"Deseja aplicar algum template para {self.dest_path}?", options)
        elif template_options_qty == 1:
            # só tem um template que pode ser aplicado
            selected_template = template_options[0]
        else:
            selected_template = ui_options(f"Qual template deseja aplicar para {self.dest_path}?", template_options)
        
        if not selected_template or selected_template == NO_TEMPLATE_OPTION_LABEL:
            return None
        
        return Template(
            dest_path=self.dest_path,
            path=self.templates_path,
            name=selected_template
        )