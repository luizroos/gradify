import os
from typing import Optional
from dataclasses import dataclass
from template_dir.template_dir import TemplateDir, Template

@dataclass(frozen=True)
class ToolDirectory:
    path: str

    def is_valid_version(self, version: str) -> bool:
        return os.path.isdir(f"{self.path}/{version}")

    def get_module_template(self, dest_path):
        module_templates_path = f"{self.path}/module-templates"
        
        module_template_dir = TemplateDir(
            dest_path=dest_path,
            templates_path=module_templates_path
        )     

        return module_template_dir.select_template()   

    def get_project_template(self, dest_path: str, version: str) -> Template: 
        project_template_path=f"{self.path}/{version}/project-templates"

        project_template_dir = TemplateDir(
            dest_path=dest_path,
            templates_path=project_template_path,
            enable_no_template=False
        )

        return project_template_dir.select_template()



# representa diretorio onde tem as ferramentas que podemos usar para criar um projeto
# esse diretorio segue o modelo de:
# dir/
#   - {tool_name}/
#     - module-templates/ (veja template-dir)
#     - {versao}/project-template/ (veja template-dir)
@dataclass(frozen=True)
class ToolsDirectory:
    # diretorio onde encontramos as tools que lidamos 
    path: str

    def get_tool_dir(self, tool_name: str) -> Optional[ToolDirectory]:
        tool_path = f"{self.path}/{tool_name}"
        print(tool_path)
        if not os.path.isdir(tool_path):
            return None

        return ToolDirectory(
            path=tool_path
        )

if __name__ == "__main__":
    tools_dir = ToolsDirectory(
        path="/tools"
    )
    tools_dir.get_tool_dir("gradle")
