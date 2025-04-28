# IMPORTS ----------------------------------------------------------------------------------------------
import math
import ps_interpreter.core as core

op_stack       = core.op_stack
dict_stack     = core.dict_stack
StackUnderflow = core.StackUnderflow
TypeMismatch   = core.TypeMismatch


# OPERATIONS -------------------------------------------------------------------------------------------

# Stack Manipulation
def exch_operation():
    if len(op_stack) >= 2:
        op2 = op_stack.pop()
        op1 = op_stack.pop()
        op_stack.append(op2)
        op_stack.append(op1)
    else:
        raise StackUnderflow("Need 2 operands for exch.")

def pop_operation():
    if len(op_stack) >= 1:
        op_stack.pop()
    else:
        raise StackUnderflow("Need 1 operand for pop.")
    
def copy_operation():
    if len(op_stack) >= 1:
        n = op_stack.pop()
        if n < 0:
            raise ValueError("Negative count for copy.")
        if len(op_stack) >= n:
            op_stack.extend(op_stack[-n:]) # gets the last n elements and appends them onto the stack
        else:
            raise StackUnderflow(f"There are not {n} operands on the stack.")
    else:
        raise StackUnderflow("Need 1 operand for copy.")    

def dup_operation():
    if len(op_stack) >= 1:
        op_stack.append(op_stack[-1])
    else:
        raise StackUnderflow("Need 1 operand for dup.")
    
def clear_operation():
    op_stack.clear() # empties the list in-place

def count_operation():
    op_stack.append(len(op_stack))

# Arithmetic
def add_operation():
    if len(op_stack) >= 2:
        op2 = op_stack.pop()
        op1 = op_stack.pop()
        res = op1 + op2
        op_stack.append(res)
    else:
        raise StackUnderflow("Need 2 operands for add.")

def sub_operation():
    if len(op_stack) >= 2:
        op2 = op_stack.pop()
        op1 = op_stack.pop()
        res = op1 - op2
        op_stack.append(res)
    else:
        raise StackUnderflow("Need 2 operands for sub.")

def mul_operation():
    if len(op_stack) >= 2:
        op2 = op_stack.pop()
        op1 = op_stack.pop()
        res = op1 * op2
        op_stack.append(res)
    else:
        raise StackUnderflow("Need 2 operands for mul.")

def div_operation():
    if len(op_stack) >= 2:
        op2 = op_stack.pop()
        op1 = op_stack.pop()
        if op2 != 0:
            res = op1 / op2
            op_stack.append(res)
        else:
            raise ValueError("Division by zero.")
    else:
        raise StackUnderflow("Need 2 operands for div.")

def idiv_operation():
    if len(op_stack) >= 2:
        op2 = op_stack.pop()
        op1 = op_stack.pop()
        if isinstance(op1, int) and isinstance(op2, int):
            if op2 != 0:
                res = int(op1 / op2) # truncates result towards 0
                op_stack.append(res)
            else:
                raise ValueError("Division by zero.")
        else:
            raise TypeMismatch("Operands must be integers for idiv.")
    else:
        raise StackUnderflow("Need 2 operands for idiv.")

def mod_operation():
    if len(op_stack) >= 2:
        op2 = op_stack.pop()
        op1 = op_stack.pop()
        if isinstance(op1, int) and isinstance(op2, int):
            if op2 != 0:
                res = int(op1 / op2) # truncates result towards 0
                res = op1 - (op2 * res) # gives remainder
                op_stack.append(res)
            else:
                raise ValueError("Division by zero.")
        else:
            raise TypeMismatch("Operands must be integers for mod.")
    else:
        raise StackUnderflow("Need 2 operands for mod.")

def abs_operation():
    if len(op_stack) >= 1:
        op = op_stack.pop()
        res = abs(op)
        op_stack.append(res)
    else:
        raise StackUnderflow("Need 1 operand for abs.")

def neg_operation():
    if len(op_stack) >= 1:
        op = op_stack.pop()
        res = -op
        op_stack.append(res)
    else:
        raise StackUnderflow("Need 1 operand for neg.")

def ceiling_operation():
    if len(op_stack) >= 1:
        op = op_stack.pop()
        res = math.ceil(op)
        op_stack.append(res)
    else:
        raise StackUnderflow("Need 1 operand for ceiling.")

