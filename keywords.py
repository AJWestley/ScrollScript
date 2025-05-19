'''
All keywords contained in ScrollScript
'''

# ----- Variables -----
VAR_DECLARATION = "rune"
CAST_EXPR = "transmute"
CONST_DECLARATION = "sealed"
VAR_TO_CONST = "seal"

# ----- Data Types -----
INTEGER = 'int'
FLOAT = 'float'
STRING = 'string'
BOOLEAN = 'bool'

# ----- Control Flow -----
IF = 'foretell'
ELIF = 'shift'
ELSE = 'resolve'

# ----- I/O -----
PRINT = "reveal"
INPUT = "channel"

# ----- Booleans -----
TRUE = "Truthsung"
FALSE = "Falsehood"

# ----- Standard Features -----
DELETE = "dispel"
LENGTH = "measure"

# ----- Unique Features -----
FROM = "from"
DAYS = "days"
OF = "of"
YORE = "of"

# ----- Full List -----
KEYWORDS_LIST = {
    value
    for name, value in globals().items()
    if name.isupper()
}