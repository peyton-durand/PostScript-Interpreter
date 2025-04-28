import re
import logging
logging.basicConfig(level = logging.DEBUG)

op_stack = [] # operand stack
dict_stack = [] # dictionary stack
dict_stack.append({})

class ParseFailed(Exception):
    """ Exception while parsing """
    def __init__(self, message):
        super().__init__(message)

class TypeMismatch(Exception):
    """ Exception with types of operators and operands """
    def __init__(self, message):
        super().__init__(message)

class StackUnderflow(Exception):
    """ Exception with amount of operands """
    def __init__(self, message):
        super().__init__(message)


# repl and input processing --------------------------------------------------------------------------------------
from ps_interpreter.parser import process_input

# regex
_TOKEN_RE = re.compile(
    r'%.*$|'         #  1) comments       → '%...' to end-of-line
    r'\([^)]*\)|'    #  2) strings        → '( ... )'
    r'\{[^}]*\}|'    #  3) code blocks    → '{ ... }'
    r'\[[^\]]*\]|'   #  4) arrays         → '\[ ... \]'
    r'[^\s]+'        #  5) bare tokens    → sequences of non-whitespace characters
)

def tokenize(line):
    tokens = []
    for m in _TOKEN_RE.finditer(line): # walks through the line in order and groups based on the regex
        tok = m.group(0) # pulls out the grouped text from the regex
        if tok.startswith('%'): # handles comments
            break
        tokens.append(tok) # adds a token to the list
        logging.debug(f"Token: {tok}")
    return tokens # returns the list of tokens

def repl():
    while True:
        line = input("REPL> ") # reads in the user entered line
        if line.lower() == "quit": # checks for user trying to exit
            break
        for tok in tokenize(line): # loops through the list of tokens produced by tokenize
            process_input(tok) # sends the token to the parser
        logging.debug(f"Operand Stack: {op_stack}")




# import operators
import ps_interpreter.operations

# entry point
if __name__ == "__main__":
    repl()