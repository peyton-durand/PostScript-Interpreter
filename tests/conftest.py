import importlib
import pytest
import ps_interpreter.core as core

@pytest.fixture(autouse=True)
def reset_interpreter_state():
    """
    Clear the operand & dictionary stacks and re-register ops before each test.
    """
    core.op_stack.clear()
    core.dict_stack.clear()
    core.dict_stack.append({})
    # re-load operations so they update the fresh dict_stack
    import ps_interpreter.operations as ops_mod
    importlib.reload(ops_mod)