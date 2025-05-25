#!/usr/bin/env python3
"""
Test script specifically for recursive functions in the Pseudocode Interpreter.
"""

from pseudocode_interpreter.core.lexer import Lexer
from pseudocode_interpreter.core.parser import Parser
from pseudocode_interpreter.core.interpreter import Interpreter
from pseudocode_interpreter.core.values import Variable

def run_test(code, expected_output=None):
    """Run a test and report results."""
    lexer = Lexer(code)
    tokens = lexer.generate_tokens()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    interpreter = Interpreter()
    result = interpreter.interpret(ast)
    
    print("===== TEST: RECURSIVE FUNCTION =====")
    print("Code:")
    print(code)
    print("\nOutput:")
    print(interpreter.output_text)
    
    if expected_output is not None:
        success = interpreter.output_text.strip() == expected_output.strip()
        if success:
            print("\n✅ TEST PASSED!")
        else:
            print("\n❌ TEST FAILED!")
            print("Expected output:")
            print(expected_output)
    
    return interpreter.output_text

# Test factorial recursion
factorial_code = """
FUNCTION factorial(n)
    IF n <= 1 THEN
        RETURN 1
    ELSE
        RETURN n * factorial(n - 1)
    ENDIF
ENDFUNCTION

PRINT "Factorial of 5 is: " + factorial(5)
"""

# Test Fibonacci recursion
fibonacci_code = """
FUNCTION fibonacci(n)
    IF n <= 0 THEN
        RETURN 0
    ENDIF
    IF n = 1 THEN
        RETURN 1
    ENDIF
    RETURN fibonacci(n - 1) + fibonacci(n - 2)
ENDFUNCTION

FOR i ← 0 TO 10
    PRINT "Fibonacci(" + i + ") = " + fibonacci(i)
NEXT i
"""

if __name__ == "__main__":
    print("\n\n======= TESTING RECURSIVE FUNCTIONS =======\n")
    
    # Test factorial
    print("\n=== FACTORIAL TEST ===")
    factorial_expected = "Factorial of 5 is: 120"
    factorial_output = run_test(factorial_code, factorial_expected)
    
    # Test fibonacci
    print("\n=== FIBONACCI TEST ===")
    fibonacci_expected = """Fibonacci(0) = 0
Fibonacci(1) = 1
Fibonacci(2) = 1
Fibonacci(3) = 2
Fibonacci(4) = 3
Fibonacci(5) = 5
Fibonacci(6) = 8
Fibonacci(7) = 13
Fibonacci(8) = 21
Fibonacci(9) = 34
Fibonacci(10) = 55"""
    fibonacci_output = run_test(fibonacci_code, fibonacci_expected)
    
    # Report success
    print("\n======= RECURSION TESTING COMPLETE =======")
