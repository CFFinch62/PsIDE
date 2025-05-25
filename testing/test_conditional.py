#!/usr/bin/env python3
"""
Test conditional evaluation in functions.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from pseudocode_interpreter.core.lexer import Lexer
from pseudocode_interpreter.core.parser import Parser
from pseudocode_interpreter.core.interpreter import Interpreter

def test_conditionals():
    """Test conditional evaluation"""
    code = """
    FUNCTION test_condition(n)
        PRINT "test_condition called with n = " + n
        PRINT "Checking n <= 0: " + (n <= 0)
        PRINT "Checking n = 1: " + (n = 1)
        PRINT "Checking n > 1: " + (n > 1)
        
        IF n <= 0 THEN
            PRINT "  Branch: n <= 0"
            RETURN 0
        ENDIF
        
        IF n = 1 THEN
            PRINT "  Branch: n = 1"
            RETURN 1
        ENDIF
        
        PRINT "  Branch: n > 1, should do recursion"
        RETURN 999
    ENDFUNCTION

    PRINT "Testing with n = 3:"
    result = test_condition(3)
    PRINT "Result: " + result
    """
    
    print("Testing conditional evaluation:")
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
    test_conditionals() 