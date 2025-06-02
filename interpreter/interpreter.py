# interpreter/interpreter.py
from .lexer import PLUS, MINUS, MUL, DIV, MOD
from .parser import BinOp, Num, UnaryOp, Assign, Var, Compound, NoOp, While
from .errors import SemanticError

class NodeVisitor:
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method")

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_SCOPE = {} # Symbol table

    def visit_BinOp(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)

        if not isinstance(left_val, int) or not isinstance(right_val, int):
             raise SemanticError("Type error: Both operands must be integers for binary operations")

        if node.op.type == PLUS:
            return left_val + right_val
        elif node.op.type == MINUS:
            return left_val - right_val
        elif node.op.type == MUL:
            return left_val * right_val
        elif node.op.type == DIV:
            if right_val == 0:
                raise SemanticError("Runtime error: Division by zero")
            # Integer division
            return left_val // right_val
        elif node.op.type == MOD:
            if right_val == 0:
                raise SemanticError("Runtime error: Modulo by zero")
            return left_val % right_val
        else:
             raise SemanticError(f"Unknown binary operator: {node.op.type}")

    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        val = self.visit(node.expr)
        if not isinstance(val, int):
             raise SemanticError("Type error: Operand must be an integer for unary operations")

        if node.op.type == PLUS:
            return +val
        elif node.op.type == MINUS:
            return -val
        else:
             raise SemanticError(f"Unknown unary operator: {node.op.type}")

    def visit_Assign(self, node):
        var_name = node.left.value
        # Evaluate the expression on the right side
        value = self.visit(node.right)
        if not isinstance(value, int):
             raise SemanticError(f"Type error: Cannot assign non-integer value to variable 	{var_name}")
        # Store the value in the symbol table
        self.GLOBAL_SCOPE[var_name] = value
        # Assignment statements don't return a value
        return None

    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise SemanticError(f"Name error: Variable 	{var_name}	 is not defined")
        else:
            return val

    def visit_Compound(self, node):
        # Execute each statement in the compound statement/block
        for child in node.children:
            self.visit(child)
        # Compound statements/blocks don't return a value
        return None

    def visit_While(self, node):
        # Evaluate the condition
        condition_value = self.visit(node.condition)

        # Loop while the condition is true (non-zero integer)
        while isinstance(condition_value, int) and condition_value != 0:
            # Execute the block of statements
            self.visit(node.block)
            # Re-evaluate the condition for the next iteration
            condition_value = self.visit(node.condition)

        # While loops don't return a value
        return None

    def visit_NoOp(self, node):
        # Do nothing for NoOp nodes (empty statements)
        pass

    def interpret(self):
        tree = self.parser.parse()
        if tree is None:
            return ""
        # Start visiting the root node (which should be a Compound node for the program)
        self.visit(tree)
        # Return the final state of the global scope for inspection or testing
        # print("Final Symbol Table:", self.GLOBAL_SCOPE) # Optional: print final state
        return self.GLOBAL_SCOPE

