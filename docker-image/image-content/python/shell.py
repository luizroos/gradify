import os
import tempfile
import subprocess
from ui import print_error

def execute_shell_commands(cmds: any, working_directory: str, vars: any):
    # Cria um arquivo temporário para consolidar os comandos
    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".sh") as temp_script:
        script_path = temp_script.name

        # Escreve as variáveis no script
        for var_name, value in vars.items():
            temp_script.write(f"{var_name}='{value}'\n")
        
        # Adiciona os comandos
        for cmd in cmds:
            temp_script.write(f"{cmd}\n")

    try:
        # Torna o script executável e executa
        os.chmod(script_path, 0o755)
        result = subprocess.run([script_path], cwd=working_directory, shell=True)
        if result.returncode != 0:
            print_error(f"Error applying scripts from {script_path}")
            exit(1)
    finally:
        os.remove(script_path)