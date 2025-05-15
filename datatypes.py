from keywords import INTEGER, FLOAT, STRING, BOOLEAN, TRUE, FALSE

class ScrollValue:
    def cast_to(self, target_type: str):
        raise NotImplementedError("Casting not implemented for this type.")

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {str(self)}>"


class ScrollBool(ScrollValue):
    
    type_name = BOOLEAN
    
    def __init__(self, value):
        if isinstance(value, str):
            self.value = value == TRUE
        else:
            self.value = bool(value)

    def __bool__(self):
        return self.value

    def __str__(self):
        return TRUE if self.value else FALSE

    def __repr__(self):
        return f"<ScrollBool: {TRUE if self.value else FALSE}>"

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
        if target_type == BOOLEAN:
            return self
        elif target_type == INTEGER:
            return ScrollInt(1 if self.value else 0)
        elif target_type == FLOAT:
            return ScrollFloat(1.0 if self.value else 0.0)
        elif target_type == STRING:
            return ScrollString(str(self))
        else:
            raise ValueError(f"Cannot cast {BOOLEAN} to {target_type}")


class ScrollInt(ScrollValue):
    
    type_name = INTEGER
    
    def __init__(self, value: int):
        self.value = int(value)
        
    def __add__(self, other):
        other_val = wrap_primitive(other).value
        if isinstance(other_val, str):
            return ScrollString(str(self.value) + other_val)
        return ScrollInt(self.value + other_val)

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
    
    def __str__(self):
        return str(self.value)

    def cast_to(self, target_type: str):
        if target_type == INTEGER:
            return self
        elif target_type == FLOAT:
            return ScrollFloat(float(self.value))
        elif target_type == BOOLEAN:
            return ScrollBool(self.value != 0)
        elif target_type == STRING:
            return ScrollString(str(self.value))
        else:
            raise ValueError(f"Cannot cast {INTEGER} to {target_type}")


class ScrollFloat(ScrollValue):
    
    type_name = FLOAT
    
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
    
    def __str__(self):
        return str(self.value)

    def cast_to(self, target_type: str):
        if target_type == FLOAT:
            return self
        elif target_type == INTEGER:
            return ScrollInt(int(self.value))
        elif target_type == BOOLEAN:
            return ScrollBool(self.value != 0.0)
        elif target_type == STRING:
            return ScrollString(str(self.value))
        else:
            raise ValueError(f"Cannot cast {FLOAT} to {target_type}")


class ScrollString(ScrollValue):
    
    type_name = 'str'
    
    def __init__(self, value: str):
        self.value = str(value)
    
    def __add__(self, other):
        return ScrollString(self.value + str(other))

    def cast_to(self, target_type: str):
        if target_type == STRING:
            return self
        elif target_type == BOOLEAN:
            return ScrollBool(len(self.value) > 0)
        elif target_type == INTEGER:
            try:
                return ScrollInt(int(self.value))
            except ValueError:
                raise ValueError(f"Cannot cast {STRING} '{self.value}' to {INTEGER}")
        elif target_type == FLOAT:
            try:
                return ScrollFloat(float(self.value))
            except ValueError:
                raise ValueError(f"Cannot cast {STRING} '{self.value}' to {FLOAT}")
        else:
            raise ValueError(f"Cannot cast {STRING} to {target_type}")


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