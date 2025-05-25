import sys
import os
from PyQt6.QtWidgets import QDialog
from .ast_nodes import Node, NodeType
from .values import Variable, Number, String, List, Function, SymbolTable

# Interpreter class
class Interpreter:
    def __init__(self, symbol_table=None):
        self.global_symbol_table = symbol_table or SymbolTable()
        self.current_symbol_table = self.global_symbol_table
        self.return_value = None
        self.output_text = ""
        self.cwd = ""
        self.recursion_depth = 0
        self.max_recursion_depth = 1000

        # Initialize global variables
        self._init_globals()

    def _init_globals(self):
        """Initialize global variables like TRUE, FALSE, OS, etc."""
        self.global_symbol_table.set("TRUE", Variable(1.0))
        self.global_symbol_table.set("FALSE", Variable(0.0))

        # Set OS: 0=Windows, 1=Mac, 2=Linux, 3=Unix, 4=Posix
        if sys.platform.startswith('win'):
            self.global_symbol_table.set("OS", Variable(0.0))
        elif sys.platform.startswith('darwin'):
            self.global_symbol_table.set("OS", Variable(1.0))
        elif sys.platform.startswith('linux'):
            self.global_symbol_table.set("OS", Variable(2.0))
        elif sys.platform.startswith(('freebsd', 'netbsd', 'openbsd')):
            self.global_symbol_table.set("OS", Variable(3.0))
        elif os.name == 'posix':
            self.global_symbol_table.set("OS", Variable(4.0))

    def interpret(self, node):
        """Interpret an AST node and return the result"""
        self.output_text = ""
        return self.visit(node)

    def visit(self, node):
        """Visit a node and call the appropriate method based on node type"""
        method_name = f'visit_{node.type.name.lower()}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        """Called when there's no method for the node type"""
        raise Exception(f"No visit_{node.type.name.lower()} method defined")

    def visit_null(self, node):
        """Visit a null node, which represents nothing"""
        return Variable()

    def visit_number(self, node):
        """Visit a number node"""
        return Variable(node.value)

    def visit_string(self, node):
        """Visit a string node"""
        return Variable(node.name)

    def visit_boolean(self, node):
        """Visit a boolean node"""
        # Store boolean values as numbers but display them as TRUE/FALSE
        value = 1.0 if node.name == 'TRUE' else 0.0
        var = Variable(value)
        # Add a special flag to indicate this is a boolean
        var.is_boolean = True
        var.boolean_name = node.name
        return var

    def visit_list(self, node):
        """Visit a list node"""
        elements = []
        for element_node in node.nodes:
            elements.append(self.visit(element_node))

        return Variable(elements)

    def visit_var_access(self, node):
        """Visit a variable access node"""
        var_name = node.name

        if not self.current_symbol_table.has(var_name):
            raise Exception(f"Variable '{var_name}' not defined")

        return self.current_symbol_table.get(var_name)

    def visit_var_assign(self, node):
        """Visit a variable assignment node"""
        var_name = node.name
        value = self.visit(node.nodes[0])

        self.current_symbol_table.set(var_name, value)
        return value

    def visit_add(self, node):
        """Visit an addition node"""
        left = self.visit(node.nodes[0])
        right = self.visit(node.nodes[1])
        
        # Ensure both operands are Variable instances
        if not isinstance(left, Variable):
            left = Variable(left)
        if not isinstance(right, Variable):
            right = Variable(right)

        # Handle different type combinations
        if left.type == "number" and right.type == "number":
            # For numeric addition, make sure we extract the numeric values properly
            # This is critical for recursive function results
            left_value = left.value.value if hasattr(left.value, 'value') else 0
            right_value = right.value.value if hasattr(right.value, 'value') else 0
            return Variable(left_value + right_value)
        elif left.type == "string" and right.type == "string":
            return Variable(left.value.value + right.value.value)
        elif left.type == "list" and right.type == "list":
            return Variable(left.value.values + right.value.values)
        else:
            # Convert to string for mixed types
            return Variable(str(left) + str(right))

    def visit_subtract(self, node):
        """Visit a subtraction node"""
        left = self.visit(node.nodes[0])
        right = self.visit(node.nodes[1])

        if left.type != "number" or right.type != "number":
            raise Exception("Cannot subtract non-number values")

        return Variable(left.value.value - right.value.value)

    def visit_multiply(self, node):
        """Visit a multiplication node"""
        left = self.visit(node.nodes[0])
        right = self.visit(node.nodes[1])

        # Handle different type combinations
        if left.type == "number" and right.type == "number":
            return Variable(left.value.value * right.value.value)
        elif left.type == "string" and right.type == "number":
            # Repeat string
            return Variable(left.value.value * int(right.value.value))
        elif left.type == "number" and right.type == "string":
            # Repeat string
            return Variable(right.value.value * int(left.value.value))
        elif left.type == "list" and right.type == "number":
            # Repeat list
            return Variable(left.value.values * int(right.value.value))
        else:
            raise Exception("Invalid operands for multiplication")

    def visit_divide(self, node):
        """Visit a division node"""
        left = self.visit(node.nodes[0])
        right = self.visit(node.nodes[1])

        if left.type != "number" or right.type != "number":
            raise Exception("Cannot divide non-number values")

        if right.value.value == 0:
            raise Exception("Division by zero")

        return Variable(left.value.value / right.value.value)

    def visit_power(self, node):
        """Visit a power node"""
        left = self.visit(node.nodes[0])
        right = self.visit(node.nodes[1])

        if left.type != "number" or right.type != "number":
            raise Exception("Cannot perform power operation on non-number values")

        return Variable(left.value.value ** right.value.value)

    def visit_modulo(self, node):
        """Visit a modulo node"""
        left = self.visit(node.nodes[0])
        right = self.visit(node.nodes[1])

        if left.type != "number" or right.type != "number":
            raise Exception("Cannot perform modulo operation on non-number values")

        if right.value.value == 0:
            raise Exception("Modulo by zero")

        return Variable(left.value.value % right.value.value)

    def visit_int_divide(self, node):
        """Visit an integer division node"""
        left = self.visit(node.nodes[0])
        right = self.visit(node.nodes[1])

        if left.type != "number" or right.type != "number":
            raise Exception("Cannot perform integer division on non-number values")

        if right.value.value == 0:
            raise Exception("Division by zero")

        return Variable(int(left.value.value // right.value.value))

    def visit_plus(self, node):
        """Visit a unary plus node"""
        value = self.visit(node.nodes[0])

        if value.type != "number":
            raise Exception("Cannot apply unary plus to non-number value")

        return value  # No change needed for unary plus

    def visit_minus(self, node):
        """Visit a unary minus node"""
        value = self.visit(node.nodes[0])

        if value.type != "number":
            raise Exception("Cannot apply unary minus to non-number value")

        return Variable(-value.value.value)

    def visit_ee(self, node):
        """Visit an equals equals node"""
        left = self.visit(node.nodes[0])
        right = self.visit(node.nodes[1])
        
        # Ensure both are Variable instances
        if not isinstance(left, Variable):
            left = Variable(left)
        if not isinstance(right, Variable):
            right = Variable(right)
        
        # Special case for equality comparison
        if left.type == "number" and right.type == "number":
            # Extract the actual numeric values for comparison
            left_value = left.value.value if hasattr(left.value, 'value') else 0
            right_value = right.value.value if hasattr(right.value, 'value') else 0
            is_equal = left_value == right_value
        elif left.type == "string" and right.type == "string":
            left_value = left.value.value if hasattr(left.value, 'value') else ""
            right_value = right.value.value if hasattr(right.value, 'value') else ""
            is_equal = left_value == right_value
        else:
            # Different types are never equal
            is_equal = False

        result = Variable(1.0 if is_equal else 0.0)
        result.is_boolean = True
        result.boolean_name = "TRUE" if is_equal else "FALSE"
        return result

    def visit_ne(self, node):
        """Visit a not equals node"""
        left = self.visit(node.nodes[0])
        right = self.visit(node.nodes[1])
        
        # Ensure both are Variable instances
        if not isinstance(left, Variable):
            left = Variable(left)
        if not isinstance(right, Variable):
            right = Variable(right)
        
        # Special case for inequality comparison
        if left.type == "number" and right.type == "number":
            left_value = left.value.value if hasattr(left.value, 'value') else 0
            right_value = right.value.value if hasattr(right.value, 'value') else 0
            is_not_equal = left_value != right_value
        elif left.type == "string" and right.type == "string":
            left_value = left.value.value if hasattr(left.value, 'value') else ""
            right_value = right.value.value if hasattr(right.value, 'value') else ""
            is_not_equal = left_value != right_value
        else:
            # Different types are always not equal
            is_not_equal = True

        result = Variable(1.0 if is_not_equal else 0.0)
        result.is_boolean = True
        result.boolean_name = "TRUE" if is_not_equal else "FALSE"
        return result

    def visit_lt(self, node):
        """Visit a less than node"""
        left = self.visit(node.nodes[0])
        right = self.visit(node.nodes[1])
        
        # Ensure both are Variable instances
        if not isinstance(left, Variable):
            left = Variable(left)
        if not isinstance(right, Variable):
            right = Variable(right)

        # Handle different type combinations with proper value extraction
        if left.type == "number" and right.type == "number":
            # Extract the actual numeric values for comparison
            left_value = left.value.value if hasattr(left.value, 'value') else 0
            right_value = right.value.value if hasattr(right.value, 'value') else 0
            is_less_than = left_value < right_value
        elif left.type == "string" and right.type == "string":
            left_value = left.value.value if hasattr(left.value, 'value') else ""
            right_value = right.value.value if hasattr(right.value, 'value') else ""
            is_less_than = left_value < right_value
        else:
            raise Exception("Cannot compare different types")

        result = Variable(1.0 if is_less_than else 0.0)
        result.is_boolean = True
        result.boolean_name = "TRUE" if is_less_than else "FALSE"
        return result

    def visit_gt(self, node):
        """Visit a greater than node"""
        left = self.visit(node.nodes[0])
        right = self.visit(node.nodes[1])
        
        # Ensure both are Variable instances
        if not isinstance(left, Variable):
            left = Variable(left)
        if not isinstance(right, Variable):
            right = Variable(right)

        # Handle different type combinations with proper value extraction
        if left.type == "number" and right.type == "number":
            # Extract the actual numeric values for comparison
            left_value = left.value.value if hasattr(left.value, 'value') else 0
            right_value = right.value.value if hasattr(right.value, 'value') else 0
            is_greater_than = left_value > right_value
        elif left.type == "string" and right.type == "string":
            left_value = left.value.value if hasattr(left.value, 'value') else ""
            right_value = right.value.value if hasattr(right.value, 'value') else ""
            is_greater_than = left_value > right_value
        else:
            raise Exception("Cannot compare different types")

        result = Variable(1.0 if is_greater_than else 0.0)
        result.is_boolean = True
        result.boolean_name = "TRUE" if is_greater_than else "FALSE"
        return result

    def visit_lte(self, node):
        """Visit a less than or equal node"""
        left = self.visit(node.nodes[0])
        right = self.visit(node.nodes[1])
        
        # Ensure both are Variable instances
        if not isinstance(left, Variable):
            left = Variable(left)
        if not isinstance(right, Variable):
            right = Variable(right)

        # Handle different type combinations with proper value extraction
        if left.type == "number" and right.type == "number":
            # Extract the actual numeric values for comparison
            left_value = left.value.value if hasattr(left.value, 'value') else 0
            right_value = right.value.value if hasattr(right.value, 'value') else 0
            is_less_than_or_equal = left_value <= right_value
        elif left.type == "string" and right.type == "string":
            left_value = left.value.value if hasattr(left.value, 'value') else ""
            right_value = right.value.value if hasattr(right.value, 'value') else ""
            is_less_than_or_equal = left_value <= right_value
        else:
            raise Exception("Cannot compare different types")

        result = Variable(1.0 if is_less_than_or_equal else 0.0)
        result.is_boolean = True
        result.boolean_name = "TRUE" if is_less_than_or_equal else "FALSE"
        return result

    def visit_gte(self, node):
        """Visit a greater than or equal node"""
        left = self.visit(node.nodes[0])
        right = self.visit(node.nodes[1])
        
        # Ensure both are Variable instances
        if not isinstance(left, Variable):
            left = Variable(left)
        if not isinstance(right, Variable):
            right = Variable(right)

        # Handle different type combinations with proper value extraction
        if left.type == "number" and right.type == "number":
            # Extract the actual numeric values for comparison
            left_value = left.value.value if hasattr(left.value, 'value') else 0
            right_value = right.value.value if hasattr(right.value, 'value') else 0
            is_greater_than_or_equal = left_value >= right_value
        elif left.type == "string" and right.type == "string":
            left_value = left.value.value if hasattr(left.value, 'value') else ""
            right_value = right.value.value if hasattr(right.value, 'value') else ""
            is_greater_than_or_equal = left_value >= right_value
        else:
            raise Exception("Cannot compare different types")

        result = Variable(1.0 if is_greater_than_or_equal else 0.0)
        result.is_boolean = True
        result.boolean_name = "TRUE" if is_greater_than_or_equal else "FALSE"
        return result

    def visit_and(self, node):
        """Visit an AND node"""
        left = self.visit(node.nodes[0])

        # Short circuit evaluation
        if left.type == "number" and left.value.value == 0:
            result = Variable(0.0)
            result.is_boolean = True
            result.boolean_name = "FALSE"
            return result

        right = self.visit(node.nodes[1])

        if left.type != "number" or right.type != "number":
            raise Exception("AND operation requires number operands")

        result = Variable(1.0 if left.value.value != 0 and right.value.value != 0 else 0.0)
        result.is_boolean = True
        result.boolean_name = "TRUE" if result.value.value == 1.0 else "FALSE"
        return result

    def visit_or(self, node):
        """Visit an OR node"""
        left = self.visit(node.nodes[0])

        # Short circuit evaluation
        if left.type == "number" and left.value.value != 0:
            result = Variable(1.0)
            result.is_boolean = True
            result.boolean_name = "TRUE"
            return result

        right = self.visit(node.nodes[1])

        if left.type != "number" or right.type != "number":
            raise Exception("OR operation requires number operands")

        result = Variable(1.0 if left.value.value != 0 or right.value.value != 0 else 0.0)
        result.is_boolean = True
        result.boolean_name = "TRUE" if result.value.value == 1.0 else "FALSE"
        return result

    def visit_not(self, node):
        """Visit a NOT node"""
        value = self.visit(node.nodes[0])

        if value.type != "number":
            raise Exception("NOT operation requires a number operand")

        result = Variable(1.0 if value.value.value == 0 else 0.0)
        result.is_boolean = True
        result.boolean_name = "TRUE" if result.value.value == 1.0 else "FALSE"
        return result

    def visit_if(self, node):
        """Visit an IF node"""
        condition = self.visit(node.nodes[0])

        if condition.type != "number":
            raise Exception("IF condition must evaluate to a number")

        if condition.value.value != 0:
            return self.visit(node.nodes[1])  # Execute the if block

        return Variable()  # Return nothing if condition is false

    def visit_if_else(self, node):
        """Visit an IF-ELSE node"""
        condition = self.visit(node.nodes[0])

        if condition.type != "number":
            raise Exception("IF condition must evaluate to a number")

        if condition.value.value != 0:
            return self.visit(node.nodes[1])  # Execute the if block
        else:
            return self.visit(node.nodes[2])  # Execute the else block

    def visit_for(self, node):
        """Visit a FOR loop node"""
        var_name = node.name
        start_val = self.visit(node.nodes[0])
        end_val = self.visit(node.nodes[1])
        step_val = self.visit(node.nodes[2])
        body = node.nodes[3]

        if start_val.type != "number" or end_val.type != "number" or step_val.type != "number":
            raise Exception("FOR loop values must be numbers")

        self.current_symbol_table.set(var_name, start_val)
        last_value = Variable()

        # Different loop behavior based on step direction
        if step_val.value.value >= 0:
            while self.current_symbol_table.get(var_name).value.value <= end_val.value.value:
                last_value = self.visit(body)

                # Check if a return was requested
                if self.return_value is not None:
                    return self.return_value

                # Increment counter
                current_val = self.current_symbol_table.get(var_name).value.value
                self.current_symbol_table.set(var_name,
                                            Variable(current_val + step_val.value.value))
        else:
            while self.current_symbol_table.get(var_name).value.value >= end_val.value.value:
                last_value = self.visit(body)

                # Check if a return was requested
                if self.return_value is not None:
                    return self.return_value

                # Decrement counter
                current_val = self.current_symbol_table.get(var_name).value.value
                self.current_symbol_table.set(var_name,
                                            Variable(current_val + step_val.value.value))

        return last_value

    def visit_while(self, node):
        """Visit a WHILE loop node"""
        condition = node.nodes[0]
        body = node.nodes[1]
        last_value = Variable()

        while True:
            cond_value = self.visit(condition)

            if cond_value.type != "number":
                raise Exception("WHILE condition must evaluate to a number")

            if cond_value.value.value == 0:
                break

            last_value = self.visit(body)

            # Check if a return was requested
            if self.return_value is not None:
                return self.return_value

        return last_value

    def visit_block(self, node):
        """Visit a block of code"""
        last_value = Variable()

        for statement in node.nodes:
            last_value = self.visit(statement)

            # Check if a return was requested
            if self.return_value is not None:
                return self.return_value

        return last_value

    def visit_def(self, node):
        """Visit a function definition node"""
        func_name = node.name
        function = Function(func_name, node.nodes[0], node.nodes[1], node.nodes[2])
        self.current_symbol_table.set(func_name, Variable(function))
        return Variable(function)

    def visit_function_call(self, node):
        """Visit a function call node"""
        func_name = node.name

        # Check recursion depth
        if self.recursion_depth >= self.max_recursion_depth:
            # Raise an exception instead of silently returning a value
            # This prevents silent infinite recursion issues
            raise Exception(f"Maximum recursion depth exceeded ({self.max_recursion_depth})")

        if not self.current_symbol_table.has(func_name):
            raise Exception(f"Function '{func_name}' not defined")

        function_var = self.current_symbol_table.get(func_name)

        if function_var.type != "function":
            raise Exception(f"'{func_name}' is not a function")

        function = function_var.value

        # Evaluate function arguments in the current scope
        # It's important to do this before creating the new scope
        arg_values = []
        if node.nodes:
            for arg_node in node.nodes:
                arg_values.append(self.visit(arg_node))

        # Increment recursion depth before executing function body
        self.recursion_depth += 1

        try:
            # Create a new completely independent symbol table for this function call
            # Unlike before, we create a child table of the current table to preserve scope chain
            function_symbol_table = self.current_symbol_table.create_child_table()
            
            # Add the function itself to the new symbol table to enable recursion
            function_symbol_table.set(func_name, function_var)

            # Process and set arguments in the function's symbol table
            if function.args_node:
                arg_nodes = function.args_node.nodes

                if len(arg_nodes) != len(arg_values):
                    raise Exception(f"Function '{func_name}' expects {len(arg_nodes)} arguments, got {len(arg_values)}")

                for i, arg_node in enumerate(arg_nodes):
                    arg_name = arg_node.name
                    # Create new copies of values for function arguments to prevent side effects
                    function_symbol_table.set(arg_name, arg_values[i].copy() if hasattr(arg_values[i], 'copy') else arg_values[i])

            # Save current state
            old_symbol_table = self.current_symbol_table
            old_return_value = self.return_value
            
            # Switch context to the function's environment
            self.current_symbol_table = function_symbol_table
            self.return_value = None

            # Execute the function body
            body_result = self.visit(function.body_node)
            
            # Determine the return value
            if self.return_value is not None:
                # An explicit RETURN statement was executed
                return_value = self.return_value
            else:
                # No explicit RETURN, use the function's return expression
                return_value = self.visit(function.return_node)

            # Restore the original context
            self.current_symbol_table = old_symbol_table
            
            # Reset return value properly
            # This fix is crucial for recursive functions like Fibonacci
            # We only want to preserve return values for the immediate caller
            self.return_value = old_return_value

            return return_value
        finally:
            # Always decrement recursion depth
            self.recursion_depth -= 1

    def visit_print(self, node):
        """Visit a PRINT node"""
        values = []

        for arg_node in node.nodes:
            value = self.visit(arg_node)
            values.append(str(value))

        output = " ".join(values)
        self.output_text += output + "\n"
        return Variable()

    def visit_input(self, node):
        """Visit an INPUT node"""
        # This will be overridden by the GUI component
        # Default implementation for testing
        var_name = node.name
        result = input(f"Enter value for {var_name}: ")

        # Try to convert to number if possible
        try:
            value = Variable(float(result))
        except ValueError:
            value = Variable(result)

        # Store the input value in the variable
        self.current_symbol_table.set(var_name, value)

        return value

    def visit_read(self, node):
        """Visit a READ node"""
        if not node.nodes:
            raise Exception("READ requires a filename")

        filename_var = self.visit(node.nodes[0])
        filename = str(filename_var)

        # Check if the path is relative or absolute
        if not os.path.isabs(filename):
            filename = os.path.join(self.cwd, filename)

        try:
            with open(filename, 'r') as file:
                content = file.read()
                return Variable(content)
        except Exception as e:
            raise Exception(f"Error reading file '{filename}': {str(e)}")

    def visit_include(self, node):
        """Visit an INCLUDE node"""
        from .lexer import Lexer
        from .parser import Parser
        import importlib.resources as pkg_resources

        filename = node.name
        file_content = None
        error_message = ""

        # Paths to try in order:
        # 1. Absolute path if provided
        # 2. Relative to current working directory
        # 3. In the stdlib directory

        # Check if the path is absolute
        if os.path.isabs(filename):
            try:
                with open(filename, 'r') as file:
                    file_content = file.read()
            except Exception as e:
                error_message = f"Error reading file '{filename}': {str(e)}"
        else:
            # Try relative to current directory first
            try:
                local_path = os.path.join(self.cwd, filename)
                with open(local_path, 'r') as file:
                    file_content = file.read()
            except Exception as local_error:
                # If not found locally, try stdlib directory
                stdlib_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'stdlib', filename)
                try:
                    with open(stdlib_path, 'r') as file:
                        file_content = file.read()
                except Exception as stdlib_error:
                    error_message = f"Could not find '{filename}' in current directory or stdlib: {str(local_error)}"

        if file_content is None:
            raise Exception(error_message)

        # Tokenize the included file
        lexer = Lexer(file_content)
        tokens = lexer.generate_tokens()

        # Parse the tokens
        parser = Parser(tokens)
        included_ast = parser.parse()

        # Execute the included code
        return self.visit(included_ast)

    def visit_return(self, node):
        """Visit a RETURN node"""
        # Evaluate the return expression
        return_value = self.visit(node.nodes[0])
        
        # Make sure we have a Variable instance
        if not isinstance(return_value, Variable):
            return_value = Variable(return_value)
            
        # Store the return value in this instance
        # This will be checked by the function_call visitor
        self.return_value = return_value
        
        # Return the value directly as well, to support implicit returns
        return return_value

    def visit_case(self, node):
        """Visit a CASE node"""
        var_name = node.name

        # Get the value of the variable
        if not self.current_symbol_table.has(var_name):
            raise Exception(f"Variable '{var_name}' not defined")

        var_value = self.current_symbol_table.get(var_name)

        # Evaluate each case item in order
        for case_item in node.nodes:
            if case_item.type == NodeType.CASE_OTHERWISE:
                return self.visit(case_item)

            # Get the case value
            case_value = self.visit(case_item.nodes[0])

            # Check if this is a range case (has two value nodes)
            if len(case_item.nodes) >= 2 and case_item.nodes[1].type not in [NodeType.BLOCK, NodeType.PRINT, NodeType.INPUT, NodeType.READ]:
                range_end = self.visit(case_item.nodes[1])

                # Check if value is in the range
                if case_value.type != "number" or range_end.type != "number" or var_value.type != "number":
                    raise Exception("Range values must be numbers")

                if (var_value.value.value >= case_value.value.value and
                    var_value.value.value <= range_end.value.value):
                    # Execute the statements for this case
                    last_value = Variable()
                    for statement in case_item.nodes[2:]:
                        last_value = self.visit(statement)
                    return last_value
            else:
                # Simple equality check
                if var_value == case_value:
                    # Execute the statements for this case
                    last_value = Variable()
                    for statement in case_item.nodes[1:]:
                        last_value = self.visit(statement)
                    return last_value

        # If no cases matched and there's no OTHERWISE clause, return an empty value
        return Variable()

    def visit_case_item(self, node):
        """Visit a CASE_ITEM node"""
        # This should not be directly visited, as the CASE node handles it
        raise Exception("CASE_ITEM should not be directly visited")

    def visit_case_otherwise(self, node):
        """Visit a CASE_OTHERWISE node"""
        # Execute all statements in the OTHERWISE clause
        last_value = Variable()
        for statement in node.nodes:
            last_value = self.visit(statement)
        return last_value

    def visit_repeat_until(self, node):
        """Visit a REPEAT-UNTIL loop node"""
        body = node.nodes[0]
        condition = node.nodes[1]
        last_value = Variable()

        while True:
            # First execute the body
            last_value = self.visit(body)

            # Check if a return was requested
            if self.return_value is not None:
                return self.return_value

            # Then check the condition
            cond_value = self.visit(condition)

            if cond_value.type != "number":
                raise Exception("UNTIL condition must evaluate to a number")

            # If condition is true, exit the loop
            if cond_value.value.value != 0:
                break

        return last_value

    def visit_declare(self, node):
        """Visit a DECLARE node"""
        var_name = node.name
        type_node = node.nodes[0]
        type_name = type_node.name

        # Initialize the variable based on its type
        if type_name == "INTEGER":
            self.current_symbol_table.set(var_name, Variable(0))
        elif type_name == "REAL":
            self.current_symbol_table.set(var_name, Variable(0.0))
        elif type_name == "STRING":
            self.current_symbol_table.set(var_name, Variable(""))
        elif type_name == "BOOLEAN":
            self.current_symbol_table.set(var_name, Variable(0))  # False
        elif type_name == "CHAR":
            self.current_symbol_table.set(var_name, Variable(""))  # Empty char
        elif type_name.startswith("ARRAY"):
            # Initialize as empty list
            self.current_symbol_table.set(var_name, Variable([]))
        else:
            # For user-defined types, initialize as empty
            self.current_symbol_table.set(var_name, Variable())

        return Variable()

    def visit_array_access(self, node):
        """Visit an array access node"""
        var_name = node.name

        if not self.current_symbol_table.has(var_name):
            raise Exception(f"Array '{var_name}' not defined")

        array_var = self.current_symbol_table.get(var_name)

        if array_var.type != "list":
            raise Exception(f"'{var_name}' is not an array")

        # Get the array data
        array_data = array_var.value.values

        # Calculate the index
        if len(node.nodes) == 1:
            # One-dimensional array
            index_val = self.visit(node.nodes[0])
            if index_val.type != "number":
                raise Exception("Array index must be a number")

            index = int(index_val.value.value) - 1  # Convert to 0-based indexing

            if index < 0 or index >= len(array_data):
                raise Exception(f"Array index {index + 1} out of bounds")

            return array_data[index]

        elif len(node.nodes) == 2:
            # Two-dimensional array
            row_val = self.visit(node.nodes[0])
            col_val = self.visit(node.nodes[1])

            if row_val.type != "number" or col_val.type != "number":
                raise Exception("Array indices must be numbers")

            row = int(row_val.value.value) - 1  # Convert to 0-based indexing
            col = int(col_val.value.value) - 1

            if row < 0 or row >= len(array_data):
                raise Exception(f"Array row index {row + 1} out of bounds")

            if not isinstance(array_data[row], Variable) or array_data[row].type != "list":
                raise Exception("Invalid 2D array structure")

            row_data = array_data[row].value.values

            if col < 0 or col >= len(row_data):
                raise Exception(f"Array column index {col + 1} out of bounds")

            return row_data[col]

        else:
            raise Exception("Arrays with more than 2 dimensions not supported")

    def visit_array_assign(self, node):
        """Visit an array assignment node"""
        var_name = node.name

        if not self.current_symbol_table.has(var_name):
            raise Exception(f"Array '{var_name}' not defined")

        array_var = self.current_symbol_table.get(var_name)

        if array_var.type != "list":
            raise Exception(f"'{var_name}' is not an array")

        # Get the array data
        array_data = array_var.value.values

        # Get the value to assign (last node)
        value = self.visit(node.nodes[-1])

        # Calculate the index
        if len(node.nodes) == 2:  # 1 index + 1 value
            # One-dimensional array
            index_val = self.visit(node.nodes[0])
            if index_val.type != "number":
                raise Exception("Array index must be a number")

            index = int(index_val.value.value) - 1  # Convert to 0-based indexing

            # Expand array if necessary
            while index >= len(array_data):
                array_data.append(Variable(0))

            if index < 0:
                raise Exception(f"Array index {index + 1} out of bounds")

            array_data[index] = value

        elif len(node.nodes) == 3:  # 2 indices + 1 value
            # Two-dimensional array
            row_val = self.visit(node.nodes[0])
            col_val = self.visit(node.nodes[1])

            if row_val.type != "number" or col_val.type != "number":
                raise Exception("Array indices must be numbers")

            row = int(row_val.value.value) - 1  # Convert to 0-based indexing
            col = int(col_val.value.value) - 1

            # Expand array if necessary
            while row >= len(array_data):
                array_data.append(Variable([]))

            if row < 0:
                raise Exception(f"Array row index {row + 1} out of bounds")

            # Ensure the row is a list
            if array_data[row].type != "list":
                array_data[row] = Variable([])

            row_data = array_data[row].value.values

            # Expand row if necessary
            while col >= len(row_data):
                row_data.append(Variable(0))

            if col < 0:
                raise Exception(f"Array column index {col + 1} out of bounds")

            row_data[col] = value

        else:
            raise Exception("Arrays with more than 2 dimensions not supported")

        return value