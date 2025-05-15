'''
This file contains all keywords in ScrollScript
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

KEYWORDS_LIST = {
    value
    for name, value in globals().items()
    if name.isupper()
}