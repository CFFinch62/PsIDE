#!/usr/bin/env python3
"""
Test equality operator specifically.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from pseudocode_interpreter.core.lexer import Lexer
from pseudocode_interpreter.core.parser import Parser
from pseudocode_interpreter.core.interpreter import Interpreter

def test_equality():
    """Test equality operator"""
    code = """
    n = 3
    PRINT "n = " + n
    PRINT "1 = " + 1
    PRINT "n = 1 evaluates to: " + (n = 1)
    PRINT "n = 3 evaluates to: " + (n = 3)
    PRINT "3 = 3 evaluates to: " + (3 = 3)
    PRINT "3 = 1 evaluates to: " + (3 = 1)
    """
    
    print("Testing equality operator:")
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
    test_equality() 