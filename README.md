# Python PostScript Interpreter

A minimal PostScript‑like interpreter in Python supporting a defined subset of commands, dynamic scoping by default, and optional lexical scoping via a command‑line flag.

## Prerequisites

* Python 3.8 or higher
* (Optional) a virtual environment tool such as venv or virtualenv

## Setup and Installation

1. Clone the repository
2. (Optional) Create and activate a virtual environment
3. Install dependencies via requirements.txt

## Running the Interpreter

Once in the project folder, run
```python
# for dynamic scoping (default)
python3 -m ps_interpreter

# for lexical scoping
python3 -m ps_interpreter --lexical
```
* Dynamic scoping: variables and procedures resolve against the current dictionary stack at call time.
* Lexical scoping: procedures capture the dictionary environment at definition time and use that when executed.

The prompt will indicate the mode:
* ```REPL>``` for dynamic mode
* ```lexical REPL>``` for lexical mode

## Running Tests

text

## Command Subset

[PostScript command subset.docx](https://github.com/user-attachments/files/19951626/PostScript.command.subset.docx)
