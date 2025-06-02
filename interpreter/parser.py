# interpreter/parser.py
from .lexer import (
    INTEGER, PLUS, MINUS, MUL, DIV, MOD, LPAREN, RPAREN, ID, ASSIGN, SEMI, EOF,
    WHILE, LBRACE, RBRACE
)

# --- AST Nodes ---
class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left  # ID token
        self.token = self.op = op # ASSIGN token
        self.right = right # Expression AST node

class Var(AST):
    """The Var node is constructed out of ID token."""
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Compound(AST):
    """Represents a block of statements, e.g., { statement_list } or the main program."""
    def __init__(self):
        self.children = []

class While(AST):
    """Represents a while loop: while (condition) block"""
    def __init__(self, condition, block):
        self.condition = condition # Expression AST node
        self.block = block # Compound AST node

class NoOp(AST):
    """Represents an empty statement."""
    pass

# --- Parser ---
class ParserError(Exception):
    pass

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        # Set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self, message="Invalid syntax"):
        raise ParserError(f"{message} (token: {self.current_token})")

    def eat(self, token_type):
        # Compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Expected token {token_type}, got {self.current_token.type}")

    def factor(self):
        """factor : (PLUS | MINUS) factor | INTEGER | LPAREN expr RPAREN | variable"""
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type == ID:
             node = self.variable()
             return node
        else:
            self.error("Expected INTEGER, LPAREN, PLUS, MINUS or ID")

    def term(self):
        """term : factor ((MUL | DIV | MOD) factor)*"""
        node = self.factor()

        while self.current_token.type in (MUL, DIV, MOD):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            elif token.type == MOD:
                self.eat(MOD)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        """expr : term ((PLUS | MINUS) term)*"""
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def variable(self):
        """variable : ID"""
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def assignment_statement(self):
        """assignment_statement : variable ASSIGN expr"""
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def while_statement(self):
        """while_statement : WHILE LPAREN expr RPAREN block"""
        self.eat(WHILE)
        self.eat(LPAREN)
        condition = self.expr()
        self.eat(RPAREN)
        block = self.block()
        node = While(condition, block)
        return node

    def block(self):
        """block : LBRACE statement_list RBRACE"""
        self.eat(LBRACE)
        # statement_list now returns a list of nodes
        statement_nodes = self.statement_list()
        self.eat(RBRACE)

        root = Compound()
        # Add all statements parsed within the block
        root.children.extend(statement_nodes)
        # Handle empty block { } -> Compound with NoOp
        if not root.children:
            root.children.append(NoOp())
        return root

    def statement(self):
        """statement : assignment_statement
                     | while_statement
                     | block
                     | empty"""
        if self.current_token.type == ID:
            node = self.assignment_statement()
        elif self.current_token.type == WHILE:
            node = self.while_statement()
        elif self.current_token.type == LBRACE:
            node = self.block()
        elif self.current_token.type == SEMI:
            # Explicit empty statement via semicolon
            self.eat(SEMI)
            node = self.empty()
        else:
            # If it's not the start of a known statement or an explicit empty statement,
            # consider it an implicit empty statement (NoOp) only if followed by EOF or RBRACE?
            # Or raise error? Let's be stricter for now and rely on statement_list logic.
            # If we reach here, it might mean statement_list logic needs adjustment.
            # For now, let's assume it's an error if not handled by statement_list.
            # Revert to previous logic: if not ID/WHILE/LBRACE, it's NoOp.
            node = self.empty()
            # self.error(f"Unexpected token {self.current_token.type} at start of statement")
        return node

    def statement_list(self):
        """statement_list : statement (statement)* """
        # Handles sequences of statements within the program or a block.
        # Semicolons are treated more like optional terminators.
        nodes = []

        # Keep parsing statements as long as we haven't reached EOF or the end of a block (RBRACE)
        while self.current_token.type not in (EOF, RBRACE):
            current_statement = self.statement()
            nodes.append(current_statement)

            # Optional: Consume a semicolon if present after a statement, but don't require it.
            if self.current_token.type == SEMI:
                self.eat(SEMI)
                # If semicolon is followed immediately by RBRACE or EOF, it was a trailing one.
                if self.current_token.type in (EOF, RBRACE):
                    break
            # If the next token is not the start of a statement, and not EOF/RBRACE, it might be an error
            # This check might be too strict depending on language design (e.g., allowing expressions as statements)
            # Let's rely on the statement() method to handle valid starts or produce NoOp/Error.

        # Filter out NoOp nodes unless the list is empty or contains only NoOps
        filtered_nodes = [node for node in nodes if not isinstance(node, NoOp)]
        if not filtered_nodes and nodes: # Contained only NoOps
            return [NoOp()] # Return a single NoOp for purely empty lists/blocks
        elif not nodes: # Was genuinely empty
             return [NoOp()] # Represent empty block/program as NoOp
        else:
            return filtered_nodes # Return statements without unnecessary NoOps

    def empty(self):
        """An empty production"""
        return NoOp()

    def program(self):
        """program : statement_list"""
        nodes = self.statement_list() # Returns a list of statements
        if self.current_token.type != EOF:
            self.error(f"Unexpected token {self.current_token.type} after program statements")

        root = Compound()
        # Add all parsed statements to the program's compound node
        root.children.extend(nodes)
        # Ensure even an empty program results in a Compound node containing at least NoOp
        if not root.children:
            root.children.append(NoOp())

        return root

    def parse(self):
        node = self.program()
        # EOF check is now within program()
        return node

