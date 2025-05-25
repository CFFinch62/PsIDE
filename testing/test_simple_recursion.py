#!/usr/bin/env python3
"""
Simple recursion test to debug the issue step by step.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from pseudocode_interpreter.core.lexer import Lexer
from pseudocode_interpreter.core.parser import Parser
from pseudocode_interpreter.core.interpreter import Interpreter

def test_simple_recursion():
    """Test a very simple recursive function"""
    code = """
    FUNCTION test_recursion(n)
        PRINT "Called with n = " + n
        IF n <= 0 THEN
            PRINT "Base case reached"
            RETURN 1
        ENDIF
        PRINT "Making recursive call with " + (n - 1)
        result = test_recursion(n - 1)
        PRINT "Received result: " + result
        final_result = n + result
        PRINT "Returning: " + final_result
        RETURN final_result
    ENDFUNCTION

    PRINT "Starting test with n = 2"
    final = test_recursion(2)
    PRINT "Final result: " + final
    """
    
    print("Testing simple recursion:")
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
    test_simple_recursion() 