import questionary
import sys
from system import is_debug_mode
from termcolor import colored
from logger_config import setup_logger
from functools import partial
from types_validate import validate_type

# basicamente tem funções para lidar com a iteração com o usuário

logger = setup_logger()
print_prefix = colored("Gradify", "light_blue")

def _print(message: str):
    print(f"{print_prefix} {message}")

def print_info(message: str):
    #formatted_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
    _print(message)

def print_warn(message: str):
    _print(colored(message, "yellow"))

def print_error(message: str):
    _print(colored(message, "red"))

def print_debug(message: str):
    if is_debug_mode():
        _print(f"{colored("DEBUG", "red")} {colored(message, "green")}")

def ui_options(question: str, options: any):
    while True:
        option = questionary.select(
            message=question,
            qmark="Gradify",
            choices=options
        ).ask()
        if option is not None:
            return option

def ui_question(question: str, q_type: str, default_value: str):
    if q_type == "boolean":
        response = ui_options(question, ["true", "false"])
    else:
        response = questionary.text(
            message=question,
            qmark="Gradify",
            instruction=q_type, # acho que isso pode tirar depois
            default=default_value,
            validate=partial(validate_type, expected_type=q_type)
        ).ask()

    if not response or not validate_type(response.strip(), q_type):
        print_warn("Valor inválido! Tente novamente.")
        return ui_question(question, q_type, default_value)
    
    return response.strip()

if __name__ == "__main__":
    method = sys.argv[1]
    message = sys.argv[2]

    if method == 'print_info':
        print_info(message)
    elif method == 'print_warn':
        print_warn(message)
    elif method == 'print_error':
        print_error(message)
    else: 
        raise ValueError("Invalid Method!")