#!/usr/bin/env python3
"""
Step-by-step trace for Fibonacci function to diagnose recursion issues.
"""

from pseudocode_interpreter.core.lexer import Lexer
from pseudocode_interpreter.core.parser import Parser
from pseudocode_interpreter.core.interpreter import Interpreter
from pseudocode_interpreter.core.values import Variable, Number

# Let's try a completely different approach using an iterative solution instead of recursion
code = """
FUNCTION fibonacci_iterative(n)
    PRINT "Computing fibonacci for n = " + n
    
    REM Base cases
    IF n = 0 THEN
        PRINT "Base case: n = 0, returning 0"
        RETURN 0
    ENDIF
    
    IF n = 1 THEN
        PRINT "Base case: n = 1, returning 1"
        RETURN 1
    ENDIF
    
    REM Initialize variables for iteration
    PRINT "Using iteration to compute fibonacci(" + n + ")"
    a = 0
    b = 1
    
    REM Iterate to calculate fibonacci
    FOR i ← 2 TO n
        PRINT "Iteration " + i + ": a = " + a + ", b = " + b
        temp = a + b
        a = b
        b = temp
        PRINT "New value: " + b
    NEXT i
    
    PRINT "Final fibonacci(" + n + ") = " + b
    RETURN b
ENDFUNCTION

PRINT "Starting Fibonacci calculation (iterative)"
result = fibonacci_iterative(10)
PRINT "Final result: " + result
"""

def run_trace():
    print("===== FIBONACCI STEP-BY-STEP TRACE =====")
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
    run_trace()
