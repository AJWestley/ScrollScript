class ScrollValue:
    def cast_to(self, target_type: str):
        raise NotImplementedError("Casting not implemented for this type.")

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {str(self)}>"


class ScrollBool(ScrollValue):
    
    type_name = 'bool'
    
    def __init__(self, value):
        if isinstance(value, str):
            self.value = value == "Truthsung"
        else:
            self.value = bool(value)

    def __bool__(self):
        return self.value

    def __str__(self):
        return "Truthsung" if self.value else "Falsehood"

    def __repr__(self):
        return f"<ScrollBool: {'Truthsung' if self.value else 'Falsehood'}>"

    def __eq__(self, other):
        if isinstance(other, ScrollBool):
            return self.value == other.value
        return self.value == bool(other)

    def __and__(self, other):
        return ScrollBool(self.value and bool(other))

    def __or__(self, other):
        return ScrollBool(self.value or bool(other))

    def __invert__(self):
        return ScrollBool(not self.value)
    
    def __add__(self, other):
        if isinstance(other, ScrollString):
            return ScrollString(str(self) + other.value)
        else:
            return ScrollString(str(self) + str(other))
    
    def __radd__(self, other):
        return ScrollString(str(other) + str(self))

    def cast_to(self, target_type: str):
        if target_type == "bool":
            return self
        elif target_type == "int":
            return ScrollInt(1 if self.value else 0)
        elif target_type == "float":
            return ScrollFloat(1.0 if self.value else 0.0)
        elif target_type == "string":
            return ScrollString(str(self))
        else:
            raise ValueError(f"Cannot cast bool to {target_type}")


class ScrollInt(ScrollValue):
    
    type_name = 'int'
    
    def __init__(self, value: int):
        self.value = int(value)
        
    def __add__(self, other):
        return ScrollInt(self.value + wrap_primitive(other).value)

    def __sub__(self, other):
        return ScrollInt(self.value - wrap_primitive(other).value)

    def __mul__(self, other):
        return ScrollInt(self.value * wrap_primitive(other).value)

    def __truediv__(self, other):
        other_val = wrap_primitive(other).value
        if other_val == 0:
            raise ZeroDivisionError("The arcane winds forbid division by zero.")
        return ScrollFloat(self.value / wrap_primitive(other).value)

    def __mod__(self, other):
        return ScrollInt(self.value % wrap_primitive(other).value)

    def __pow__(self, other):
        return ScrollInt(self.value ** wrap_primitive(other).value)
    
    def __neg__(self):
        return ScrollInt(-self.value)

    def cast_to(self, target_type: str):
        if target_type == "int":
            return self
        elif target_type == "float":
            return ScrollFloat(float(self.value))
        elif target_type == "bool":
            return ScrollBool(self.value != 0)
        elif target_type == "string":
            return ScrollString(str(self.value))
        else:
            raise ValueError(f"Cannot cast int to {target_type}")


class ScrollFloat(ScrollValue):
    
    type_name = 'float'
    
    def __init__(self, value: float):
        self.value = float(value)
    
    def __add__(self, other):
        return ScrollFloat(self.value + wrap_primitive(other).value)

    def __sub__(self, other):
        return ScrollFloat(self.value - wrap_primitive(other).value)

    def __mul__(self, other):
        return ScrollFloat(self.value * wrap_primitive(other).value)

    def __truediv__(self, other):
        other_val = wrap_primitive(other).value
        if other_val == 0:
            raise ZeroDivisionError("The arcane winds forbid division by zero.")
        return ScrollFloat(self.value / wrap_primitive(other).value)

    def __mod__(self, other):
        return ScrollFloat(self.value % wrap_primitive(other).value)

    def __pow__(self, other):
        return ScrollFloat(self.value ** wrap_primitive(other).value)
    
    def __neg__(self):
        return ScrollFloat(-self.value)

    def cast_to(self, target_type: str):
        if target_type == "float":
            return self
        elif target_type == "int":
            return ScrollInt(int(self.value))
        elif target_type == "bool":
            return ScrollBool(self.value != 0.0)
        elif target_type == "string":
            return ScrollString(str(self.value))
        else:
            raise ValueError(f"Cannot cast float to {target_type}")


class ScrollString(ScrollValue):
    
    type_name = 'str'
    
    def __init__(self, value: str):
        self.value = str(value)
    
    def __add__(self, other):
        return ScrollString(self.value + str(other))

    def cast_to(self, target_type: str):
        if target_type == "string":
            return self
        elif target_type == "bool":
            return ScrollBool(len(self.value) > 0)
        elif target_type == "int":
            try:
                return ScrollInt(int(self.value))
            except ValueError:
                raise ValueError(f"Cannot cast string '{self.value}' to int")
        elif target_type == "float":
            try:
                return ScrollFloat(float(self.value))
            except ValueError:
                raise ValueError(f"Cannot cast string '{self.value}' to float")
        else:
            raise ValueError(f"Cannot cast string to {target_type}")


def wrap_primitive(value):
    if value is None:
        raise TypeError("Cannot wrap a dormant rune (None) into a ScrollValue.")
    
    if isinstance(value, ScrollValue):
        return value
    elif isinstance(value, bool):
        return ScrollBool(value)
    elif isinstance(value, int):
        return ScrollInt(value)
    elif isinstance(value, float):
        return ScrollFloat(value)
    elif isinstance(value, str):
        return ScrollString(value)
    else:
        raise TypeError(f"Unsupported type: {type(value)}")