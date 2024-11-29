import questionary
import re
import sys
from termcolor import colored
from datetime import datetime
from logger_config import setup_logger
from functools import partial

logger = setup_logger()
print_prefix = colored("Gradify", "light_blue")

def print_info(message: str):
    #formatted_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
    print(f"{print_prefix} {message}")

def print_warn(message: str):
    print_info(colored(message, "yellow"))

def print_error(message: str):
    print_info(colored(message, "red"))

def ui_options(question: str, options: any):
    option = questionary.select(
        message=question,
        qmark="Gradify",
        choices=options
    ).ask()
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
        printWarn("Valor inválido! Tente novamente.")
        return ui_question(question, q_type, default_value)
    
    return response.strip()

def validate_type(value, expected_type):
    if expected_type == "boolean":
        return value in ["true", "false"]
    
    elif expected_type == "integer":
        return bool(re.match(r"^[+-]?[0-9]+$", value))
    
    elif expected_type == "positive_integer":
        return bool(re.match(r"^[0-9]+$", value)) and int(value) > 0
    
    elif expected_type == "decimal":
        return bool(re.match(r"^[+-]?[0-9]*[.]?[0-9]+$", value))
    
    elif expected_type == "string":
        return True
    
    elif expected_type == "string_no_spaces":
        return bool(re.match(r"^[^\s]+$", value))
    
    elif expected_type == "string_alphanumeric":
        return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9]*$", value))
    
    else:
        return False


if __name__ == "__main__":
    method = sys.argv[1]
    out_file_resp = sys.argv[2]

    response = None
    if method == 'ui_question':
        question = sys.argv[3]
        q_type = sys.argv[4]
        default_value = sys.argv[5]    
        response = ui_question(question, q_type, default_value)
    elif method == 'ui_options':
        question = sys.argv[3]
        options = sys.argv[4]        
        options_list = options.split(",")
        response = ui_options(question, options_list)
    else: 
        raise ValueError("Invalid Method!")
    
    with open(out_file_resp, 'w') as f:
        f.write(response.strip())    