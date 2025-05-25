#!/usr/bin/env python3
"""
Comprehensive test script for the Pseudocode Interpreter.
This script tests all major features of the interpreter to ensure they're working correctly.
"""

import os
import sys
import traceback
from pseudocode_interpreter.core import Lexer, Parser, Interpreter, TokenType, NodeType

# Test categories
TESTS = {
    "Basic": [],
    "Variables": [],
    "Operators": [],
    "ControlFlow": [],
    "Functions": [],
    "Arrays": [],
    "Includes": [],
    "FileIO": [],
    "Math": [],
    "Strings": [],
    "Shell": [],
}

def run_test(name, code, expected_output=None, expected_result=None, category="Basic"):
    """Run a single test and report results."""
    print(f"Testing {name}...")
    print(f"Code:\n{code.strip()}")

    try:
        # Tokenize
        lexer = Lexer(code)
        tokens = lexer.generate_tokens()

        # Parse
        parser = Parser(tokens)
        ast = parser.parse()

        # Interpret
        interpreter = Interpreter()
        result = interpreter.interpret(ast)
        output = interpreter.output_text.rstrip('\n')  # Only strip trailing newlines, not spaces

        print(f"Output: {output}")

        # Check results
        success = True
        if expected_output is not None and output != expected_output:
            print(f"❌ Output mismatch!\nExpected: {expected_output}\nGot: {output}")
            success = False

        if expected_result is not None and result != expected_result:
            print(f"❌ Result mismatch!\nExpected: {expected_result}\nGot: {result}")
            success = False

        if success:
            print(f"✅ Test '{name}' passed!")
            TESTS[category].append((name, True))
        else:
            print(f"❌ Test '{name}' failed!")
            TESTS[category].append((name, False))

        return success

    except Exception as e:
        print(f"❌ Test '{name}' failed with exception: {e}")
        traceback.print_exc()
        TESTS[category].append((name, False))
        return False

def test_basic_functionality():
    """Test basic lexing, parsing, and interpreting."""
    code = """
    x = 5
    y = 10
    result = x + y
    PRINT result
    """
    run_test("Basic Assignment and Output", code, expected_output="15", category="Basic")

    code = """
    // This is a comment
    REM This is also a comment
    PRINT "Hello, World!" // This is an inline comment
    """
    run_test("Comments", code, expected_output="Hello, World!", category="Basic")

def test_variables():
    """Test variable declarations and assignments."""
    code = """
    DECLARE x : INTEGER
    x ← 42
    PRINT x
    """
    run_test("Variable Declaration and Assignment", code, expected_output="42", category="Variables")

    code = """
    test_var ← 42
    test_var2 ← 10
    my_string ← "Hello with underscores!"

    PRINT test_var
    PRINT test_var2
    PRINT my_string
    """
    run_test("Identifiers with Underscores", code,
             expected_output="42\n10\nHello with underscores!", category="Variables")

    code = """
    x = 5
    y = 3.14
    z = "Hello"
    b = TRUE
    c = 'A'

    PRINT x
    PRINT y
    PRINT z
    PRINT b
    PRINT c
    """
    run_test("Different Data Types", code,
             expected_output="5\n3.14\nHello\nTRUE\nA", category="Variables")

def test_operators():
    """Test arithmetic, comparison, and logical operators."""
    code = """
    // Arithmetic operators
    PRINT 5 + 3
    PRINT 5 - 3
    PRINT 5 * 3
    PRINT 5 / 3
    PRINT 5 ^ 2
    PRINT 5 MOD 3
    PRINT 5 DIV 3

    // Comparison operators
    PRINT 5 = 5
    PRINT 5 <> 5
    PRINT 5 < 3
    PRINT 5 > 3
    PRINT 5 <= 5
    PRINT 5 >= 3

    // Logical operators
    PRINT TRUE AND FALSE
    PRINT TRUE OR FALSE
    PRINT NOT TRUE
    """
    expected = "8\n2\n15\n1.6666666666666667\n25\n2\n1\nTRUE\nFALSE\nFALSE\nTRUE\nTRUE\nTRUE\nFALSE\nTRUE\nFALSE"
    run_test("Operators", code, expected_output=expected, category="Operators")

