# Simple Python-Based Interpreter

## Description

This project implements a basic interpreter for a simple, custom programming language using Python. The interpreter can parse and execute scripts written in this language, supporting integer variables, arithmetic operations, expressions with parentheses, and `while` loops.

The primary goal was to create a functional interpreter demonstrating core concepts like lexical analysis (lexing), syntax analysis (parsing), and abstract syntax tree (AST) evaluation.

## Features

*   **Integer Variables:** Declare and assign integer values to variables (e.g., `my_var = 10;`).
*   **Arithmetic Operations:** Perform addition (`+`), subtraction (`-`), multiplication (`*`), integer division (`/`), and modulo (`%`).
*   **Expressions:** Evaluate complex integer expressions respecting operator precedence and parentheses (e.g., `result = (a + b) * 2 - (a / 5);`).
*   **While Loops:** Execute blocks of code repeatedly based on a condition (e.g., `while (counter) { ... }`). The loop continues as long as the condition evaluates to a non-zero integer.
*   **Code Blocks:** Group statements using curly braces `{ ... }`, primarily used for `while` loop bodies.
*   **Comments:** Ignore single-line comments starting with `#`.
*   **Basic Error Handling:** Reports syntax errors during parsing and runtime errors (like division by zero or undefined variables) during interpretation.
*   **Global Scope:** All variables are stored in a single global scope.

## Project Structure

```
python_interpreter/
├── interpreter/            # Core interpreter modules
│   ├── __init__.py
│   ├── lexer.py            # Lexical analyzer (Tokenizer)
│   ├── parser.py           # Syntax analyzer (Parser) & AST definitions
│   ├── interpreter.py      # AST visitor for execution
│   └── errors.py           # Custom error classes
├── tests/
│   ├── __init__.py
│   ├── sample_programs/    # Example scripts in the custom language
│   │   ├── basic_arithmetic.pi
│   │   └── while_loop.pi
│   ├── test_lexer.py       # Placeholder for lexer unit tests
│   ├── test_parser.py      # Placeholder for parser unit tests
│   └── test_interpreter.py # Placeholder for interpreter unit tests
├── main.py                 # Main script to run the interpreter
├── README.md               # This file
└── todo.md                 # Development task checklist
```

## How to Run

1.  Ensure you have Python 3 installed.
2.  Navigate to the `python_interpreter` directory in your terminal.
3.  Run the interpreter with a script file as an argument:

    ```bash
    python3.11 main.py tests/sample_programs/your_script_name.pi
    ```

    Replace `your_script_name.pi` with the path to the script you want to execute (e.g., `basic_arithmetic.pi` or `while_loop.pi`).

4.  The interpreter will execute the script and print the final state of all variables (the global scope) upon completion.

## Sample Programs

Two sample programs are included in the `tests/sample_programs/` directory:

*   `basic_arithmetic.pi`: Demonstrates variable assignment and various arithmetic operations.
*   `while_loop.pi`: Shows how to use `while` loops for iterative calculations (summation and factorial).

## Language Syntax Notes

*   The language currently only supports **integer** values and operations.
*   Statements can optionally be terminated by a semicolon (`;`). Semicolons are generally not required between statements but can be used for clarity or to separate multiple statements on a single line (though the latter is not explicitly tested).
*   Blocks of code for `while` loops must be enclosed in curly braces `{}`.
*   Variables must be assigned a value before being used in expressions.
*   All variables exist in a single **global scope**.
*   Comments start with `#` and extend to the end of the line.

