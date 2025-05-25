#!/usr/bin/env python3
"""
Test script to diagnose comparison operator issues in the Pseudocode Interpreter.
"""

from pseudocode_interpreter.core.lexer import Lexer
from pseudocode_interpreter.core.parser import Parser
from pseudocode_interpreter.core.interpreter import Interpreter

# Simple test that just compares values
code = """
a = 10
b = 5

PRINT "Testing comparison operators"
PRINT "a = " + a
PRINT "b = " + b

PRINT "a = b: " + (a = b)  REM Should be FALSE
PRINT "a <> b: " + (a <> b)  REM Should be TRUE
PRINT "a > b: " + (a > b)  REM Should be TRUE
PRINT "a < b: " + (a < b)  REM Should be FALSE
PRINT "a >= b: " + (a >= b)  REM Should be TRUE
PRINT "a <= b: " + (a <= b)  REM Should be FALSE

PRINT "Testing IF statements with different values"
x = 5

IF x = 0 THEN
    PRINT "x equals 0"
ELSE
    PRINT "x does not equal 0"
ENDIF

IF x = 1 THEN
    PRINT "x equals 1"
ELSE
    PRINT "x does not equal 1"
ENDIF

IF x = 5 THEN
    PRINT "x equals 5"
ELSE
    PRINT "x does not equal 5"
ENDIF

IF x > 3 THEN
    PRINT "x is greater than 3"
ELSE
    PRINT "x is not greater than 3"
ENDIF

IF x < 3 THEN
    PRINT "x is less than 3"
ELSE
    PRINT "x is not less than 3"
ENDIF
"""

def run_test():
    print("===== COMPARISON OPERATOR TEST =====")
    print(f"Code:\n{code}")
    
    lexer = Lexer(code)
    tokens = lexer.generate_tokens()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    interpreter = Interpreter()
    result = interpreter.interpret(ast)
    
    print("\nOutput:")
    print(interpreter.output_text)

if __name__ == "__main__":
    run_test()
