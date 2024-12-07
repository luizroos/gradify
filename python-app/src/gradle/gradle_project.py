import sys
import os
from typing import Union
from ui import print_info, print_error, print_warn
from file_system import load_yaml
from system import get_gradify_tools_dir
from project.project_module import ProjectModules
from project.project_directory import ProjectDirectory, ProjectDirSyncAction, SyncAction
from tools_dir.tools_dir import ToolsDirectory, ToolDirectory
from termcolor import colored

MODULE_MANIFEST_FILENAME=".gradify.yaml"

class GradleProject:
    # diretorio onde estao as configuracoes do graddle
    tool_dir: ToolDirectory

    # arquivo yaml do projeto
    prj_config_yaml: Union[dict, list]

    # diretório do projeto
    project_dir: ProjectDirectory

    # modulos do projeto
    project_modules: ProjectModules

    def __init__(self, project_dir: ProjectDirectory, prj_config_yaml: str, tool_dir: ToolDirectory):
        self.tool_dir = tool_dir
        self.project_dir = project_dir
        self.prj_config_yaml = prj_config_yaml

        project_modules = ProjectModules()
        yaml_modules = self.prj_config_yaml['project']['modules']
        for yaml_module in yaml_modules:
            project_modules.add_module(
                module_id=yaml_module.get("id"), 
                module_name=yaml_module["name"]
            )        
        self.project_modules = project_modules

    # aplica o template do projeto
    def apply_project_template(self):
        # TODO Não é possivel ter mais de um template, pois esses são justamente os arquivos que queremos
        # ficar atualizando, a menos que façamos uma alteração no yaml para incluir o template selecionado 
        # lá
        config_version = self.prj_config_yaml['configVersion']

        template = self.tool_dir.get_project_template(
            dest_path=self.project_dir.get_path(),
            version=config_version
        )

        template.apply_from_yaml_param_file(self.prj_config_yaml)
        return True

    # cria todos modulos do projeto gradle
    def update_modules(self) -> bool:
        if not self.project_modules.has_unique_modules():
            # TODO criar uma classe para lidar com esse arquivo e poder encapsular tudo isso la, 
            # inclusive a criação do objeto project_modules
            print_error("Arquivo de configuração inválido, possui módulos com nomes ou ids duplicados...")
            return False

        # sincroniza os modulos do projeto com os diretorios, no callback sera notificado o que aconteceu
        return self.project_dir.synchronize_with_project_modules(
            prj_modules=self.project_modules,
            action_callback=self.sync_callback
        )
        
    # callback chamado enquando ProjectDirectory ajusta os diretorios
    def sync_callback(self, sync_action: ProjectDirSyncAction, dry_run: bool):
        
        if dry_run or not sync_action.linked_module or sync_action.action != SyncAction.CREATE_NEW:
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
        # TODO, ver se da para passar ProjectDir para dentro de module
        module.create_module_directories(self.project_dir.get_path(), gradle_src_dirs)

        module_path=module.module_path(self.project_dir.get_path())
        template = self.tool_dir.get_module_template(
            dest_path=module_path
        )

        if not template:
            print_info(f"Não será aplicado nenhum template para {colored(module_path, attrs=['bold'])}...")
            return

        print_info(f"Aplicando template {colored(template.name, attrs=['bold'])}...")
        if template.apply_from_var_questions_param():
            print_info(f"Template aplicado com sucesso...")
        else:
            print_warn(f"Não foi possível aplicar o template...")

if __name__ == "__main__":
    project_dir = sys.argv[1]
    prj_config_filename = sys.argv[2]
    tools_path = sys.argv[3]

    prj_config_yaml = load_yaml(f"{project_dir}/{prj_config_filename}")

    # diretorio de tools que suportamos
    tools_directory = ToolsDirectory(
        path=tools_path
    )
    tool_directory = tools_directory.get_tool_dir("gradle")

    config_version = prj_config_yaml['configVersion']
    if not tool_directory.is_valid_version(version=config_version):
        print_error(f"Seu {prj_config_filename} especifica configVersion {config_version} que não é suportado")
        sys.exit(1)

    # cria o objeto que que representa a diretório do projeto
    project_directory = ProjectDirectory(
        path=project_dir, 
        module_manifest_filename=MODULE_MANIFEST_FILENAME
    )

    print_info("Atualizando projeto...")
    gradleProject = GradleProject(
        project_dir=project_directory, 
        tool_dir=tool_directory,
        prj_config_yaml=prj_config_yaml
    )

    print_info("Aplicando o template do projeto...")
    if not gradleProject.apply_project_template():
        print_error("Não foi possível aplicar o template do projeto...")
        sys.exit(1)

    print_info("Atualizando os módulos...")
    if not gradleProject.update_modules():
        print_error("Não foi possível atualizar os módulos...")
        sys.exit(1)
   
    print_info("Projeto atualizado...")

        

