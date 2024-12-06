import re

# TODO criar enum desses types e quem sabe usa-los direto

def validate_type(value: str, expected_type: str):
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