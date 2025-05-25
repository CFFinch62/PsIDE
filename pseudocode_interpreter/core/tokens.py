from enum import Enum, auto

# Token Types
class TokenType(Enum):
    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    POW = auto()
    LPAREN = auto()
    RPAREN = auto()
    EQ = auto()
    IDENTIFIER = auto()
    NONE = auto()
    EE = auto()  # equals equals (==)
    NE = auto()  # not equals (!=)
    LT = auto()  # less than
    GT = auto()  # greater than
    LTE = auto() # less than or equal to
    GTE = auto() # greater than or equal to
    KEYWORD = auto()
    COMMA = auto()
    STRING = auto()
    LSQBRACKET = auto()
    RSQBRACKET = auto()
    SEP = auto()  # Block separator - semicolon
    NL = auto()   # Newline - separate instructions
    CASE = auto()
    CASE_ITEM = auto()
    CASE_OTHERWISE = auto()
    COLON = auto()  # Colon for CASE statements
    EOF = auto()    # End of file

# Token class
class Token:
    def __init__(self, type_: TokenType, value=None, name=None):
        self.type = type_
        self.value = value
        self.name = name

    def __repr__(self):
        if self.value is not None:
            return f"{self.type.name}:{self.value}"
        elif self.name is not None:
            return f"{self.type.name}:{self.name}"
        else:
            return f"{self.type.name}"