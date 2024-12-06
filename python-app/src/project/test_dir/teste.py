from typing import Dict, Optional
from file_system import load_yaml
from project.project_module import ProjectModules
from project.project_directory import ProjectDirectory, ProjectDirSyncAction, SyncAction

#### TODO criar um modelo de teste descente para isso, deixei esse diretorio com um cenario legal

def callback_fn(sync_action: ProjectDirSyncAction, dry_run: bool):
    print(dry_run)
    if not sync_action.linked_module or sync_action.action == SyncAction.KEEP:
        return
    print(f"callback: {sync_action} ")

if __name__ == "__main__":
    project_base_dir = "/project/python/project/test_dir/cenario1"
    MODULE_MANIFEST_FILENAME=".gradify.yaml"

    # carrega os modulos do arquivo
    prj_config_yaml = load_yaml(f"{project_base_dir}/project-config.yaml")    
    yaml_modules = prj_config_yaml['project']['modules']
    modules_dirs:  Dict[str, Optional[str]] = {}

    prj_modules = ProjectModules()
    for yaml_module in yaml_modules:
        prj_modules.add_module(
            module_id=yaml_module.get("id"),
            module_name=yaml_module["name"]
        )

    # cria o objeto que representa o diretorio 
    project_dir = ProjectDirectory(
        module_manifest_filename=MODULE_MANIFEST_FILENAME,
        project_base_dir=project_base_dir
    )
    project_dir.synchronize_with_project_modules(
        prj_modules=prj_modules,
        action_callback=callback_fn,
        dry_run=True
    )