def test_control_flow():
    """Test control flow statements."""
    # IF statement
    code = """
    x = 10
    IF x > 5 THEN
        PRINT "x is greater than 5"
    ELSE
        PRINT "x is not greater than 5"
    ENDIF

    y = 3
    IF y > 5 THEN
        PRINT "y is greater than 5"
    ELSE
        PRINT "y is not greater than 5"
    ENDIF
    """
    expected = "x is greater than 5\ny is not greater than 5"
    run_test("IF-ELSE Statement", code, expected_output=expected, category="ControlFlow")

    # FOR loop
    code = """
    sum = 0
    FOR i ← 1 TO 5
        sum = sum + i
        PRINT i
    NEXT i
    PRINT "Sum: " + sum
    """
    expected = "1\n2\n3\n4\n5\nSum: 15"
    run_test("FOR Loop", code, expected_output=expected, category="ControlFlow")

    # FOR loop with STEP
    code = """
    FOR i ← 10 TO 2 STEP -2
        PRINT i
    NEXT i
    """
    expected = "10\n8\n6\n4\n2"
    run_test("FOR Loop with STEP", code, expected_output=expected, category="ControlFlow")

    # WHILE loop
    code = """
    i = 1
    WHILE i <= 5 DO
        PRINT i
        i = i + 1
    ENDWHILE
    """
    expected = "1\n2\n3\n4\n5"
    run_test("WHILE Loop", code, expected_output=expected, category="ControlFlow")

    # REPEAT loop
    code = """
    i = 1
    REPEAT
        PRINT i
        i = i + 1
    UNTIL i > 5
    """
    expected = "1\n2\n3\n4\n5"
    run_test("REPEAT-UNTIL Loop", code, expected_output=expected, category="ControlFlow")

    # CASE statement
    code = """
    day = 3
    CASE OF day
        1: PRINT "Monday"
        2: PRINT "Tuesday"
        3: PRINT "Wednesday"
        4: PRINT "Thursday"
        5: PRINT "Friday"
        OTHERWISE: PRINT "Weekend"
    ENDCASE
    """
    expected = "Wednesday"
    run_test("CASE Statement", code, expected_output=expected, category="ControlFlow")

def test_functions():
    """Test function and procedure definitions and calls."""
    # Function definition and call
    code = """
    FUNCTION add(a, b) RETURNS INTEGER
        RETURN a + b
    ENDFUNCTION

    PRINT add(5, 3)
    """
    run_test("Function Definition and Call", code, expected_output="8", category="Functions")

    # Alternative function syntax
    code = """
    DEF multiply(a, b) DO
        RETURN a * b
    ENDEF

    PRINT multiply(4, 7)
    """
    run_test("Alternative Function Syntax", code, expected_output="28", category="Functions")

    # Procedure definition and call
    code = """
    PROCEDURE greet(name)
        PRINT "Hello, " + name + "!"
    ENDPROCEDURE

    greet("World")
    """
    run_test("Procedure Definition and Call", code, expected_output="Hello, World!", category="Functions")

    # Recursive function - NOW WORKING!
    code = """
    FUNCTION fibonacci(n)
        IF n <= 0 THEN
            RETURN 0
        ENDIF
        IF n = 1 THEN
            RETURN 1
        ENDIF
        RETURN fibonacci(n - 1) + fibonacci(n - 2)
    ENDFUNCTION

    PRINT fibonacci(5)
    """
    run_test("Recursive Function", code, expected_output="5", category="Functions")

def test_arrays():
    """Test array declarations and operations."""
    code = """
    DECLARE numbers : ARRAY[1:5] OF INTEGER

    FOR i ← 1 TO 5
        numbers[i] = i * 2
    NEXT i

    FOR i ← 1 TO 5
        PRINT numbers[i]
    NEXT i
    """
    expected = "2\n4\n6\n8\n10"
    run_test("One-dimensional Array", code, expected_output=expected, category="Arrays")

    code = """
    DECLARE matrix : ARRAY[1:3, 1:3] OF INTEGER

    // Initialize matrix
    FOR i ← 1 TO 3
        FOR j ← 1 TO 3
            matrix[i, j] = i * j
        NEXT j
    NEXT i

    // Print matrix
    FOR i ← 1 TO 3
        row = ""
        FOR j ← 1 TO 3
            row = row + matrix[i, j] + " "
        NEXT j
        PRINT row
    NEXT i
    """
    expected = "1 2 3 \n2 4 6 \n3 6 9 "
    run_test("Two-dimensional Array", code, expected_output=expected, category="Arrays")

def test_includes():
    """Test the INCLUDE functionality."""
    # Create a temporary file to include
    with open("temp_include.pscd", "w") as f:
        f.write("""
        DEF add(a, b) DO
            RETURN a + b
        ENDEF
        """)

    code = """
    INCLUDE "temp_include.pscd"

    PRINT add(10, 20)
    """

    expected = "30"
    run_test("Include Functionality", code, expected_output=expected, category="Includes")

    # Clean up the temporary file
    import os
    if os.path.exists("temp_include.pscd"):
        os.remove("temp_include.pscd")

def print_summary():
    """Print a summary of all test results."""
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    total_tests = 0
    passed_tests = 0

    for category, tests in TESTS.items():
        if tests:
            print(f"\n{category}:")
            for test_name, passed in tests:
                status = "✅ PASS" if passed else "❌ FAIL"
                print(f"  {status}: {test_name}")
                total_tests += 1
                if passed:
                    passed_tests += 1

    print(f"\n{'-'*60}")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "No tests run")
    print("="*60)

def main():
    """Run all tests."""
    print("Starting Comprehensive Pseudocode Interpreter Tests...")
    print("="*60)

    # Run all test functions
    test_basic_functionality()
    test_variables()
    test_operators()
    test_control_flow()
    test_functions()
    test_arrays()
    test_includes()

    # Print summary
    print_summary()

if __name__ == "__main__":
    main()