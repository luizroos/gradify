import os
import yaml
from termcolor import colored
from typing import Dict
from enum import Enum
from typing import List, Callable, Optional
from ui import print_error, print_info
from dataclasses import dataclass
from file_system import load_yaml
from project.project_module import ProjectModules, ProjectModule

# Tipo de acoes que da para fazer
class SyncAction(Enum):
    CREATE_NEW = 1
    RENAME = 2
    KEEP = 3

# a acao que deve ser executada em um diretorio do projeto
@dataclass
class ProjectDirSyncAction:
    # nome atual
    current_name: Optional[str] = None

    # id unico para esse diretorio
    mid: Optional[str] = None

    # nome que deve ficar
    target_name: Optional[str] = None
    
    # acao que devemos fazer ara sair de current_name para target_name
    action: Optional[SyncAction] = None

    # módulo que pode estar linkado com esse diretório
    linked_module: Optional[ProjectModule] = None

    def update_mid(self, mid: str):
        self.mid = mid
  
    def rename_to(self, target_name: str, linked_module: ProjectModule):
        self.target_name = target_name
        self.linked_module = linked_module
        self.action = SyncAction.RENAME

    def keep_current_name(self, linked_module: Optional[ProjectModule] = None):
        self.target_name = self.current_name
        self.linked_module = linked_module
        self.action = SyncAction.KEEP

    def __str__(self):
        return f"ProjectDirSyncAction(\n\tcurrent_name={self.current_name}, mid={self.mid}, target_name={self.target_name}, action={self.action}, linked_module={self.linked_module}\n)"


# Representa o diretório do projeto
@dataclass(frozen=True)
class ProjectDirectory:
    # diretorio base do projeto
    project_base_dir: str
   
    # arquivo de manifesto
    module_manifest_filename: str

    # sincroniza o diretório do projeto com a definição de módulos que o projeto tem. Esse método vai atualizar ou criar diretórios novos.
    def synchronize_with_project_modules(
            self,
            # diretorios de modulos (chave = nome do diretorio, valor = id (opcional))
            prj_modules: ProjectModules,
            # callback
            action_callback: Callable[[ProjectDirSyncAction], None] = None
    ) -> bool:

        # verifica a consistência dos dados de módulos (como vamos criar diretórios, não pode haver módulos repetidos)
        if not prj_modules.has_unique_modules():
            return False

        mid_map: Dict[str, ProjectDirSyncAction] = {}
        current_name_map: Dict[str, ProjectDirSyncAction] = {}
        directories: List[ProjectDirSyncAction] = []

        # verifica os diretorios atuais, montando current_name e o id único (pego do arquivo de manifest)
        for entry in os.scandir(self.project_base_dir):
            if not entry.is_dir():
                continue

            prj_dir = ProjectDirSyncAction(
                current_name=entry.name
            )
            directories.append(prj_dir)

            manifest_file = load_yaml(f"{entry.path}/{self.module_manifest_filename}")    
            dir_module_id = manifest_file.get("module_id") if manifest_file else None
            if dir_module_id:
                prj_dir.update_mid(dir_module_id)
                mid_map[dir_module_id] = prj_dir
            
            current_name_map[prj_dir.current_name] = prj_dir

        # verifica os módulos informados e decide se se deve criar novos ou renomear algum (com base no module id que o diretório pode ter)
        for module in prj_modules.modules:
            prj_dir = mid_map.get(module.id)
            if prj_dir:
                # um diretorio já existe para esse module id, renomearemos esse diretório para o nome desse módulo
                if(prj_dir.current_name == module.name):
                    prj_dir.keep_current_name(
                        linked_module=module
                    )
                else:
                    prj_dir.rename_to(
                        target_name=module.name,
                        linked_module=module
                    )
            elif not module.directory_exists(self.project_base_dir):
                # não existe um diretório ainda para esse nome, então criaremos um novo
                new_prj_dir = ProjectDirSyncAction(
                    target_name=module.name,
                    action=SyncAction.CREATE_NEW,
                    linked_module=module
                )   
                directories.append(new_prj_dir)            

        # Podem ter sobrado módulos que tinham diretorios criados mas que seus ids foram alterados 
        # ou reusados por outros módulos, aqui vamos decidir se mantemos o diretório com mesmo nome só atualizando
        # o arquivo de configuração, ou se vamos criar um novo diretório
        for module in prj_modules.modules:
            prj_dir = current_name_map.get(module.name)
            if not prj_dir:
                # é um modulo novo, ignora que já foi tratado antes
                continue
            
            if not prj_dir.target_name:
                # se o diretório ainda esta sem target_name, reaproveita, e provavelmente o que ocorreu foi a perda do arquivo
                # de configuração ou mudança de id
                prj_dir.keep_current_name(
                    linked_module=module
                )
            elif prj_dir.target_name != module.name:
                # o target_name existe, mas não é o mesmo que o nome do modulo, então provavelmente o seu id foi reaproveitado
                #  para outro, o diretorio sera renomeado e criaremos outro diretorio para esse
                new_prj_dir = ProjectDirSyncAction(
                    target_name=module.name,
                    action=SyncAction.CREATE_NEW,
                    linked_module=module
                )
                directories.append(new_prj_dir)     

        # por fim, diretorios sem acao, devem apenas ser mantidos
        for prj_dir in directories:
            if not prj_dir.action:
                prj_dir.keep_current_name()

        # executa as ações para sincronizar os diretorios
        return self.execute_project_dir_sync_actions(
            directories=directories,
            action_callback=action_callback
        )

    # executa as acoes definidas para os diretorios
    def execute_project_dir_sync_actions(
            self, 
            directories: List[ProjectDirSyncAction], 
            action_callback: Callable[[ProjectDirSyncAction], None] = None
    ) -> bool:
        for prj_dir in directories:
            if not prj_dir.action:
                continue
            if prj_dir.action == SyncAction.CREATE_NEW:
                os.makedirs(f"{self.project_base_dir}/{prj_dir.target_name}", exist_ok=True)
                print_info(f"Diretório {prj_dir.target_name} {colored("criado", attrs=['bold'])}...")
            elif prj_dir.action == SyncAction.RENAME:
                # renomeia primeiro para o id unico e depois para o final
                os.rename(f"{self.project_base_dir}/{prj_dir.current_name}", f"{self.project_base_dir}/{prj_dir.mid}")

        for prj_dir in directories:
            if not prj_dir.action:
                continue
            if prj_dir.action == SyncAction.RENAME:
                os.rename(f"{self.project_base_dir}/{prj_dir.mid}", f"{self.project_base_dir}/{prj_dir.target_name}")
                print_info(f"Diretório {prj_dir.current_name} {colored("renomeado", attrs=['bold'])} para {prj_dir.target_name}...")

        # cria o arquivo de manifest para todos diretorios que tem um modulo linkado e que o modulo tenha um id
        for prj_dir in directories:
            linked_module = prj_dir.linked_module
            if linked_module and linked_module.id:
                self.create_manifest_file(
                    relative_path=prj_dir.target_name,
                    module_id=linked_module.id
                )

        # faz a chamada do callback
        if not action_callback:
            return True
        for action in directories:
            action_callback(action)
        return True

    # cria o arquivo de manifesto
    def create_manifest_file(self, relative_path: str, module_id: str):
        manifest_file_yaml = os.path.join(f"{self.project_base_dir}/{relative_path}", self.module_manifest_filename)
        content = {
            "module_id": module_id
        }
        with open(manifest_file_yaml, 'w') as file:
            yaml.dump(content, file, default_flow_style=False)