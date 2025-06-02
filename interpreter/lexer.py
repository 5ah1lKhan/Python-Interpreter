# interpreter/lexer.py

# Token types
INTEGER       = "INTEGER"
PLUS          = "PLUS"
MINUS         = "MINUS"
MUL           = "MUL"
DIV           = "DIV"
MOD           = "MOD"
LPAREN        = "LPAREN"
RPAREN        = "RPAREN"
ID            = "ID"
ASSIGN        = "ASSIGN"
SEMI          = "SEMI"  # Semicolon to separate statements
EOF           = "EOF"   # End of file

# Keywords
WHILE         = "WHILE"
LBRACE        = "LBRACE" # { 
RBRACE        = "RBRACE" # }

# --- Token Class (Defined before use) ---
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {repr(self.value)})"

    def __repr__(self):
        return self.__str__()

# --- Reserved Keywords (Uses Token class) ---
RESERVED_KEYWORDS = {
    "while": Token(WHILE, "while"),
}

# --- Lexer Error Class ---
class LexerError(Exception):
    pass

# --- Lexer Class ---
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def advance(self):
        """Advance the 'pos' pointer and set the 'current_char' variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        """Skip single-line comments starting with #."""
        while self.current_char is not None and self.current_char != "\n":
            self.advance()
        # Advance past the newline character as well, if present
        if self.current_char == "\n":
            self.advance()

    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def identifier(self):
        """Handle identifiers and reserved keywords."""
        result = ""
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == "_"):
            result += self.current_char
            self.advance()

        # Check if the identifier is a reserved keyword
        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # Skip comments
            if self.current_char == "#":
                self.skip_comment()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char.isalpha() or self.current_char == "_":
                return self.identifier()

            if self.current_char == "=":
                self.advance()
                return Token(ASSIGN, "=")

            if self.current_char == ";":
                self.advance()
                return Token(SEMI, ";")

            if self.current_char == "+":
                self.advance()
                return Token(PLUS, "+")

            if self.current_char == "-":
                self.advance()
                return Token(MINUS, "-")

            if self.current_char == "*":
                self.advance()
                return Token(MUL, "*")

            if self.current_char == "/":
                self.advance()
                return Token(DIV, "/")

            if self.current_char == "%" :
                self.advance()
                return Token(MOD, "%")

            if self.current_char == "(":
                self.advance()
                return Token(LPAREN, "(")

            if self.current_char == ")":
                self.advance()
                return Token(RPAREN, ")")

            if self.current_char == "{":
                self.advance()
                return Token(LBRACE, "{")

            if self.current_char == "}":
                self.advance()
                return Token(RBRACE, "}")

            # If character is not recognized
            raise LexerError(f"Invalid character: {self.current_char}")

        return Token(EOF, None)

