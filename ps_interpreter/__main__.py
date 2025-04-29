import argparse
import ps_interpreter.core as core
from .core import repl

def main():
    parser = argparse.ArgumentParser(
        prog="python -m ps_interpreter",
        description="Run the PostScript REPL"
    )
    parser.add_argument(
        "--lexical",
        action="store_true",
        help="Use lexical scoping instead of dynamic."
    )
    args, _ = parser.parse_known_args()
    core.lexical_scoping = args.lexical
    repl()

if __name__ == "__main__":
    main()