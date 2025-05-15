'''
All keywords contained in ScrollScript
'''

VAR_DECLARATION = "rune"
PRINT = "chant"
INPUT = "channel"
FROM = "from"
DAYS = "days"
OF = "of"
YORE = "of"
TRUE = "Truthsung"
FALSE = "Falsehood"
CAST_EXPR = "transmute"
INTEGER = 'int'
FLOAT = 'float'
STRING = 'string'
BOOLEAN = 'bool'

KEYWORDS_LIST = {
    value
    for name, value in globals().items()
    if name.isupper()
}