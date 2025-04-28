import logging
from ps_interpreter.core import op_stack, dict_stack, ParseFailed, TypeMismatch


# PARSER FUNCTIONS ---------------------------------------------------------------
def process_string(input):
    logging.debug(f"Input to process string: {input}")
    if len(input) >= 2 and input.startswith("(") and input.endswith(")"):
        return input[1:-1]
    raise ParseFailed("can't parse this into a string")

def process_boolean(input):
    logging.debug(f"Input to process boolean: {input}")
    if input == "true":
        return True
    elif input == "false":
        return False
    else:
        raise ParseFailed("can't parse it into boolean")
    
def process_number(input):
    logging.debug(f"Input to process number: {input}")
    try:
        float_value = float(input)
        if float_value.is_integer():
            return int(float_value)
        else:
            return float_value
    except ValueError:
        raise ParseFailed("can't parse this into a number")
    
def process_code_block(input):
    logging.debug(f"Input to process code block: {input}")
    if len(input) >= 2 and input.startswith("{") and input.endswith("}"):
        return input[1:-1].strip().split()
    else:
        raise ParseFailed("can't parse this into a code block")

def process_name_constant(input):
    logging.debug(f"Input to process name constant: {input}")
    if input.startswith("/"):
        return input
    else:
        raise ParseFailed("Can't parse into name constant")
    
def process_array(input):
    logging.debug(f"Input to process array: {input}")
    if len(input) >= 2 and input.startswith("[") and input.endswith("]"):
        inner = input[1:-1].strip()
        if not inner:
            return []
        return inner.split()
    raise ParseFailed("can't parse this into an array")


PARSERS = [
    process_string,
    process_boolean,
    process_number,
    process_code_block,
    process_name_constant,
    process_array
]


def process_constants(input):
    for parser in PARSERS:
        try:
            res = parser(input)
            op_stack.append(res)
            return
        except ParseFailed as e:
            logging.debug(e)
            continue
    raise ParseFailed(f"Not a literal: {input}")

def lookup_in_dictionary(input):
    top_dict = dict_stack[-1]
    if input not in top_dict:
        raise ParseFailed(f"input {input} is not in dictionary")
    value = top_dict[input]
    if callable(value):
        return value()
    if isinstance(value, list):
        for item in value:
            process_input(item)
    else:
        op_stack.append(value)


def process_input(token):
    try:
        process_constants(token)
    except ParseFailed as e:
        logging.debug(e)
        try:
            lookup_in_dictionary(token)
        except Exception as e:
            logging.error(e)