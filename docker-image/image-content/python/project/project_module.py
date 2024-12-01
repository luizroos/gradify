import os
from dataclasses import dataclass, field
from typing import List, Optional

# Representação do módulo de um projeto
@dataclass
class ProjectModule:

    # id opcional do modulo, o id serve como identificador unico e com ele podemos gerenciar mudanças de nome para o modulo
    id: Optional[str]
    
    # nome do modulo
    name: str

    def module_path(self, base_dir: str) -> str:
        return f"{base_dir}/{self.name}"

    # verifica se existe um diretório para o módulo, dentro da um diretório base
    def directory_exists(self, base_dir: str) -> bool:
        return os.path.isdir(self.module_path(base_dir))

    # cria a estrutura do módulo dentro de um diretório base
    def create_module_directories(self, base_dir: str, relative_dirs: List[str]):
        for relative_dir in relative_dirs:
            full_path = os.path.join(base_dir, relative_dir)
            os.makedirs(full_path, exist_ok=True)

# Representa a lista de modulos do projeto
@dataclass
class ProjectModules:

    # lista de módulos que o projeto tem
    modules: List[ProjectModule] = field(default_factory=list)

    # adiciona um módulo
    def add_module(self, module_name: str, module_id: Optional[int] = None):
        self.modules.append(ProjectModule(
            id=module_id,
            name=module_name,
        ))

    # verficia se os ids e nomes dos módulos são unicos
    def has_unique_modules(modules: List[ProjectModule]) -> bool:
        ids = [module.id for module in modules]
        names = [module.name for module in modules]
        if len(ids) != len(set(ids)):
            return False
        if len(names) != len(set(names)):
            return False