from enum import Enum, auto

# Node Types
class NodeType(Enum):
    NULL = auto()
    NUMBER = auto()
    ADD = auto()
    SUBTRACT = auto()
    DIVIDE = auto()
    MULTIPLY = auto()
    POWER = auto()
    PLUS = auto()     # Unary plus
    MINUS = auto()    # Unary minus
    VAR_ASSIGN = auto()
    VAR_ACCESS = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    GT = auto()
    LT = auto()
    GTE = auto()
    LTE = auto()
    EE = auto()
    NE = auto()
    IF = auto()
    IF_ELSE = auto()
    FOR = auto()
    WHILE = auto()
    PRINT = auto()
    READ = auto()
    INPUT = auto()
    STRING = auto()
    LIST = auto()
    BLOCK = auto()
    DEF = auto()
    ARGS = auto()
    ARG = auto()
    FUNCTION_CALL = auto()
    RETURN = auto()
    INCLUDE = auto()
    CASE = auto()
    CASE_ITEM = auto()
    CASE_OTHERWISE = auto()
    REPEAT_UNTIL = auto()
    DECLARE = auto()
    MODULO = auto()
    INT_DIVIDE = auto()
    BOOLEAN = auto()
    ARRAY_ACCESS = auto()
    ARRAY_ASSIGN = auto()

# Node class
class Node:
    def __init__(self, type_: NodeType, value=None, name=None, nodes=None):
        self.type = type_
        self.value = value
        self.name = name
        self.nodes = nodes or []

    def __repr__(self):
        result = f"{self.type.name}"

        if self.value is not None:
            result += f":{self.value}"
        if self.name is not None:
            result += f":{self.name}"

        if self.nodes:
            result += f"[{', '.join(str(node) for node in self.nodes)}]"

        return result