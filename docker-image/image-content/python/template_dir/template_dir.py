import os
from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path
from file_system import get_sub_directories, copy_dir_content, load_yaml
from system import get_gradify_base_dir
from ui import ui_options, ui_question, print_info
from shell import execute_shell_commands
from logger_config import setup_logger
from template_render import gen_file_from_template2

logger = setup_logger()

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

    def apply(self) -> bool:
        template_path = f"{self.path}/{self.name}"
        template_data_path = f"{template_path}/data"
        if not os.path.isdir(template_data_path):
            logger.error(f"Template {self.name} configurado errado, faltando diretório data...")
            return False
        
        # faz todas as perguntas definidas em var-questions.yaml para o usuario
        var_questions_yaml = load_yaml(f"{template_path}/var-questions.yaml")
        env_vars = {}
        if var_questions_yaml is not None:
            for question_data in var_questions_yaml['questions']:
                var_name = question_data['varName']
                question = question_data['question']
                var_type = question_data['type']
                default_value = question_data.get('defaultValue', '')
                response = ui_question(question, var_type, str(default_value))
                env_vars[var_name] = response       
            # executa os comandos antes de aplicar o template
            execute_shell_commands(var_questions_yaml['preTemplateScript'], template_data_path, env_vars)

        # copia todos arquivos 
        copy_dir_content(template_data_path, self.dest_path)

        for template_file in Path(self.dest_path).rglob("*.j2"):
            if not template_file.is_file():
                continue
        
            dir_name = template_file.parent
            base_name = template_file.stem  # Nome do arquivo sem extensão .j2
            output_file = dir_name / base_name

            gen_file_from_template2(template_file, env_vars, output_file)
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
        
        options: List[str]
        
        if self.enable_no_template:
            # o usuário pode escolher não aplicar nenhum template, isso por si só já da uma opção para ele
            options = [NO_TEMPLATE_OPTION_LABEL] + template_options
        elif template_options_qty == 1:
            # só tem um template que pode ser aplicado
            return Template(
                dest_path=self.dest_path,
                path=self.templates_path,
                name=template_options[0]
            )
        
        selected_template = ui_options(f"Deseja aplicar algum template para {self.dest_path}?", options)
        if not selected_template or selected_template == NO_TEMPLATE_OPTION_LABEL:
            return None
        
        return Template(
            dest_path=self.dest_path,
            path=self.templates_path,
            name=selected_template
        )