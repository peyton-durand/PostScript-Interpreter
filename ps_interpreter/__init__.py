import argparse
import ps_interpreter.core as core
from .core import repl

# 1) parse the --lexical flag
parser = argparse.ArgumentParser(prog="python -m ps_interpreter")
parser.add_argument(
    "--lexical",
    action="store_true",
    help="Use lexical scoping instead of dynamic."
)
# use parse_known_args so you don’t break if you add other flags later
args, _ = parser.parse_known_args()

# 2) set the core flag
core.lexical_scoping = args.lexical

# 3) start the REPL with the correct prompt
repl()