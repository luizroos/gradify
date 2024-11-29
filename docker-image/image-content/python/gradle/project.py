import os
import sys
import yaml
from code_template import CodeTemplate
from file_system import is_directory_exists, create_directories, copy_dir_content
from ui import print_info, print_warn
from logger_config import setup_logger
from system import get_gradify_base_dir, get_project_config_filename
from template_render import gen_file_from_loaded_template

logger = setup_logger()
TOOL_NAME="gradle"

class GradleProject:
    def __init__(self, project_dir: str, prj_config_filename: str):
        prj_config_filename = get_project_config_filename()
        self.project_dir = project_dir
        with open(f"{project_dir}/{prj_config_filename}", 'r') as file:
            self.prj_config_yaml = yaml.safe_load(file)        

    # copia/atualiza os arquivos de configuracao do gradle para dentro do projeto
    def copy_gradle_files(self):
        print_info("Atualizando arquivos do gradle...")
        gradify_base_dir = get_gradify_base_dir()
        config_version = self.prj_config_yaml['configVersion']
        copy_dir_content(f"{gradify_base_dir}/{TOOL_NAME}/{config_version}/gradle-8.11.1", self.project_dir)  
        self._update_gradle_file(gradify_base_dir, config_version, "build.gradle.j2", "build.gradle")
        self._update_gradle_file(gradify_base_dir, config_version, "settings.gradle.j2", "settings.gradle")
        self._update_gradle_file(gradify_base_dir, config_version, "libs.versions.toml.j2", "gradle/libs.versions.toml")

    def _update_gradle_file(self, gradify_base_dir: str, config_version: str, template_file: str, dest_file: str):
        template_file_path=f"{gradify_base_dir}/{TOOL_NAME}/{config_version}/templates/{template_file}"
        dest_file_path=f"{self.project_dir}/{dest_file}"
        gen_file_from_loaded_template(template_file_path, dest_file_path, self.prj_config_yaml)

    # cria todos modulos do projeto gradle
    def create_modules(self):
        module_names = [module['name'] for module in self.prj_config_yaml['project']['modules']]
        for module_name in module_names:
            module_path = f"{self.project_dir}/{module_name}"
            # cria todos diretorios do modulo
            if not self.create_module_directories(module_name, module_path):
                continue
            # aplica um code template
            code_template = CodeTemplate(module_path, TOOL_NAME)
            code_template.apply()

    # cria todos diretorios de um modulo de um projeto gradle
    def create_module_directories(self, module_name, module_path):
        if is_directory_exists(module_path):
            print_warn(f"Diretório do módulo {module_name} já existente...")
            return False
        
        print_info(f"Criando módulo {module_name}...")

        # Lista de diretórios a serem criados
        directories = [
            module_path,
            os.path.join(module_path, "src"),
            os.path.join(module_path, "src", "main"),
            os.path.join(module_path, "src", "main", "java"),
            os.path.join(module_path, "src", "main", "resources"),
            os.path.join(module_path, "src", "test"),
            os.path.join(module_path, "src", "test", "java"),
        ]

        create_directories(directories)
        return True        
    

if __name__ == "__main__":
    project_dir = sys.argv[1]
    prj_config_filename = sys.argv[1]
    
    print_info("Atualizando projeto...")
    gradleProject = GradleProject(project_dir, prj_config_filename)
    gradleProject.create_modules()
    gradleProject.copy_gradle_files()
    print_info("Projeto atualizado...")
