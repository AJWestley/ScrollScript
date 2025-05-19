import random
import math
from lark import Token
import keywords
from utils import is_keyword, is_number
from datatypes import wrap_primitive, ScrollBool, ScrollFloat, ScrollInt, ScrollString
from exceptions import *

class ScrollScriptInterpreter:
    def __init__(self):
        self.variables = {}
    
    
    def start(self, tree):
        for instruction in tree.children:
            # print(instruction.pretty())
            self.execute(instruction)
    
    
    # ----- Assignments & Declarations ------
    
    def var_declaration(self, tree):
        items = tree.children
        variable = self.execute(items[1])

        if variable in self.variables:
            raise RuneAlreadyWrittenError(variable)
        
        if len(items) > 2 and items[2] is not None:
            value = self.execute(items[2])
            value = wrap_primitive(value)
            var_type = type(value).type_name
        else:
            value = None
            var_type = None

        self.variables[variable] = {
            "value": value,
            "type": var_type,
            "const": False,
            "previous": None
        }

    def const_declaration(self, tree):
        items = tree.children
        variable = self.execute(items[2])

        if variable in self.variables:
            raise RuneAlreadyWrittenError(variable)

        if len(items) > 3 and items[3] is not None:
            value = self.execute(items[3])
            value = wrap_primitive(value)
            var_type = type(value).type_name
        else:
            value = None
            var_type = None

        self.variables[variable] = {
            "value": value,
            "type": var_type,
            "const": True,
            "previous": None
        }
    
    def assignment(self, tree):
        name, value = self.execute(tree.children[0]), self.execute(tree.children[1])
        
        if name not in self.variables:
            raise RuneNotWrittenError(name)
        
        if self.variables[name]['const']:
            raise SealedRuneError(name)
        
        value = wrap_primitive(value)
        new_type = type(value).type_name
        old_type = self.variables[name]['type']
        
        self.variables[name]['previous'] = self.variables[name]['value'] if old_type == new_type else None
        self.variables[name]['value'] = value 
        self.variables[name]['type'] = new_type
    
    def deletion(self, tree):
        variable = self.execute(tree.children[1])

        if variable not in self.variables:
            raise RuneNotWrittenError(variable)
        
        self.variables.pop(variable)
    
    def seal_statement(self, tree):
        name = self.execute(tree.children[1])
        
        if name not in self.variables:
            raise RuneNotWrittenError(name)
        
        if self.variables[name]['const']:
            raise SealedRuneError(name)
        
        self.variables[name]['const'] = True
    
    def simple_increment(self, tree):
        name = self.execute(tree.children[0])

        if name not in self.variables:
            raise RuneNotWrittenError(name)
        elif self.variables[name]['const']:
            raise SealedRuneError(name)
        
        op = self.execute(tree.children[1])
        
        if not is_number(self.variables[name]['value']):
            raise CarelessSpellError(f"'{self.variables[name]['type']}' {op} is an invalid incantation.")
        
        match op:
            case "++": self.variables[name]['value'] += 1
            case "--": self.variables[name]['value'] -= 1
            case _: raise UnknownSpellError(op)
    
    def compound_increment(self, tree):
        name = self.execute(tree.children[0])

        if name not in self.variables:
            raise RuneNotWrittenError(name)
        elif self.variables[name]['const']:
            raise SealedRuneError(name)
        
        op = self.execute(tree.children[1])
        value = self.execute(tree.children[2])
        
        if not is_number(self.variables[name]['value']) or not is_number(value):
            raise CarelessSpellError(f"'{self.variables[name]['type']}' {op} '{value.type_name}' is an invalid incantation.")
        
        match op:
            case "+=": self.variables[name]['value'] += value
            case "-=": self.variables[name]['value'] -= value
            case "*=": self.variables[name]['value'] *= value
            case "/=": self.variables[name]['value'] /= value
            case "%=": self.variables[name]['value'] %= value
            case "^=": self.variables[name]['value'] **= value
            case "/+=": self.variables[name]['value'] = math.floor((self.variables[name]['value'] + value).value)
            case "/-=": self.variables[name]['value'] = math.floor((self.variables[name]['value'] - value).value)
            case "/*=": self.variables[name]['value'] = math.floor((self.variables[name]['value'] * value).value)
            case "//=": self.variables[name]['value'] //= value
            case "/^=": self.variables[name]['value'] = math.floor((self.variables[name]['value'] ** value).value)
            case "/%=": self.variables[name]['value'] = math.floor((self.variables[name]['value'] % value).value)
            case "^+=": self.variables[name]['value'] = math.ceil((self.variables[name]['value'] + value).value)
            case "^-=": self.variables[name]['value'] = math.ceil((self.variables[name]['value'] - value).value)
            case "^*=": self.variables[name]['value'] = math.ceil((self.variables[name]['value'] * value).value)
            case "^/=": self.variables[name]['value'] = math.ceil((self.variables[name]['value'] / value).value)
            case "^^=": self.variables[name]['value'] = math.ceil((self.variables[name]['value'] ** value).value)
            case "~%=": self.variables[name]['value'] = math.ceil((self.variables[name]['value'] % value).value)
            case "~+=": self.variables[name]['value'] = round((self.variables[name]['value'] + value).value)
            case "~-=": self.variables[name]['value'] = round((self.variables[name]['value'] - value).value)
            case "~*=": self.variables[name]['value'] = round((self.variables[name]['value'] * value).value)
            case "~/=": self.variables[name]['value'] = round((self.variables[name]['value'] / value).value)
            case "~^=": self.variables[name]['value'] = round((self.variables[name]['value'] ** value).value)
            case "~%=": self.variables[name]['value'] = round((self.variables[name]['value'] % value).value)
            case _: raise UnknownSpellError(op)
        self.variables[name]['value'] = wrap_primitive(self.variables[name]['value'])
        self.variables[name]['type'] = self.variables[name]['value'].type_name
            
    
    # ----- Expressions ------
    
    def bin_expr_add(self, tree):
        left, op, right = list(map(self.execute, tree.children))
        left, right = wrap_primitive(left), wrap_primitive(right)
        
        if not (is_number(left) and is_number(right)):
            raise CarelessSpellError(f"'{left.type_name}' + '{right.type_name}' is an invalid incantation.")
        
        value = None
        match op:
            case "+": value = left + right
            case "/+": value = math.floor((left + right).value)
            case "^+": value = math.ceil((left + right).value)
            case "~+": value = round((left + right).value)
            case "-": value = left - right
            case "/-": value = math.floor((left - right).value)
            case "^-": value = math.ceil((left - right).value)
            case "~-": value = round((left - right).value)
            case _: raise UnknownSpellError(op)
        return wrap_primitive(value)
    
    def bin_expr_mul(self, tree):
        left, op, right = list(map(self.execute, tree.children))
        left, right = wrap_primitive(left), wrap_primitive(right)
        
        value = None
        match op:
            case "*": value = left * right
            case "/*": value = math.floor((left * right).value)
            case "^*": value = math.ceil((left * right).value)
            case "~*": value = round((left * right).value)
            case "/": value = left / right
            case "//": value = left // right
            case "^/": value = math.ceil((left / right).value)
            case "~/": value = round((left / right).value)
            case "%": value = left % right
            case "/%": value = math.floor((left % right).value)
            case "^%": value = math.ceil((left % right).value)
            case "~%": value = round((left % right).value)
            case _: value = UnknownSpellError(op)
        return wrap_primitive(value)
    
    def bin_expr_pow(self, tree):
        left, right = self.execute(tree.children[0]), self.execute(tree.children[1])
        left, right = wrap_primitive(left), wrap_primitive(right)
        return left ** right
    
    def bin_expr_or(self, tree):
        left, right = self.execute(tree.children[0]), self.execute(tree.children[2])
        left, right = wrap_primitive(left), wrap_primitive(right)
        return ScrollBool(left or right)
    
    def bin_expr_and(self, tree):
        left, right = self.execute(tree.children[0]), self.execute(tree.children[2])
        left, right = wrap_primitive(left), wrap_primitive(right)
        return ScrollBool(left and right)
    
    def bin_expr_comp(self, tree):
        left, op, right = list(map(self.execute, tree.children))
        match op:
            case "<": val = left < right
            case ">": val = left > right
            case "<=": val = left <= right
            case ">=": val = left >= right
            case "==": val = left == right
            case "!=": val = left != right
            case _: raise UnknownSpellError(op)
        return ScrollBool(val)
    
    def group_expr(self, tree):
        value = self.execute(tree.children[0])
        return wrap_primitive(value)

    def un_expr_negate(self, tree):
        value = self.execute(tree.children[0])
        return -wrap_primitive(value)
    
    def un_expr_round(self, tree):
        op = self.execute(tree.children[0])
        value = self.execute(tree.children[1])
        match op:
            case "~": value = round(value.value)
            case "/": value = math.floor(value.value)
            case "^": value = math.ceil(value.value)
            case _: raise UnknownSpellError(op)
        return wrap_primitive(value)
    
    def un_expr_not(self, tree):
        value = self.execute(tree.children[1])
        return ScrollBool(not bool(wrap_primitive(value)))
    
    def length_expr(self, tree):
        variable = self.execute(tree.children[1])
        sz = len(variable)
        return wrap_primitive(sz)
    
    
    # ----- Control Flow ------
    
    def block(self, tree):
        for instruction in tree.children:
            self.execute(instruction)
    
    def if_statement(self, tree):
        i = 0
        while i < len(tree.children) and tree.children[i] is not None:
            if_type = self.execute(tree.children[i])
            if if_type == keywords.ELSE:
                self.execute(tree.children[i+1])
                break
            condition = self.execute(tree.children[i+1])
            if_block = tree.children[i+2]
            if condition:
                self.execute(if_block)
                break
            i += 3
    
    def maybe_statement(self, tree):
        ratio = tree.children[1]
        if ratio is not None:
            ratio = self.execute(ratio)
        else:
            ratio = 0.5

        block = tree.children[2]
        if random.uniform(0, 1) < ratio:
            self.execute(block)
    
    def ratio(self, tree):
        left, right = int(tree.children[0].value), int(tree.children[1].value)
        if left < 0 or right < 0 or left + right == 0:
            raise CarelessSpellError(f"'{left}' : '{right}' is an invalid incantation.")
        return left / (left + right)
    
    def for_range(self, tree):
        var_name, var_type, start, stop, step = self.execute(tree.children[1])

        self.variables[var_name] = {
            "value": start,
            "type": var_type,
            "const": False,
            "previous": None
        }

        block = tree.children[2]

        while self.variables[var_name]['value'] <= stop:
            try:
                self.execute(block)
            except ShatterError:
                break
            except PersistenceError:
                pass
            self.variables[var_name]['previous'] = self.variables[var_name]['value']
            self.variables[var_name]['value'] += step
        
        del self.variables[var_name]
    
    def infinite_loop(self, tree):
        block = tree.children[3]
        while True:
            try:
                self.execute(block)
            except ShatterError:
                break
            except PersistenceError:
                pass
            
    
    def range_expression(self, tree):
        name = self.execute(tree.children[0])

        start = self.execute(tree.children[1])
        stop = self.execute(tree.children[2])
        step = self.execute(tree.children[3]) if tree.children[3] is not None else 1

        start = wrap_primitive(start)
        stop = wrap_primitive(stop)
        step = wrap_primitive(step)

        if not is_number(start) or not is_number(stop) or not is_number(step):
            raise CarelessSpellError(f"'{start.type_name}' -> '{stop.type_name}' | '{step.type_name}' is an invalid incantation.")

        var_type = 'float' if isinstance(start, ScrollFloat) or isinstance(stop, ScrollFloat) or isinstance(step, ScrollFloat) else 'int'

        if name in self.variables:
            raise RuneAlreadyWrittenError(name)
        
        return name, var_type, start, stop, step
    
    def loop_interrupt(self, tree):
        self.execute(tree.children[0])
    
    def BREAK(self, tree):
        raise ShatterError()

    def CONTINUE(self, tree):
        raise PersistenceError()

    def IF(self, token):
        return str(token.value)

    def ELIF(self, token):
        return str(token.value)
    
    def ELSE(self, token):
        return str(token.value)
    
    def AD(self, token):
        return str(token.value)
    
    def INFINITUM(self, token):
        return str(token.value)
    
    
    # ----- Variables ------

    def var_expr(self, tree):
        name = self.execute(tree.children[0])
        name = str(name)
        if name not in self.variables:
            raise RuneNotWrittenError(name)
        elif self.variables[name]['value'] is None:
            raise DormantRuneError(name)
        return self.variables[name]['value']
    
    def var_name(self, tree):
        value = self.execute(tree.children[0])
        return str(value)
    
    def VARIABLE(self, token):
        name = str(token)
        if is_keyword(name):
            raise FundamentalRuneError(name)
        return name
    
    def value_cast(self, tree):
        value = self.execute(tree.children[1])
        value = wrap_primitive(value)
        
        target_type = self.execute(tree.children[3])
        target_type = str(target_type)

        try:
            return value.cast_to(target_type)
        except Exception:
            raise TransmutationError(value.type_name, target_type)
    
    # ----- Data Types ------
    
    def INTEGER(self, token):
        return ScrollInt(int(token))
    
    def FLOAT(self, token):
        return ScrollFloat(float(token))
    
    def BOOLEAN(self, token):
        return ScrollBool(str(token))
    
    def STRING(self, token):
        raw = str(token)[1:-1]
        unescaped = bytes(raw, "utf-8").decode("unicode_escape")
        return ScrollString(str(unescaped))
    
    def DATA_TYPE(self, token):
        return str(token.value)
    
    # ----- Operators ------
    
    def ADD_OP(self, token):
        return str(token.value)
    
    def MUL_OP(self, token):
        return str(token.value)
    
    def COMP_OP(self, token):
        return str(token.value)
    
    def INCR_OP(self, token):
        return str(token.value)
    
    def CMP_INCR_OP(self, token):
        return str(token.value)
    
    def ROUND_OP(self, token):
        return str(token.value)
    
    
    # ----- Input & Output ------
    
    def print_statement(self, tree):
        text = self.execute(tree.children[1])
        print(str(text), end='')
    
    def input_statement(self, tree):
        return input()
    
    def prompted_input(self, tree):
        text = self.execute(tree.children[1])
        return input(str(text))


    # ----- Features ------
    
    def interpolated_string(self, tree):
        items = list(map(self.execute, tree.children[1:-1]))
        result = "".join([str(part) for part in items])
        return wrap_primitive(result)
    
    def interpolation_part(self, tree):
        items = list(map(self.execute, tree.children))
        if len(items) == 1 and isinstance(items[0], ScrollString):
            return items[0]
        else:
            return items[1]

    def INTERP_TEXT(self, token): 
        raw = str(token)
        unescaped = bytes(raw, "utf-8").decode("unicode_escape")
        return ScrollString(str(unescaped))
    
    def INTERP_EXPR_START(self, _): 
        pass
    
    def INTERP_EXPR_END(self, _): 
        pass
    

    # ----- Unique Features ------
    
    def previous(self, tree):
        name = self.execute(tree.children[0])
        name = str(name)
        if name not in self.variables:
            raise RuneNotWrittenError(name)
        elif self.variables[name]['previous'] is None:
            raise NoPastError(name)
        return self.variables[name]['previous']
    
    def execute(self, node):
        method_name = node.type if isinstance(node, Token) else node.data
        func = getattr(self, method_name, None)
        if callable(func):
            return func(node)
        else:
            raise ScrollError(f"Something is amiss in the arcane ({method_name}).")