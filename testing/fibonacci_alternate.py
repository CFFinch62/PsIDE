#!/usr/bin/env python3
"""
Alternative approach to implementing Fibonacci in PsIDE.
This implementation uses arrays to store computed values and avoids the variable update issue.
"""

from pseudocode_interpreter.core.lexer import Lexer
from pseudocode_interpreter.core.parser import Parser
from pseudocode_interpreter.core.interpreter import Interpreter

# Using array-based approach to avoid variable update issues
code = """
REM ============================================================
REM FIBONACCI IMPLEMENTATION - ARRAY-BASED APPROACH
REM ============================================================

FUNCTION fibonacci_array(n)
    REM Handle base cases explicitly
    IF n = 0 THEN
        RETURN 0
    ENDIF
    
    IF n = 1 THEN
        RETURN 1
    ENDIF
    
    REM Use an array to store Fibonacci values
    DECLARE fib : ARRAY[0:20] OF INTEGER
    
    REM Initialize base cases
    fib[0] = 0
    fib[1] = 1
    
    REM Compute Fibonacci numbers using the array
    FOR i ← 2 TO n
        fib[i] = fib[i-1] + fib[i-2]
        PRINT "Computing fib[" + i + "] = " + fib[i-1] + " + " + fib[i-2] + " = " + fib[i]
    NEXT i
    
    RETURN fib[n]
ENDFUNCTION

PRINT "Testing Array-Based Fibonacci"
PRINT "---------------------------"
PRINT "Fibonacci(0) = " + fibonacci_array(0)
PRINT "Fibonacci(1) = " + fibonacci_array(1)
PRINT "Fibonacci(2) = " + fibonacci_array(2)
PRINT "Fibonacci(3) = " + fibonacci_array(3)
PRINT "Fibonacci(4) = " + fibonacci_array(4)
PRINT "Fibonacci(5) = " + fibonacci_array(5)
PRINT "Fibonacci(6) = " + fibonacci_array(6)
PRINT "Fibonacci(7) = " + fibonacci_array(7)
PRINT "Fibonacci(8) = " + fibonacci_array(8)
PRINT "Fibonacci(9) = " + fibonacci_array(9)
PRINT "Fibonacci(10) = " + fibonacci_array(10)
"""

def run_test():
    print("===== ARRAY-BASED FIBONACCI SOLUTION =====")
    
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
