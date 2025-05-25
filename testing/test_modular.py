#!/usr/bin/env python3
"""
Test script to verify the modular pseudocode interpreter works.
"""

from pseudocode_interpreter.core import Lexer, Parser, Interpreter

def test_basic_functionality():
    """Test basic lexing, parsing, and interpreting."""
    code = """
    x = 5
    y = 10
    result = x + y
    PRINT result
    """
    
    print("Testing basic functionality...")
    print(f"Code: {code.strip()}")
    
    try:
        # Tokenize
        lexer = Lexer(code)
        tokens = lexer.generate_tokens()
        print(f"Tokens generated: {len(tokens)}")
        
        # Parse
        parser = Parser(tokens)
        ast = parser.parse()
        print(f"AST created: {ast.type}")
        
        # Interpret
        interpreter = Interpreter()
        result = interpreter.interpret(ast)
        print(f"Output: {interpreter.output_text.strip()}")
        print(f"Result: {result}")
        
        print("✅ Basic functionality test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_imports():
    """Test that all modules can be imported."""
    print("\nTesting imports...")
    try:
        from pseudocode_interpreter.core import (
            Token, TokenType, Lexer, Node, NodeType, Parser,
            Variable, Number, String, List, Function, SymbolTable, Interpreter
        )
        print("✅ Core module imports successful!")
        
        from pseudocode_interpreter.gui import (
            PseudocodeIDE, PseudocodeHighlighter, InputDialog
        )
        print("✅ GUI module imports successful!")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

if __name__ == "__main__":
    print("Pseudocode Interpreter Modular Structure Test")
    print("=" * 50)
    
    import_success = test_imports()
    basic_success = test_basic_functionality()
    
    if import_success and basic_success:
        print("\n🎉 All tests passed! The modular structure is working correctly.")
    else:
        print("\n💥 Some tests failed. Please check the error messages above.") 