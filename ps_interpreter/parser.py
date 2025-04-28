import logging
import ps_interpreter.core as core
from ps_interpreter.core import CodeBlock, op_stack, dict_stack, ParseFailed, TypeMismatch


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
        toks = input[1:-1].strip().split()
        # capture current dict‐stack for lexical scoping later
        env_snapshot = dict_stack.copy()
        # return the CodeBlock, let process_constants append it
        return CodeBlock(toks, env_snapshot)
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

def lookup_in_dictionary(token):
    # 1) find value via dynamic lookup
    for d in reversed(dict_stack):
        if token in d:
            value = d[token]
            break
    else:
        raise ParseFailed(f"Undefined token: {token}")

    # 2) callable?
    if callable(value):
        return value()

    # 3) code block?
    if isinstance(value, CodeBlock):
        if core.lexical_scoping:
            # swap in the block’s env
            old_stack = dict_stack[:] 
            dict_stack[:] = [d.copy() for d in value.env]
            for t in value.tokens:
                process_input(t)
            dict_stack[:] = old_stack
        else:
            # dynamic
            for t in value.tokens:
                process_input(t)
        return

    # 4) literal
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