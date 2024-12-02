import sys
from typing import Union
from ui import print_info, print_error
from file_system import copy_dir_content, load_yaml
from logger_config import setup_logger
from system import get_gradify_base_dir
from template_render import gen_file_from_loaded_template
from project.project_module import ProjectModules
from project.project_directory import ProjectDirectory, ProjectDirSyncAction, SyncAction
from template_dir.template_dir import TemplateDir
from termcolor import colored

logger = setup_logger()
TOOL_NAME="gradle"
MODULE_MANIFEST_FILENAME=".gradify.yaml"

class GradleProject:
    # arquivo yaml do projeto
    prj_config_yaml: Union[dict, list]

    # diretório do projeto
    project_dir: str

    # modulos do projeto
    project_modules: ProjectModules

    def __init__(self, project_dir: str, prj_config_filename: str):
        self.project_dir = project_dir
        self.prj_config_yaml = load_yaml(f"{project_dir}/{prj_config_filename}")

        project_modules = ProjectModules()
        yaml_modules = self.prj_config_yaml['project']['modules']
        for yaml_module in yaml_modules:
            project_modules.add_module(
                module_id=yaml_module.get("id"), 
                module_name=yaml_module["name"]
            )        
        self.project_modules = project_modules

    # copia/atualiza os arquivos de configuracao do gradle para dentro do projeto
    def copy_gradle_files(self):
        gradify_base_dir = get_gradify_base_dir()
        config_version = self.prj_config_yaml['configVersion']

        # TODO fazer isso usando TemplateDir
        project_template_path=f"{gradify_base_dir}/{TOOL_NAME}/{config_version}/project-templates"

        copy_dir_content(f"{project_template_path}/gradle-8.11.1", self.project_dir)  
        self._update_gradle_file(project_template_path, "build.gradle.j2", "build.gradle")
        self._update_gradle_file(project_template_path, "settings.gradle.j2", "settings.gradle")
        self._update_gradle_file(project_template_path, "libs.versions.toml.j2", "gradle/libs.versions.toml")
        return True

    def _update_gradle_file(self, project_template_path: str, template_file: str, dest_file: str):
        template_file_path=f"{project_template_path}/templates/{template_file}"
        dest_file_path=f"{self.project_dir}/{dest_file}"
        gen_file_from_loaded_template(template_file_path, dest_file_path, self.prj_config_yaml)

    # cria todos modulos do projeto gradle
    def update_modules(self) -> bool:
        if not self.project_modules.has_unique_modules():
            # TODO criar uma classe para lidar com esse arquivo e poder fazer encapsular tudo isso la, 
            # inclusive a criação do objeto project_modules
            print_error("Arquivo de configuração inválido, possui módulos com nomes ou ids duplicados...")
            return False

        # cria o objeto que que representa a diretório do projeto
        project_directory = ProjectDirectory(
            project_base_dir=self.project_dir, 
            module_manifest_filename=MODULE_MANIFEST_FILENAME
        )

        # sincroniza os modulos do projeto com os diretorios, no callback sera notificado o que aconteceu
        return project_directory.synchronize_with_project_modules(
            prj_modules=self.project_modules,
            action_callback=self.sync_callback
        )
        
    # callback chamado enquando ProjectDirectory ajusta os diretorios
    def sync_callback(self, sync_action: ProjectDirSyncAction):
        
        if not sync_action.linked_module or sync_action.action != SyncAction.CREATE_NEW:
            return
        
        module = sync_action.linked_module       
        
        # TODO isso tudo aqui poderia ser feito um dia reusando a estrutura de code template
        gradle_src_dirs = [
            "src",
            "src/main",
            "src/main/java",
            "src/main/resources",
            "src/test",
            "src/test/java",
        ]        
        # TODO ta criando errado
        module.create_module_directories(self.project_dir, gradle_src_dirs)

        # aplica um code template (TODO revisar daqui em diante)
        
        module_templates_path = f"{get_gradify_base_dir()}/{TOOL_NAME}/module-templates"

        module_path=module.module_path(self.project_dir)
        module_template_dir = TemplateDir(
            dest_path=module_path,
            templates_path=module_templates_path
        )
        selected_template = module_template_dir.select_template()
        if not selected_template:
            print_info(f"Não será aplicado nenhum template para {colored(module_path, attrs=['bold'])}...")
            return

        print_info(f"Aplicando template {colored(selected_template.name, attrs=['bold'])}...")
        if selected_template.apply():
            print_info(f"Template aplicado com sucesso...")
        else:
            print_info(f"Não foi possível aplicar o template...")

if __name__ == "__main__":
    project_dir = sys.argv[1]
    prj_config_filename = sys.argv[2]
    
    print_info("Atualizando projeto...")
    gradleProject = GradleProject(
        project_dir=project_dir, 
        prj_config_filename=prj_config_filename
    )

    print_info("Atualizando os módulos...")
    if not gradleProject.update_modules():
        print_error("Não foi possível atualizar os módulos...")

    print_info("Atualizando arquivos do gradle...")
    if not gradleProject.copy_gradle_files():
        print_error("Não foi possível atualizar os arquivos do gradle...")
    
    print_info("Projeto atualizado...")

        

