#!/usr/bin/env python3
"""
Debug script specifically for the Fibonacci recursion issue.
This will add debug output to help trace the problem.
"""

from pseudocode_interpreter.core.lexer import Lexer
from pseudocode_interpreter.core.parser import Parser
from pseudocode_interpreter.core.interpreter import Interpreter
from pseudocode_interpreter.core.values import Variable, Number

# Modify the interpreter to include debug output
class DebugInterpreter(Interpreter):
    def __init__(self):
        super().__init__()
        self.debug_indent = 0
        
    def visit_function_call(self, node):
        """Overridden visit_function_call with debug output"""
        func_name = node.name
        
        # Add debug output
        indent = "  " * self.debug_indent
        print(f"{indent}Calling {func_name} with args:", end=" ")
        
        # Get argument values for debug
        arg_values = []
        if node.nodes:
            for arg_node in node.nodes:
                value = self.visit(arg_node)
                print(f"{value}", end=", ")
                arg_values.append(value)
        print()
        
        # Check recursion depth
        if self.recursion_depth >= self.max_recursion_depth:
            raise Exception(f"Maximum recursion depth exceeded ({self.max_recursion_depth})")

        if not self.current_symbol_table.has(func_name):
            raise Exception(f"Function '{func_name}' not defined")

        function_var = self.current_symbol_table.get(func_name)

        if function_var.type != "function":
            raise Exception(f"'{func_name}' is not a function")

        function = function_var.value

        # Increment recursion depth and debug indent
        self.recursion_depth += 1
        self.debug_indent += 1

        try:
            # Create a completely new symbol table with no parent
            function_symbol_table = self.global_symbol_table.create_child_table()
            
            # Add the function to its own scope to enable recursion
            function_symbol_table.set(func_name, function_var)

            # Process arguments
            if function.args_node:
                arg_nodes = function.args_node.nodes

                if len(arg_nodes) != len(arg_values):
                    raise Exception(f"Function '{func_name}' expects {len(arg_nodes)} arguments, got {len(arg_values)}")

                # Set arguments in the function's symbol table
                for i, arg_node in enumerate(arg_nodes):
                    arg_name = arg_node.name
                    function_symbol_table.set(arg_name, arg_values[i])

            # Save the current symbol table and return value
            old_symbol_table = self.current_symbol_table
            old_return_value = self.return_value
            
            # Switch to the function's symbol table
            self.current_symbol_table = function_symbol_table
            # Clear any previous return value
            self.return_value = None

            # Execute the function body
            self.visit(function.body_node)
            
            # Get return value - either from explicit RETURN or function return expression
            if self.return_value is not None:
                # An explicit RETURN statement was executed
                return_value = self.return_value
                # Clear the return value to not affect outer scope
                self.return_value = None
            else:
                # Use the function's return expression
                return_value = self.visit(function.return_node)

            # Restore previous state
            self.current_symbol_table = old_symbol_table
            self.return_value = old_return_value
            
            # Debug output for return value
            print(f"{indent}Return from {func_name}: {return_value}")

            return return_value
        finally:
            # Always decrement recursion depth and debug indent
            self.recursion_depth -= 1
            self.debug_indent -= 1
            
    def visit_add(self, node):
        """Overridden visit_add with debug output"""
        left = self.visit(node.nodes[0])
        right = self.visit(node.nodes[1])
        
        indent = "  " * self.debug_indent
        print(f"{indent}Adding: {left} + {right}")
        
        # Ensure both operands are Variable instances
        if not isinstance(left, Variable):
            left = Variable(left)
        if not isinstance(right, Variable):
            right = Variable(right)

        # Handle different type combinations
        if left.type == "number" and right.type == "number":
            # For numeric addition, make sure we extract the numeric values properly
            left_value = left.value.value if hasattr(left.value, 'value') else 0
            right_value = right.value.value if hasattr(right.value, 'value') else 0
            result = Variable(left_value + right_value)
            print(f"{indent}Result: {result}")
            return result
        elif left.type == "string" and right.type == "string":
            result = Variable(left.value.value + right.value.value)
            print(f"{indent}Result: {result}")
            return result
        elif left.type == "list" and right.type == "list":
            result = Variable(left.value.values + right.value.values)
            print(f"{indent}Result: {result}")
            return result
        else:
            # Convert to string for mixed types
            result = Variable(str(left) + str(right))
            print(f"{indent}Result: {result}")
            return result

# Run a simplified Fibonacci test
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

PRINT fibonacci(3)
"""

if __name__ == "__main__":
    print("===== DEBUGGING FIBONACCI RECURSION =====")
    print(f"Code:\n{fibonacci_code}")
    
    lexer = Lexer(fibonacci_code)
    tokens = lexer.generate_tokens()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    interpreter = DebugInterpreter()
    result = interpreter.interpret(ast)
    
    print("\nOutput:")
    print(interpreter.output_text)
