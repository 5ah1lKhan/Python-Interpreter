# interpreter/errors.py

class InterpreterError(Exception):
    pass

class LexerError(InterpreterError):
    pass

class ParserError(InterpreterError):
    pass

class SemanticError(InterpreterError):
    pass

