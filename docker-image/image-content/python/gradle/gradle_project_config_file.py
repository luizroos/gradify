
from file_system import load_yaml
from typing import List
from project.project_module import ProjectModules
from types_validate import validate_type

# TODO 

class GradleProjectConfigFile:

  def __init__(self, project_dir: str, filename: str):
    self.filename = filename
    self.prj_config_yaml = load_yaml(f"{project_dir}/{filename}")

  def validate(self) -> bool:
    errors : List[str] = []
    yaml_modules = self.prj_config_yaml['project']['modules']
    for yaml_module in yaml_modules:
        if yaml_module.get("id") and not validate_type(yaml_module.get("id"), "string_alphanumeric"):
           errors.append("project.modules[].id")
        
        if not validate_type(yaml_module["name"], "string_alphanumeric"):
           errors.append("project.modules[].name")
    return True

schema = {
    'configVersion': {
        'type': 'string',
        'allowed': ['v1'],
        'required': True
    },
    'project': {
        'type': 'dict',
        'required': True,
        'schema': {
            'name': {
                'type': 'string',
                'regex': '^[a-zA-Z0-9]+$',  # Só pode ser alfanumérico
                'required': True
            },
            'group': {
                'type': 'string',
                'regex': '^[a-zA-Z0-9]+$',  # Só pode ser alfanumérico
                'required': True
            },
            'version': {
                'type': 'string',
                'required': True
            },
            'language': {
                'type': 'dict',
                'required': True,
                'schema': {
                    'type': {
                        'type': 'string',
                        'allowed': ['java'],  # Só pode ser java
                        'required': True
                    },
                    'version': {
                        'type': 'integer',  # Deve ser um inteiro
                        'required': True
                    }
                }
            },
            'versionCatalogs': {
                'type': 'dict',
                'nullable': True,
                'schema': {
                    'versions': {
                        'type': 'list',
                        'nullable': True,
                        'schema': {'type': 'string'}
                    },
                    'plugins': {
                        'type': 'list',
                        'nullable': True,
                        'schema': {'type': 'string'}
                    },
                    'libraries': {
                        'type': 'list',
                        'nullable': True,
                        'schema': {'type': 'string'}
                    }
                }
            },
            'repositories': {
                'type': 'list',
                'nullable': True,
                'schema': {'type': 'string'}
            },
            'plugins': {
                'type': 'list',
                'nullable': True,
                'schema': {'type': 'string'}
            },
            'subprojects': {
                'type': 'list',
                'nullable': True,
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'plugins': {
                            'type': 'list',
                            'nullable': True,
                            'schema': {'type': 'string'}
                        },
                        'dependencies': {
                            'type': 'list',
                            'nullable': True,
                            'schema': {'type': 'string'}
                        }
                    }
                }
            },
            'modules': {
                'type': 'list',
                'required': True,
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'name': {
                            'type': 'string',
                            'regex': '^[a-zA-Z0-9]+$',  # Só pode ser alfanumérico
                            'required': True
                        },
                        'id': {
                            'type': 'string',
                            'regex': '^[a-zA-Z0-9]+$',  # Só pode ser alfanumérico
                            'nullable': True
                        },
                        'plugins': {
                            'type': 'list',
                            'nullable': True,
                            'schema': {'type': 'string'}
                        },
                        'dependencies': {
                            'type': 'list',
                            'nullable': True,
                            'schema': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
}