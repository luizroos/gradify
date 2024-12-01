import sys
from typing import Union
from code_template import CodeTemplate
from file_system import is_directory_exists, create_directories, copy_dir_content, load_yaml
from ui import print_info, print_warn, print_error
from logger_config import setup_logger
from system import get_gradify_base_dir
from template_render import gen_file_from_loaded_template
from project.project_module import ProjectModules, ProjectModule
from project.project_directory import ProjectDirectory, ProjectDirSyncAction, SyncAction

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
    def create_modules(self) -> bool:
        if not self.project_modules.has_unique_modules:
            # TODO criar uma classe para lidar com esse arquivo e poder fazer encapsular tudo isso la, 
            # inclusive a criação do objeto project_modules
            print_error("Arquivo de configuração inválido, possui módulos com nome ou id duplicado.")
            return False

        # cria o objeto que que representa a diretório do projeto
        project_directory = ProjectDirectory(
            project_base_dir=self.project_dir, 
            module_manifest_filename=MODULE_MANIFEST_FILENAME
        )

        # sincroniza os modulos do projeto com os diretorios, no callback sera notificado o que aconteceu
        project_directory.synchronize_with_project_modules(
            prj_modules=self.project_modules,
            action_callback=self.sync_callback
        )
        
    # callback chamado enquando ProjectDirectory ajusta os diretorios
    def sync_callback(self, sync_action: ProjectDirSyncAction):
        print(sync_action)
        if not sync_action.linked_module or sync_action.action != SyncAction.CREATE_NEW:
            return
        
        module = sync_action.linked_module       
        
        gradle_src_dirs = [
            "src",
            "src/main",
            "src/main/java",
            "src/main/resources",
            "src/test",
            "src/test/java",
        ]        
        module.create_module_directories(self.project_dir, gradle_src_dirs)

        # aplica um code template (TODO revisar daqui em diante)

        code_template = CodeTemplate(
            prj_module_path=module.module_path(self.project_dir), 
            tool_name=TOOL_NAME
        )
        code_template.apply()

if __name__ == "__main__":
    project_dir = sys.argv[1]
    prj_config_filename = sys.argv[2]
    
    print_info("Atualizando projeto...")
    gradleProject = GradleProject(
        project_dir=project_dir, 
        prj_config_filename=prj_config_filename
    )
    gradleProject.create_modules()
    gradleProject.copy_gradle_files()
    print_info("Projeto atualizado...")

