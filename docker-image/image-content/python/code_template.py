import yaml
from pathlib import Path
from file_system import get_sub_directories, is_directory_exists, copy_dir_content, load_yaml
from system import get_gradify_base_dir
from ui import ui_options, ui_question, print_info
from shell import execute_shell_commands
from logger_config import setup_logger
from template_render import gen_file_from_template2

logger = setup_logger()

class CodeTemplate:
    def __init__(self, prj_module_path, tool_name):
        self.prj_module_path = prj_module_path 
        self.tool_name = tool_name

    def apply(self): 
        gradify_base_dir = get_gradify_base_dir()

        # diretorio onde estao os templates da ferramenta
        tool_code_template_base_dir = f"{gradify_base_dir}/{self.tool_name}/code-templates"
        
        # pergunta para o usuario se ele quer aplicar algum template
        no_opt_label = "Não"
        options = [no_opt_label] + (get_sub_directories(tool_code_template_base_dir))
        selected_template = ui_options(f"Deseja aplicar algum template para {self.prj_module_path}?", options)
        if not selected_template or selected_template == no_opt_label:
            print_info(f"Não será aplicado nenhum template para {self.prj_module_path}...")
            return

        code_template_dir = f"{tool_code_template_base_dir}/{selected_template}"
        code_template_data_dir = f"{code_template_dir}/data"
        if not is_directory_exists(code_template_data_dir):
            logger.error(f"Template {selected_template} configurado errado, faltando diretório data...")
            return
        
        # faz todas as perguntas definidas em var-questions.yaml para o usuario
        var_questions_yaml = load_yaml(f"{code_template_dir}/var-questions.yaml")
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
            execute_shell_commands(var_questions_yaml['preTemplateScript'], code_template_data_dir, env_vars)

        # copia todos arquivos 
        copy_dir_content(code_template_data_dir,  self.prj_module_path)

        for template_file in Path(self.prj_module_path).rglob("*.j2"):
            if not template_file.is_file():
                continue
        
            dir_name = template_file.parent
            base_name = template_file.stem  # Nome do arquivo sem extensão .j2
            output_file = dir_name / base_name

            gen_file_from_template2(template_file, env_vars, output_file)
            template_file.unlink()
