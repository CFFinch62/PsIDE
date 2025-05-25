#!/usr/bin/env python3
"""
Simplified Fibonacci debug script to isolate the issue.
"""

from pseudocode_interpreter.core.lexer import Lexer
from pseudocode_interpreter.core.parser import Parser
from pseudocode_interpreter.core.interpreter import Interpreter

# Extremely simplified test to diagnose the variable update issue
code = """
REM Test basic variable updates
a = 0
b = 1
result = 0

PRINT "Initial values: a=" + a + ", b=" + b + ", result=" + result

REM First update
result = a + b
PRINT "After first update: result = a + b = " + a + " + " + b + " = " + result

REM Second update
a = b
PRINT "After second update: a = b = " + a

REM Third update
b = result
PRINT "After third update: b = result = " + b

REM Now do another round of updates
result = a + b
a = b
b = result
PRINT "After another round: a=" + a + ", b=" + b + ", result=" + result
"""

def run_test():
    print("===== VARIABLE UPDATE TEST =====")
    
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
