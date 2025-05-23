"""
All keywords contained in ScrollScript
"""

# ----- Variables -----
VAR_DECLARATION = "rune"
CAST_EXPR = "transmute"
CONST_DECLARATION = "sealed"
VAR_TO_CONST = "seal"

# ----- Data Types -----
INTEGER = "int"
FLOAT = "float"
STRING = "string"
BOOLEAN = "bool"

# ----- Control Flow -----
IF = "foretell"
ELIF = "shift"
ELSE = "resolve"
MAYBE = "mayhaps"
FOR = "cycle"
UNTIL = "lest"
AD = "AD"
INFINITUM = "infinitum"
IN = "betwixt"
BREAK = "shatter"
CONTINUE = "persist"

# ----- Functions -----
FUNC_DEF = "incantation"
FUNC_CALL = "cast"
RETURN = "proclaim"

# ----- I/O -----
PRINT = "reveal"
INPUT = "listen"

# ----- Booleans -----
TRUE = "Truthsung"
FALSE = "Falsehood"

# ----- Standard Features -----
DELETE = "dispel"
LENGTH = "measure"

# ----- Collections -----
ARRAY = "tome"
DICT = "grimoire"

# ----- Unique Features -----
FROM = "from"
DAYS = "days"
OF = "of"
YORE = "yore"

# ----- Full List -----
KEYWORDS_LIST = {
    value
    for name, value in globals().items()
    if name.isupper()
}