def floor_operation():
    if len(op_stack) >= 1:
        op = op_stack.pop()
        res = math.floor(op)
        op_stack.append(res)
    else:
        raise StackUnderflow("Need 1 operand for floor.")

def round_operation():
    if len(op_stack) >= 1:
        op = op_stack.pop()
        res = math.floor(op + 0.5) if op >= 0 else math.ceil(op - 0.5)
        op_stack.append(res)
    else:
        raise StackUnderflow("Need 1 operand for round.")

def sqrt_operation():
    if len(op_stack) >= 1:
        op = op_stack.pop()
        if op >= 0:
            res = math.sqrt(op)
            op_stack.append(res)
        else:
            raise ValueError("Negative operand needed for sqrt.")
    else:
        raise StackUnderflow("Need 1 operand for sqrt.")

# Dictionary
def dict_operation():
    if len(op_stack) >= 1:
        n = op_stack.pop()
        if isinstance(n, int):
            if n >= 0:
                op_stack.append({}) # python doesn't need to pre-size a dictionary so the hint is ignored
            else:
                raise ValueError("Negative size for dict.")
        else:
            raise TypeMismatch("Operand must be integer for dict.")
    else:
        raise StackUnderflow("Need 1 operand for dict.")

def length_operation(): # can be used for string also
    if len(op_stack) >= 1:
        obj = op_stack.pop()
        if isinstance(obj, (str, list, dict)):
            op_stack.append(len(obj))
        else:
            raise TypeMismatch("Unsupported type for length.")
    else:
        raise StackUnderflow("Need 1 operand for length.")

def maxlength_operation():
    if len(op_stack) >= 1:
        obj = op_stack.pop()
        if isinstance(obj, (str, list, dict)):
            op_stack.append(len(obj))
        else:
            raise TypeMismatch("Unsupported type for maxlength.")
    else:
        raise StackUnderflow("Need 1 operand for maxlength.")

def begin_operation():
    if len(op_stack) >= 1:
        d = op_stack.pop()
        if isinstance(d, dict):
            dict_stack.append(d)
        else:
            raise TypeMismatch("Operand must be dictionary for begin.")
    else:
        raise StackUnderflow("Need 1 operand for begin.")
    
def end_operation():
    if len(dict_stack) > 1:
        dict_stack.pop()
    else:
        raise StackUnderflow("Dictionary stack underflow for end.")    

def def_operation():
    if len(op_stack) >= 2:
        value = op_stack.pop()
        name = op_stack.pop()
        if isinstance(name, str) and name.startswith("/"):
            key = name[1:]
            dict_stack[-1][key] = value
        else:
            raise TypeMismatch("Key must be string for def.")
    else:
        raise StackUnderflow("Need 2 operands for def.")

# Strings
def get_operation():
    if len(op_stack) >= 2:
        index = op_stack.pop()
        container = op_stack.pop()

        if not isinstance(index, int):
            raise TypeMismatch("Index must be integer for get.")

        if isinstance(container, str):
            if 0 <= index < len(container):
                op_stack.append(ord(container[index]))
            else:
                raise ValueError("Index out of range for get.")
        elif isinstance(container, list):
            if 0 <= index < len(container):
                op_stack.append(container[index])
            else:
                raise ValueError("Index out of range for get.")
        else:
            raise TypeMismatch("Container must be string or array for get.")
    else:
        raise StackUnderflow("Need 2 operands for get.")

def getinterval_operation():
    if len(op_stack) >= 3:
        count = op_stack.pop()
        index = op_stack.pop()
        container = op_stack.pop()

        if not isinstance(index, int) or not isinstance(count, int):
            raise TypeMismatch("Index and count must be integers for getinterval.")
        if count < 0:
            raise ValueError("Negative count for getinterval.")

        if isinstance(container, str):
            if 0 <= index <= len(container) - count:
                op_stack.append(container[index:index + count])
            else:
                raise ValueError("Index range out of bounds for getinterval.")
        elif isinstance(container, list):
            if 0 <= index <= len(container) - count:
                op_stack.append(container[index:index + count])
            else:
                raise ValueError("Index range out of bounds for getinterval.")
        else:
            raise TypeMismatch("Container must be string or array for getinterval.")
    else:
        raise StackUnderflow("Need 3 operands for getinterval.")

