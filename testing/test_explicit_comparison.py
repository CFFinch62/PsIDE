#!/usr/bin/env python3
"""
Test using explicit double equals for Fibonacci.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from pseudocode_interpreter.core.lexer import Lexer
from pseudocode_interpreter.core.parser import Parser
from pseudocode_interpreter.core.interpreter import Interpreter

def test_explicit_fibonacci():
    """Test Fibonacci with explicit == operators"""
    code = """
    FUNCTION fibonacci(n)
        PRINT "fibonacci(" + n + ") called"
        IF n <= 0 THEN
            PRINT "  returning 0 (base case)"
            RETURN 0
        ENDIF
        IF n == 1 THEN
            PRINT "  returning 1 (base case)"
            RETURN 1
        ENDIF
        PRINT "  making recursive calls for " + (n-1) + " and " + (n-2)
        fib_n_1 = fibonacci(n - 1)
        PRINT "  fibonacci(" + (n-1) + ") returned " + fib_n_1
        fib_n_2 = fibonacci(n - 2)
        PRINT "  fibonacci(" + (n-2) + ") returned " + fib_n_2
        result = fib_n_1 + fib_n_2
        PRINT "  fibonacci(" + n + ") returning " + result
        RETURN result
    ENDFUNCTION

    PRINT "Testing fibonacci(3) with explicit ==:"
    result = fibonacci(3)
    PRINT "Final result: " + result
    """
    
    print("Testing Fibonacci function with explicit == operators:")
    print(code)
    
    lexer = Lexer(code)
    tokens = lexer.generate_tokens()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    interpreter = Interpreter()
    result = interpreter.interpret(ast)
    
    print("\nOutput:")
    print(interpreter.output_text)

if __name__ == "__main__":
    test_explicit_fibonacci() 