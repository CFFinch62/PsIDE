#!/usr/bin/env python3
"""
Final working solution for Fibonacci in PsIDE.
This is the recommended solution to include in your comprehensive test suite.
"""

from pseudocode_interpreter.core.lexer import Lexer
from pseudocode_interpreter.core.parser import Parser
from pseudocode_interpreter.core.interpreter import Interpreter

# The most reliable implementation for PsIDE
code = """
REM ============================================================
REM FIBONACCI IMPLEMENTATION - PRODUCTION VERSION
REM ============================================================

FUNCTION fibonacci(n)
    REM Handle base cases explicitly
    IF n = 0 THEN
        RETURN 0
    ENDIF
    
    IF n = 1 THEN
        RETURN 1
    ENDIF
    
    REM Use the iterative implementation for reliability
    REM with explicit temporary variables at each step
    a = 0
    b = 1
    
    FOR i ← 2 TO n
        REM Use temp variables to ensure correct updates
        temp = a + b
        a = b
        b = temp
    NEXT i
    
    RETURN b
ENDFUNCTION

REM Test with known values
PRINT "Testing Fibonacci Implementation"
PRINT "------------------------------"
PRINT "Fibonacci(0) = " + fibonacci(0) + " (Expected: 0)"
PRINT "Fibonacci(1) = " + fibonacci(1) + " (Expected: 1)"
PRINT "Fibonacci(2) = " + fibonacci(2) + " (Expected: 1)"
PRINT "Fibonacci(3) = " + fibonacci(3) + " (Expected: 2)"
PRINT "Fibonacci(4) = " + fibonacci(4) + " (Expected: 3)"
PRINT "Fibonacci(5) = " + fibonacci(5) + " (Expected: 5)"
PRINT "Fibonacci(6) = " + fibonacci(6) + " (Expected: 8)"
PRINT "Fibonacci(7) = " + fibonacci(7) + " (Expected: 13)"
PRINT "Fibonacci(8) = " + fibonacci(8) + " (Expected: 21)"
PRINT "Fibonacci(9) = " + fibonacci(9) + " (Expected: 34)"
PRINT "Fibonacci(10) = " + fibonacci(10) + " (Expected: 55)"
"""

def run_test():
    print("===== FINAL FIBONACCI SOLUTION =====")
    
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