def putinterval_operation():
    if len(op_stack) >= 3:
        source = op_stack.pop()
        index  = op_stack.pop()
        container = op_stack.pop()

        # type checks
        if not isinstance(index, int):
            raise TypeMismatch("Index must be integer for putinterval.")
        if index < 0:
            raise ValueError("Negative index for putinterval.")
        if type(container) != type(source) or not isinstance(container, (str, list)):
            raise TypeMismatch("Container and source must be same type (string or array).")

        count = len(source)
        if index + count > len(container):
            raise ValueError("Range out of bounds for putinterval.")

        # perform the write
        if isinstance(container, list):
            container[index:index + count] = source
        else:
            container = container[:index] + source + container[index + count:]

        # push the container back so caller still has it
        op_stack.append(container)
    else:
        raise StackUnderflow("Need 3 operands for putinterval.")

# Bit and Boolean Operations
def eq_operation():
    if len(op_stack) >= 2:
        op2 = op_stack.pop()
        op1 = op_stack.pop()
        op_stack.append(op1 == op2)
    else:
        raise StackUnderflow("Need 2 operands for eq.")

def ne_operation():
    if len(op_stack) >= 2:
        op2 = op_stack.pop()
        op1 = op_stack.pop()
        op_stack.append(op1 != op2)
    else:
        raise StackUnderflow("Need 2 operands for ne.")
    
def ge_operation():
    if len(op_stack) >= 2:
        op2 = op_stack.pop()
        op1 = op_stack.pop()
        op_stack.append(op1 >= op2)
    else:
        raise StackUnderflow("Need 2 operands for ge.")

def gt_operation():
    if len(op_stack) >= 2:
        op2 = op_stack.pop()
        op1 = op_stack.pop()
        op_stack.append(op1 > op2)
    else:
        raise StackUnderflow("Need 2 operands for gt.")
    
def le_operation():
    if len(op_stack) >= 2:
        op2 = op_stack.pop()
        op1 = op_stack.pop()
        op_stack.append(op1 <= op2)
    else:
        raise StackUnderflow("Need 2 operands for le.")    

def lt_operation():
    if len(op_stack) >= 2:
        op2 = op_stack.pop()
        op1 = op_stack.pop()
        op_stack.append(op1 < op2)
    else:
        raise StackUnderflow("Need 2 operands for lt.")
    
def and_operation():
    if len(op_stack) >= 2:
        op2 = op_stack.pop()
        op1 = op_stack.pop()
        # logical AND for booleans
        if isinstance(op1, bool) and isinstance(op2, bool):
            res = op1 and op2
        # bitwise AND for integers
        elif isinstance(op1, int) and isinstance(op2, int):
            res = op1 & op2
        else:
            raise TypeMismatch("Operands must be both booleans or both integers for and.")
        op_stack.append(res)
    else:
        raise StackUnderflow("Need 2 operands for and.")
    
def not_operation():
    if len(op_stack) >= 1:
        op = op_stack.pop()
        if isinstance(op, bool):
            res = not op
        elif isinstance(op, int):
            res = ~op
        else:
            raise TypeMismatch("Operand must be boolean or integer for not.")
        op_stack.append(res)
    else:
        raise StackUnderflow("Need 1 operand for not.")
# Flow Control


# Input and Output



# DICTIONARY BATCH REGISTRATION ------------------------------------------------------------------------

operations = {
    # stack manipulation
    "exch":  exch_operation,
    "pop":   pop_operation,
    "copy":  copy_operation,
    "dup":   dup_operation,
    "clear": clear_operation,
    "count": count_operation,
    # arithmetic
    "add":     add_operation,
    "sub":     sub_operation,
    "mul":     mul_operation,
    "div":     div_operation,
    "idiv":    idiv_operation,
    "mod":     mod_operation,
    "abs":     abs_operation,
    "neg":     neg_operation,
    "ceiling": ceiling_operation,
    "floor":   floor_operation,
    "round":   round_operation,
    "sqrt":    sqrt_operation,
    # dictionary
    "dict":      dict_operation,
    "length":    length_operation,
    "maxlength": maxlength_operation,
    "begin":     begin_operation,
    "end":       end_operation,
    "def":       def_operation,
    # strings
    "get":          get_operation,
    "getinterval":  getinterval_operation,
    "putinterval":  putinterval_operation,
    # bit and boolean operations

    # flow control

    # input and output
}

dict_stack[-1].update(operations)