import ps_interpreter.core as core
from ps_interpreter.core import tokenize
from ps_interpreter.parser import process_input

def test_tokenize_literals_and_ops():
    line = " (foo)  true  3 4 add   % this is a comment"
    toks = tokenize(line)
    assert toks == ["(foo)", "true", "3", "4", "add"]

def test_string_and_boolean_and_number():
    core.op_stack.clear()
    process_input("(hello)")
    process_input("true")
    process_input("42")
    assert core.op_stack == ["hello", True, 42]

def test_array_and_codeblock():
    core.op_stack.clear()
    process_input("[1 2 bar]")
    arr = core.op_stack.pop()
    assert arr == ["1", "2", "bar"]

    process_input("{ 1 2 add }")
    cb = core.op_stack.pop()
    from ps_interpreter.core import CodeBlock
    assert isinstance(cb, CodeBlock)
    assert cb.tokens == ["1", "2", "add"]