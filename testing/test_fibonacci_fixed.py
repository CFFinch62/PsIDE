#!/usr/bin/env python3
"""
Test script for the Fibonacci function with our fixed recursion handling.
"""

from pseudocode_interpreter.core.lexer import Lexer
from pseudocode_interpreter.core.parser import Parser
from pseudocode_interpreter.core.interpreter import Interpreter

# Define a recursive Fibonacci function in pseudocode
fibonacci_code = """
FUNCTION fibonacci(n)
    IF n <= 1 THEN
        RETURN n
    ENDIF
    
    RETURN fibonacci(n - 1) + fibonacci(n - 2)
ENDFUNCTION

PRINT "Testing Recursive Fibonacci Function"
PRINT "-----------------------------------"
FOR i ← 0 TO 10
    PRINT "Fibonacci(" + i + ") = " + fibonacci(i)
NEXT i
"""

# Define an iterative Fibonacci function for comparison
iterative_fibonacci_code = """
FUNCTION fibonacci(n)
    IF n <= 1 THEN
        RETURN n
    ENDIF
    
    a ← 0
    b ← 1
    result ← 0
    
    FOR i ← 2 TO n
        result ← a + b
        a ← b
        b ← result
    NEXT i
    
    RETURN result
ENDFUNCTION

PRINT "Testing Iterative Fibonacci Function"
PRINT "-----------------------------------"
FOR i ← 0 TO 10
    PRINT "Fibonacci(" + i + ") = " + fibonacci(i)
NEXT i
"""

def run_test(code, description):
    print(f"\n===== {description} =====\n")
    
    # Parse and execute the code
    lexer = Lexer(code)
    tokens = lexer.generate_tokens()
    parser = Parser(tokens)
    ast = parser.parse()
    
    interpreter = Interpreter()
    result = interpreter.interpret(ast)
    
    print(interpreter.output_text)
    
    # Check results against expected values
    expected_fibonacci = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    
    # Extract Fibonacci values from output
    lines = interpreter.output_text.strip().split('\n')[2:]  # Skip header lines
    actual_values = []
    
    for line in lines:
        if line.startswith("Fibonacci("):
            value = line.split("=")[1].strip()
            actual_values.append(int(value))
    
    # Compare with expected values
    all_correct = True
    for i, (expected, actual) in enumerate(zip(expected_fibonacci, actual_values)):
        if expected != actual:
            print(f"❌ Error: Fibonacci({i}) = {actual}, expected {expected}")
            all_correct = False
    
    if all_correct:
        print(f"\n✅ SUCCESS: All Fibonacci values match expected results!")
    else:
        print(f"\n❌ FAILURE: Some Fibonacci values don't match expected results.")
    
    return all_correct

if __name__ == "__main__":
    # Test both implementations
    recursive_success = run_test(fibonacci_code, "RECURSIVE FIBONACCI IMPLEMENTATION")
    iterative_success = run_test(iterative_fibonacci_code, "ITERATIVE FIBONACCI IMPLEMENTATION")
    
    if recursive_success and iterative_success:
        print("\n🎉 OVERALL SUCCESS: Both implementations work correctly! The recursion issue is fixed!")
    else:
        print("\n⚠️ PARTIAL SUCCESS: Not all implementations work correctly.")
