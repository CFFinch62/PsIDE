#!/usr/bin/env python3
"""
Fibonacci solution for the PsIDE using an iterative approach.
This provides a more efficient and reliable implementation that avoids recursion issues.
"""

from pseudocode_interpreter.core.lexer import Lexer
from pseudocode_interpreter.core.parser import Parser
from pseudocode_interpreter.core.interpreter import Interpreter

# Iterative Fibonacci implementation
code = """
REM Iterative Fibonacci implementation 
REM This avoids the complex recursion issues and is more efficient

FUNCTION fibonacci_iterative(n)
    REM Handle base cases
    IF n <= 0 THEN
        RETURN 0
    ENDIF
    
    IF n = 1 THEN
        RETURN 1
    ENDIF
    
    REM Initialize variables for iteration
    a = 0
    b = 1
    result = 0
    
    REM Calculate Fibonacci using iteration
    FOR i ← 2 TO n
        result = a + b
        a = b
        b = result
    NEXT i
    
    RETURN result
ENDFUNCTION

REM Test the Fibonacci implementation
PRINT "Fibonacci Sequence (0-10):"
FOR i ← 0 TO 10
    PRINT "Fibonacci(" + i + ") = " + fibonacci_iterative(i)
NEXT i
"""

def run_test():
    print("===== FIBONACCI SOLUTION =====")
    
    lexer = Lexer(code)
    tokens = lexer.generate_tokens()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    interpreter = Interpreter()
    result = interpreter.interpret(ast)
    
    print("\nOutput:")
    print(interpreter.output_text)
    
    # Verify the results match the expected Fibonacci sequence
    expected = ["Fibonacci(0) = 0",
                "Fibonacci(1) = 1", 
                "Fibonacci(2) = 1",
                "Fibonacci(3) = 2", 
                "Fibonacci(4) = 3",
                "Fibonacci(5) = 5", 
                "Fibonacci(6) = 8",
                "Fibonacci(7) = 13", 
                "Fibonacci(8) = 21",
                "Fibonacci(9) = 34", 
                "Fibonacci(10) = 55"]
                
    actual = interpreter.output_text.strip().split('\n')[1:]  # Skip the first line (header)
    
    success = all(a.strip() == e for a, e in zip(actual, expected))
    
    if success:
        print("\n✅ SUCCESS: Fibonacci implementation works correctly!")
    else:
        print("\n❌ FAILURE: Fibonacci results don't match expected values.")
        
    return success

if __name__ == "__main__":
    run_test()
