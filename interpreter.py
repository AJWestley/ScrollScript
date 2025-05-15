import codecs
from lark import Transformer
from constants import KEYWORDS

class ScrollScriptInterpreter(Transformer):
    def __init__(self):
        self.variables = {}
    
    
    # ----- Assignments & Declarations ------
    
    def declaration(self, items):
        variable = items[1]
        value = items[2] if len(items) > 2 else None
        
        if variable in self.variables:
            raise Exception(f"The rune of '{variable}' is already written.")
        
        var_type = type(value)
        
        self.variables[variable] = {
            "value": value,
            "type": var_type,
            "previous": None
        }
        
        return (variable, value)
    
    def assignment(self, items):
        variable, value = items
        
        if variable not in self.variables:
            raise Exception(f"The rune of '{variable}' has not yet been written.")
        
        var_type = type(value)
        
        prev_value = self.variables[variable]['value']
        
        self.variables[variable] = {
            "value": value,
            "type": var_type,
            "previous": prev_value
        }
        return (variable, value)
    
    
    # ----- Expressions ------
    
    def string_concat(self, items):
        return items[0] + items[1]
    
    def bin_expr_add(self, items):
        left, op, right = items
        if op == "+":
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        if op == "-":
            return left - right
        
        raise Exception(f"Unknown spell:'{op}'")
    
    def bin_expr_mul(self, items):
        left, op, right = items
        
        if op == "*":
            return left * right
        
        if op == "/":
            return left / right
        
        if op == "%":
            return left % right
        
        raise Exception(f"Unknown spell:'{op}'")
    
    def bin_expr_pow(self, items):
        left, right = items
        
        return left ** right
    
    def bin_expr_or(self, items):
        left, _, right = items
        return left or right
    
    def bin_expr_and(self, items):
        left, _, right = items
        return left and right
    
    def group_expr(self, items):
        return items[0]

    def un_expr_negate(self, items):
        return -items[0]
    
    def un_expr_not(self, items):
        return not items[1]
    
    # ----- Variables ------

    def var_expr(self, items):
        name = str(items[0])
        if name not in self.variables:
            raise Exception(f"The rune of '{name}' has not yet been written.")
        elif self.variables[name] is None:
            raise Exception(f"The rune of '{name}' is written, but dormant.")
        return self.variables[name]['value']
    
    def var_name(self, items):
        return str(items[0])
    
    def VARIABLE(self, token):
        name = str(token)
        
        if name in KEYWORDS:
            raise Exception(f"{name} is a rooted in the arcane, and should not be used lightly.")
    
        return name
    
    
    # ----- Data Types ------
    
    def INTEGER(self, token):
        return int(token)
    
    def FLOAT(self, token):
        return float(token)
    
    def BOOLEAN(self, token):
        text = str(token)
        
        if text == 'True':
            return True
        elif text == 'False':
            return False
        
        raise Exception(f'A rune of bool may not be {text}.')
    
    def STRING(self, token):
        raw = str(token)[1:-1]

        unescaped = bytes(raw, "utf-8").decode("unicode_escape")
        return unescaped
    
    # ----- Operators ------
    
    
    
    
    # ----- Input & Output ------
    
    def print_statement(self, items):
        print(str(items[1]), end='')
    
    def input_statement(self, items):
        return input()
    
    def prompted_input(self, items):
        return input(items[1])


    # ----- Features ------
    
    def previous(self, items):
        name = str(items[0])
        if name not in self.variables:
            raise Exception(f"The rune of '{name}' has not yet been written.")
        elif self.variables[name] is None:
            raise Exception(f"The rune of '{name}' is written, but dormant.")
        return self.variables[name]['previous']