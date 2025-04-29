import pytest
from ps_interpreter.parser import process_input
import ps_interpreter.core as core

def run(tokens):
    for t in tokens:
        process_input(t)

def test_add():
    run(["2", "3", "add"])
    assert core.op_stack.pop() == 5

def test_sub():
    run(["10", "4", "sub"])
    assert core.op_stack.pop() == 6

def test_mul():
    run(["3", "5", "mul"])
    assert core.op_stack.pop() == 15

def test_div():
    run(["9", "3", "div"])
    assert core.op_stack.pop() == 3.0

def test_idiv_and_mod():
    run(["9", "2", "idiv"])
    assert core.op_stack.pop() == 4
    run(["9", "2", "mod"])
    assert core.op_stack.pop() == 1

def test_stack_underflow():
    # calling add with too few operands raises
    with pytest.raises(core.StackUnderflow):
        run(["1", "add"])