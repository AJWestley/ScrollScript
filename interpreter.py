import codecs
from lark import Transformer
import keywords
from utils import is_constant
from datatypes import wrap_primitive, ScrollBool, ScrollFloat, ScrollInt, ScrollString

class ScrollScriptInterpreter(Transformer):
    def __init__(self):
        self.variables = {}
    
    
    # ----- Assignments & Declarations ------
    
    def declaration(self, items):
        variable = items[1]

        if variable in self.variables:
            raise Exception(f"The rune of '{variable}' is already written.")

        if len(items) > 2 and items[2] is not None:
            value = wrap_primitive(items[2])
            var_type = type(value).type_name
        else:
            value = None
            var_type = None

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
        
        value = wrap_primitive(value)
        var_type = type(value).type_name
        
        prev_value = self.variables[variable]['value']
        
        self.variables[variable] = {
            "value": value,
            "type": var_type,
            "previous": prev_value
        }
        return (variable, value)
    
    
    # ----- Expressions ------
    
    def string_concat(self, items):
        return wrap_primitive(items[0]) + wrap_primitive(items[1])
    
    def bin_expr_add(self, items):
        left, op, right = items
        left, right = wrap_primitive(left), wrap_primitive(right)
        
        if op == "+":
            return left + right
        if op == "-":
            return left - right
        
        raise Exception(f"Unknown spell:'{op}'")
    
    def bin_expr_mul(self, items):
        left, op, right = items
        left, right = wrap_primitive(left), wrap_primitive(right)
        
        if op == "*":
            return left * right
        
        if op == "/":
            return left / right
        
        if op == "%":
            return left % right
        
        raise Exception(f"Unknown spell:'{op}'")
    
    def bin_expr_pow(self, items):
        left, right = wrap_primitive(items[0]), wrap_primitive(items[1])
        
        return left ** right
    
    def bin_expr_or(self, items):
        left, _, right = items
        left, right = wrap_primitive(left), wrap_primitive(right)
        return ScrollBool(left or right)
    
    def bin_expr_and(self, items):
        left, _, right = items
        left, right = wrap_primitive(left), wrap_primitive(right)
        return ScrollBool(left and right)
    
    def group_expr(self, items):
        return wrap_primitive(items[0])

    def un_expr_negate(self, items):
        return -wrap_primitive(items[0])
    
    def un_expr_not(self, items):
        return ScrollBool(not bool(wrap_primitive(items[1])))
    
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
        
        if is_constant(name):
            raise Exception(f"{name} is a rooted in the arcane, and should not be used lightly.")
    
        return name
    
    def value_cast(self, items):
        print(f"value_cast items: {items!r}")
        value = wrap_primitive(items[1])
        
        target_type = str(items[3])

        try:
            return value.cast_to(target_type)
        except Exception as e:
            raise Exception(f"Transmutation failed: {e}")
    
    # ----- Data Types ------
    
    def INTEGER(self, token):
        return ScrollInt(int(token))
    
    def FLOAT(self, token):
        return ScrollFloat(float(token))
    
    def BOOLEAN(self, token):
        text = ScrollString(str(token))
        
        return text.cast_to(keywords.BOOLEAN)
    
    def STRING(self, token):
        raw = str(token)[1:-1]

        unescaped = bytes(raw, "utf-8").decode("unicode_escape")
        return ScrollString(str(unescaped))
    
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