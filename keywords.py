'''
All keywords contained in ScrollScript
'''

# ----- Variables -----
VAR_DECLARATION = "rune"
CAST_EXPR = "transmute"
CONST_DECLARATION = "sealed"

# ----- Data Types -----
INTEGER = 'int'
FLOAT = 'float'
STRING = 'string'
BOOLEAN = 'bool'

# ----- I/O -----
PRINT = "chant"
INPUT = "channel"

# ----- Booleans -----
TRUE = "Truthsung"
FALSE = "Falsehood"

# ----- Standard Features -----
DELETE = "dispel"

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