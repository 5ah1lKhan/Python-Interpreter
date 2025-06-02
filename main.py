# main.py
import sys
from interpreter.lexer import Lexer
from interpreter.parser import Parser
from interpreter.interpreter import Interpreter
from interpreter.errors import InterpreterError

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <filename.pi>")
        sys.exit(1)

    filepath = sys.argv[1]
    try:
        with open(filepath, "r") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    if not text.strip():
        print("Input file is empty.")
        # Optionally return the empty scope or handle as needed
        print("Final State: {}")
        sys.exit(0)

    try:
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result_scope = interpreter.interpret()
        # Print the final state of the global scope after execution
        print("Execution finished.")
        print("Final Variable State:", result_scope)

    except InterpreterError as e:
        print(f"Interpreter Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

