from typing import List
from .tokens import Token, TokenType
from .ast_nodes import Node, NodeType

# Parser class
class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.cursor_pos = 0
        self.current_token = self.tokens[0] if tokens else Token(TokenType.NONE)

    def advance(self):
        """Advance to the next token"""
        self.cursor_pos += 1
        if self.cursor_pos < len(self.tokens):
            self.current_token = self.tokens[self.cursor_pos]
        else:
            self.current_token = Token(TokenType.NONE)

    def devance(self):
        """Go back to the previous token"""
        self.cursor_pos -= 1
        if self.cursor_pos >= 0:
            self.current_token = self.tokens[self.cursor_pos]

    def parse(self):
        """Parse the tokens and return the AST"""
        if not self.tokens:
            return Node(NodeType.NULL)

        # Skip any leading separators/newlines
        self.sep_expr()

        statements = []

        # Parse multiple statements
        while self.current_token.type != TokenType.NONE:
            if self.current_token.type in [TokenType.SEP, TokenType.NL]:
                self.sep_expr()
                continue

            statement = self.expr()
            statements.append(statement)
            self.sep_expr()  # Skip any separators after the statement

        # If we have multiple statements, wrap them in a block
        if len(statements) == 0:
            return Node(NodeType.NULL)
        elif len(statements) == 1:
            return statements[0]
        else:
            return Node(NodeType.BLOCK, nodes=statements)

    def declare_expr(self):
        """Handle variable declarations: DECLARE identifier : type"""
        self.advance()  # Skip 'DECLARE'

        if self.current_token.type != TokenType.IDENTIFIER:
            raise Exception("Expected identifier after DECLARE")

        var_name = self.current_token.name
        self.advance()  # Skip identifier

        if self.current_token.type != TokenType.COLON:
            raise Exception("Expected ':' after identifier in DECLARE statement")

        self.advance()  # Skip ':'

        # Parse the type - could be simple type or ARRAY[...] OF type
        if self.current_token.type == TokenType.KEYWORD and self.current_token.name == 'ARRAY':
            # Handle array declaration: ARRAY[1:5] OF INTEGER or ARRAY[1:3, 1:3] OF INTEGER
            self.advance()  # Skip 'ARRAY'

            if self.current_token.type != TokenType.LSQBRACKET:
                raise Exception("Expected '[' after ARRAY")

            self.advance()  # Skip '['

            # Parse array dimensions (could be multiple for multi-dimensional arrays)
            dimensions = []

            # Parse first dimension
            start_expr = self.expr()
            if self.current_token.type != TokenType.COLON:
                raise Exception("Expected ':' in array dimension")
            self.advance()  # Skip ':'
            end_expr = self.expr()
            dimensions.append((start_expr, end_expr))

            # Check for additional dimensions
            while self.current_token.type == TokenType.COMMA:
                self.advance()  # Skip ','
                start_expr = self.expr()
                if self.current_token.type != TokenType.COLON:
                    raise Exception("Expected ':' in array dimension")
                self.advance()  # Skip ':'
                end_expr = self.expr()
                dimensions.append((start_expr, end_expr))

            if self.current_token.type != TokenType.RSQBRACKET:
                raise Exception("Expected ']' to close array dimensions")

            self.advance()  # Skip ']'

            if self.current_token.type != TokenType.KEYWORD or self.current_token.name != 'OF':
                raise Exception("Expected 'OF' after array dimensions")

            self.advance()  # Skip 'OF'

            if self.current_token.type != TokenType.KEYWORD:
                raise Exception("Expected type name after 'OF'")

            element_type = self.current_token.name
            self.advance()  # Skip element type

            # Create array type string
            dim_strs = []
            for start, end in dimensions:
                # For now, just use simple representation
                dim_strs.append(f"{start.value if hasattr(start, 'value') else '?'}:{end.value if hasattr(end, 'value') else '?'}")
            array_type = f"ARRAY[{','.join(dim_strs)}] OF {element_type}"

            return Node(NodeType.DECLARE, name=var_name, nodes=[Node(NodeType.STRING, name=array_type)])
        else:
            # Simple type declaration
            if self.current_token.type != TokenType.KEYWORD:
                raise Exception("Expected type name after ':' in DECLARE statement")

            type_name = self.current_token.name
            self.advance()  # Skip type name

            return Node(NodeType.DECLARE, name=var_name, nodes=[Node(NodeType.STRING, name=type_name)])

    def expr(self, allow_assignment=True):
        """Parse expressions"""
        # Handle variable assignments (only if assignments are allowed)
        if (allow_assignment and
            self.current_token.type == TokenType.IDENTIFIER and
            self.cursor_pos + 1 < len(self.tokens) and
            self.tokens[self.cursor_pos + 1].type == TokenType.EQ):

            var_name = self.current_token.name
            self.advance()  # Skip identifier
            self.advance()  # Skip equals

            expr = self.expr()
            return Node(NodeType.VAR_ASSIGN, name=var_name, nodes=[expr])

        # Handle array assignments (only if assignments are allowed)
        elif (allow_assignment and
              self.current_token.type == TokenType.IDENTIFIER and
              self.cursor_pos + 1 < len(self.tokens) and
              self.tokens[self.cursor_pos + 1].type == TokenType.LSQBRACKET):

            # Look ahead to see if this is an array assignment
            temp_pos = self.cursor_pos + 2
            bracket_count = 1
            while temp_pos < len(self.tokens) and bracket_count > 0:
                if self.tokens[temp_pos].type == TokenType.LSQBRACKET:
                    bracket_count += 1
                elif self.tokens[temp_pos].type == TokenType.RSQBRACKET:
                    bracket_count -= 1
                temp_pos += 1

            # Check if there's an equals sign after the closing bracket
            if (temp_pos < len(self.tokens) and
                self.tokens[temp_pos].type == TokenType.EQ):

                var_name = self.current_token.name
                self.advance()  # Skip identifier
                self.advance()  # Skip '['

                # Parse array indices
                indices = []
                indices.append(self.expr())

                while self.current_token.type == TokenType.COMMA:
                    self.advance()  # Skip ','
                    indices.append(self.expr())

                if self.current_token.type != TokenType.RSQBRACKET:
                    raise Exception("Expected ']' to close array assignment")

                self.advance()  # Skip ']'
                self.advance()  # Skip '='

                value_expr = self.expr()
                return Node(NodeType.ARRAY_ASSIGN, name=var_name, nodes=indices + [value_expr])

        # Handle keywords
        elif self.current_token.type == TokenType.KEYWORD:
            keyword = self.current_token.name

            if keyword == 'IF':
                return self.if_expr()
            elif keyword == 'FOR':
                return self.for_expr()
            elif keyword == 'WHILE':
                return self.while_expr()
            elif keyword in ['DEF', 'FUNCTION', 'PROCEDURE']:
                return self.def_expr()
            elif keyword in ['PRINT', 'INPUT', 'read']:
                return self.builtin_expr()
            elif keyword == 'INCLUDE':
                return self.include_expr()
            elif keyword == 'CASE':
                return self.case_expr()
            elif keyword == 'REPEAT':
                return self.repeat_until_expr()
            elif keyword == 'DECLARE':
                return self.declare_expr()
            elif keyword == 'RETURN':
                return self.return_expr()
            elif keyword == 'ENDEF':
                # This should only appear at the end of a function definition, so it's an error if we see it here
                raise Exception("Unexpected ENDEF outside of function definition")

        # Handle logical expressions
        return self.comp_expr()

    def comp_expr(self):
        """Handle comparison expressions"""
        if self.current_token.type == TokenType.KEYWORD and self.current_token.name == 'NOT':
            self.advance()
            node = Node(NodeType.NOT, nodes=[self.comp_expr()])
            return node

        node = self.arith_expr()

        while (self.current_token.type in [TokenType.EQ, TokenType.EE, TokenType.NE, TokenType.LT,
                                          TokenType.GT, TokenType.LTE, TokenType.GTE] or
              (self.current_token.type == TokenType.KEYWORD and
               self.current_token.name in ['AND', 'OR'])):

            if self.current_token.type == TokenType.EQ:
                self.advance()
                node = Node(NodeType.EE, nodes=[node, self.arith_expr()])
            elif self.current_token.type == TokenType.EE:
                self.advance()
                node = Node(NodeType.EE, nodes=[node, self.arith_expr()])
            elif self.current_token.type == TokenType.NE:
                self.advance()
                node = Node(NodeType.NE, nodes=[node, self.arith_expr()])
            elif self.current_token.type == TokenType.LT:
                self.advance()
                node = Node(NodeType.LT, nodes=[node, self.arith_expr()])
            elif self.current_token.type == TokenType.GT:
                self.advance()
                node = Node(NodeType.GT, nodes=[node, self.arith_expr()])
            elif self.current_token.type == TokenType.LTE:
                self.advance()
                node = Node(NodeType.LTE, nodes=[node, self.arith_expr()])
            elif self.current_token.type == TokenType.GTE:
                self.advance()
                node = Node(NodeType.GTE, nodes=[node, self.arith_expr()])
            elif self.current_token.type == TokenType.KEYWORD and self.current_token.name == 'AND':
                self.advance()
                node = Node(NodeType.AND, nodes=[node, self.comp_expr()])
            elif self.current_token.type == TokenType.KEYWORD and self.current_token.name == 'OR':
                self.advance()
                node = Node(NodeType.OR, nodes=[node, self.comp_expr()])

        return node

    def arith_expr(self):
        """Handle arithmetic expressions: addition and subtraction"""
        node = self.term()

        while self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            if self.current_token.type == TokenType.PLUS:
                self.advance()
                node = Node(NodeType.ADD, nodes=[node, self.term()])
            elif self.current_token.type == TokenType.MINUS:
                self.advance()
                node = Node(NodeType.SUBTRACT, nodes=[node, self.term()])

        return node

    def term(self):
        """Handle term expressions: multiplication, division, MOD, and DIV"""
        node = self.factor()

        while (self.current_token.type in [TokenType.MULTIPLY, TokenType.DIVIDE] or
               (self.current_token.type == TokenType.KEYWORD and
                self.current_token.name in ['MOD', 'DIV'])):
            if self.current_token.type == TokenType.MULTIPLY:
                self.advance()
                node = Node(NodeType.MULTIPLY, nodes=[node, self.factor()])
            elif self.current_token.type == TokenType.DIVIDE:
                self.advance()
                node = Node(NodeType.DIVIDE, nodes=[node, self.factor()])
            elif self.current_token.type == TokenType.KEYWORD and self.current_token.name == 'MOD':
                self.advance()
                node = Node(NodeType.MODULO, nodes=[node, self.factor()])
            elif self.current_token.type == TokenType.KEYWORD and self.current_token.name == 'DIV':
                self.advance()
                node = Node(NodeType.INT_DIVIDE, nodes=[node, self.factor()])

        return node

    def factor(self):
        """Handle unary operators +/- followed by a power"""
        token = self.current_token

        if token.type == TokenType.PLUS:
            self.advance()
            return Node(NodeType.PLUS, nodes=[self.factor()])
        elif token.type == TokenType.MINUS:
            self.advance()
            return Node(NodeType.MINUS, nodes=[self.factor()])

        return self.power()

    def power(self):
        """Handle exponentiation: base ^ exponent"""
        node = self.atom()

        if self.current_token.type == TokenType.POW:
            self.advance()
            return Node(NodeType.POWER, nodes=[node, self.factor()])

        return node

    def atom(self):
        """Handle atomic expressions: numbers, variables, parentheses, lists, function calls"""
        token = self.current_token

        if token.type == TokenType.NUMBER:
            self.advance()
            return Node(NodeType.NUMBER, value=token.value)
        elif token.type == TokenType.STRING:
            self.advance()
            return Node(NodeType.STRING, name=token.name)
        elif token.type == TokenType.LSQBRACKET:
            return self.list_expr()
        elif token.type == TokenType.LPAREN:
            self.advance()
            expr = self.expr()

            if self.current_token.type != TokenType.RPAREN:
                raise Exception("Expected closing parenthesis")

            self.advance()
            return expr
        elif token.type == TokenType.IDENTIFIER:
            self.advance()

            # Check if this is a function call
            if self.current_token.type == TokenType.LPAREN:
                self.devance()  # Go back to the identifier for function_call to handle
                return self.function_call()

            # Check if this is array access
            elif self.current_token.type == TokenType.LSQBRACKET:
                var_name = token.name
                self.advance()  # Skip '['

                # Parse array indices
                indices = []
                indices.append(self.expr())

                while self.current_token.type == TokenType.COMMA:
                    self.advance()  # Skip ','
                    indices.append(self.expr())

                if self.current_token.type != TokenType.RSQBRACKET:
                    raise Exception("Expected ']' to close array access")

                self.advance()  # Skip ']'

                return Node(NodeType.ARRAY_ACCESS, name=var_name, nodes=indices)

            return Node(NodeType.VAR_ACCESS, name=token.name)
        elif token.type == TokenType.KEYWORD and token.name in ['TRUE', 'FALSE']:
            self.advance()
            return Node(NodeType.BOOLEAN, name=token.name)

        raise Exception(f"Invalid syntax: Unexpected token {token}")

    def list_expr(self):
        """Handle list expressions: [expr, expr, ...]"""
        self.advance()  # Skip the left square bracket
        elements = []

        # Handle empty list
        if self.current_token.type == TokenType.RSQBRACKET:
            self.advance()
            return Node(NodeType.LIST, nodes=elements)

        # Parse list elements
        elements.append(self.expr())

        while self.current_token.type == TokenType.COMMA:
            self.advance()
            elements.append(self.expr())

        if self.current_token.type != TokenType.RSQBRACKET:
            raise Exception("Expected closing bracket for list")

        self.advance()  # Skip the right square bracket
        return Node(NodeType.LIST, nodes=elements)

    def function_call(self):
        """Handle function calls: func_name(arg1, arg2, ...)"""
        func_name = self.current_token.name
        self.advance()  # Skip the identifier
        self.advance()  # Skip the left parenthesis

        args = []

        # Handle no arguments
        if self.current_token.type == TokenType.RPAREN:
            self.advance()
            return Node(NodeType.FUNCTION_CALL, name=func_name, nodes=args)

        # Parse arguments
        args.append(self.expr())

        while self.current_token.type == TokenType.COMMA:
            self.advance()
            args.append(self.expr())

        if self.current_token.type != TokenType.RPAREN:
            raise Exception("Expected closing parenthesis for function call")

        self.advance()  # Skip the right parenthesis
        return Node(NodeType.FUNCTION_CALL, name=func_name, nodes=args)

    def if_expr(self):
        """Handle if expressions: IF condition THEN expr (ELSE expr) ENDIF"""
        self.advance()  # Skip 'IF'
        condition = self.expr(allow_assignment=False)  # Don't allow assignments in conditions

        if self.current_token.type != TokenType.KEYWORD or self.current_token.name != 'THEN':
            raise Exception("Expected 'THEN' after IF condition")

        self.advance()  # Skip 'THEN'

        # Parse the 'if' block
        if_block = self.block_expr(['ELSE', 'ENDIF'])

        # Check if there's an 'else' block
        if self.current_token.type == TokenType.KEYWORD and self.current_token.name == 'ELSE':
            self.advance()  # Skip 'ELSE'
            else_block = self.block_expr(['ENDIF'])

            if self.current_token.type != TokenType.KEYWORD or self.current_token.name != 'ENDIF':
                raise Exception("Expected 'ENDIF' to close IF statement")

            self.advance()  # Skip 'ENDIF'
            return Node(NodeType.IF_ELSE, nodes=[condition, if_block, else_block])

        # No 'else' block
        if self.current_token.type != TokenType.KEYWORD or self.current_token.name != 'ENDIF':
            raise Exception("Expected 'ENDIF' to close IF statement")

        self.advance()  # Skip 'ENDIF'
        return Node(NodeType.IF, nodes=[condition, if_block])

    def for_expr(self):
        """Handle for loops: FOR var = start TO end (STEP step) block NEXT var"""
        self.advance()  # Skip 'FOR'

        if self.current_token.type != TokenType.IDENTIFIER:
            raise Exception("Expected variable name after FOR")

        var_name = self.current_token.name
        self.advance()  # Skip variable name

        if self.current_token.type != TokenType.EQ:
            raise Exception("Expected '=' after variable in FOR loop")

        self.advance()  # Skip '='
        start_value = self.expr()

        if self.current_token.type != TokenType.KEYWORD or self.current_token.name != 'TO':
            raise Exception("Expected 'TO' in FOR loop")

        self.advance()  # Skip 'TO'
        end_value = self.expr()

        # Check for optional STEP
        step_value = Node(NodeType.NUMBER, value=1.0)  # Default step is 1
        if self.current_token.type == TokenType.KEYWORD and self.current_token.name == 'STEP':
            self.advance()  # Skip 'STEP'
            step_value = self.expr()

        # Parse loop body
        body = self.block_expr(['NEXT'])

        if self.current_token.type != TokenType.KEYWORD or self.current_token.name != 'NEXT':
            raise Exception("Expected 'NEXT' to close FOR loop")

        self.advance()  # Skip 'NEXT'

        if self.current_token.type != TokenType.IDENTIFIER or self.current_token.name != var_name:
            raise Exception(f"Expected variable name '{var_name}' after NEXT")

        self.advance()  # Skip variable name

        # Create for node: (var_name, start, end, step, body)
        return Node(NodeType.FOR, name=var_name, nodes=[start_value, end_value, step_value, body])

    def while_expr(self):
        """Handle while loops: WHILE condition DO block ENDWHILE"""
        self.advance()  # Skip 'WHILE'
        condition = self.expr(allow_assignment=False)  # Don't allow assignments in conditions

        if self.current_token.type != TokenType.KEYWORD or self.current_token.name != 'DO':
            raise Exception("Expected 'DO' after WHILE condition")

        self.advance()  # Skip 'DO'

        # Parse loop body
        body = self.block_expr(['ENDWHILE'])

        if self.current_token.type != TokenType.KEYWORD or self.current_token.name != 'ENDWHILE':
            raise Exception("Expected 'ENDWHILE' to close WHILE loop")

        self.advance()  # Skip 'ENDWHILE'

        return Node(NodeType.WHILE, nodes=[condition, body])

    def def_expr(self):
        """Handle function definitions: DEF/FUNCTION/PROCEDURE name(args) DO block RETURN expr ENDEF/ENDFUNCTION/ENDPROCEDURE"""
        func_type = self.current_token.name  # DEF, FUNCTION, or PROCEDURE
        self.advance()  # Skip function type keyword

        if self.current_token.type != TokenType.IDENTIFIER:
            raise Exception("Expected function name after DEF")

        func_name = self.current_token.name
        self.advance()  # Skip function name

        if self.current_token.type != TokenType.LPAREN:
            raise Exception("Expected '(' after function name")

        self.advance()  # Skip '('

        # Parse arguments
        arg_nodes = []
        if self.current_token.type == TokenType.IDENTIFIER:
            arg_nodes.append(Node(NodeType.ARG, name=self.current_token.name))
            self.advance()

            while self.current_token.type == TokenType.COMMA:
                self.advance()  # Skip ','

                if self.current_token.type != TokenType.IDENTIFIER:
                    raise Exception("Expected identifier after ',' in function definition")

                arg_nodes.append(Node(NodeType.ARG, name=self.current_token.name))
                self.advance()

        if self.current_token.type != TokenType.RPAREN:
            raise Exception("Expected ')' after function arguments")

        self.advance()  # Skip ')'

        # Determine expected keywords based on function type
        if func_type == 'FUNCTION':
            # FUNCTION name(args) RETURNS type ... ENDFUNCTION
            # Skip optional RETURNS clause
            if (self.current_token.type == TokenType.KEYWORD and
                self.current_token.name == 'RETURNS'):
                self.advance()  # Skip 'RETURNS'
                # Skip the return type (INTEGER, REAL, etc.)
                if self.current_token.type == TokenType.KEYWORD:
                    self.advance()
            end_keyword = 'ENDFUNCTION'
            body_terminators = ['RETURN', 'ENDFUNCTION']
        elif func_type == 'PROCEDURE':
            # PROCEDURE name(args) ... ENDPROCEDURE
            end_keyword = 'ENDPROCEDURE'
            body_terminators = ['ENDPROCEDURE']
        else:
            # DEF name(args) DO ... ENDEF
            # Make sure there's a DO keyword
            if self.current_token.type != TokenType.KEYWORD or self.current_token.name != 'DO':
                raise Exception("Expected 'DO' after function declaration")
            self.advance()  # Skip 'DO'
            end_keyword = 'ENDEF'
            body_terminators = ['RETURN', 'ENDEF']

        # Parse function body
        body = self.block_expr(body_terminators)

        # Default return value (if no explicit return)
        return_expr = Node(NodeType.NULL)

        # Handle the return statement if present
        if self.current_token.type == TokenType.KEYWORD and self.current_token.name == 'RETURN':
            self.advance()  # Skip 'RETURN'
            # Parse return expression
            return_expr = self.expr()

            # Check for end keyword after RETURN
            self.sep_expr()  # Skip any separators
            if self.current_token.type != TokenType.KEYWORD or self.current_token.name != end_keyword:
                raise Exception(f"Expected '{end_keyword}' to close function definition after RETURN")

        # At this point, we should be at the end keyword
        if self.current_token.type != TokenType.KEYWORD or self.current_token.name != end_keyword:
            raise Exception(f"Expected '{end_keyword}' to close function definition")

        self.advance()  # Skip end keyword

        # Construct function definition node
        args_node = Node(NodeType.ARGS, nodes=arg_nodes)
        return Node(NodeType.DEF, name=func_name, nodes=[args_node, body, return_expr])

    def builtin_expr(self):
        """Handle built-in functions: PRINT/INPUT/read expr"""
        func_type = self.current_token.name
        self.advance()  # Skip function name

        # Parse arguments
        args = []

        # Handle no arguments case for PRINT
        if func_type == 'PRINT' and (
            self.current_token.type == TokenType.NONE or
            self.current_token.type == TokenType.SEP or
            self.current_token.type == TokenType.NL or
            (self.current_token.type == TokenType.KEYWORD and
             self.current_token.name in ['ELSE', 'ENDIF', 'NEXT', 'ENDWHILE'])
        ):
            return Node(NodeType.PRINT, nodes=[])

        # Handle INPUT specifically - it should take an identifier
        if func_type == 'INPUT':
            if self.current_token.type != TokenType.IDENTIFIER:
                raise Exception("INPUT requires an identifier")

            var_name = self.current_token.name
            self.advance()  # Skip identifier
            return Node(NodeType.INPUT, name=var_name)

        # For PRINT and read, we need expressions
        args.append(self.expr())

        while self.current_token.type == TokenType.COMMA:
            self.advance()  # Skip ','
            args.append(self.expr())

        if func_type == 'PRINT':
            return Node(NodeType.PRINT, nodes=args)
        elif func_type == 'read':
            return Node(NodeType.READ, nodes=args)

    def include_expr(self):
        """Handle include statements: INCLUDE "filename" """
        self.advance()  # Skip 'INCLUDE'
        if self.current_token.type != TokenType.STRING:
            raise Exception("Expected string literal after INCLUDE")

        filename = self.current_token.name
        self.advance()  # Skip string literal

        return Node(NodeType.INCLUDE, name=filename)

    def return_expr(self):
        """Handle standalone return statements: RETURN expr"""
        self.advance()  # Skip 'RETURN'

        # Parse return expression
        return_value = self.expr()

        return Node(NodeType.RETURN, nodes=[return_value])

    def block_expr(self, terminators):
        """Parse a block of code until one of the terminator keywords is reached"""
        # Skip any separators
        self.sep_expr()

        statements = []

        while (self.current_token.type != TokenType.NONE and
               not (self.current_token.type == TokenType.KEYWORD and
                   self.current_token.name in terminators)):

            statements.append(self.expr())
            self.sep_expr()  # Skip any separators between statements

        return Node(NodeType.BLOCK, nodes=statements)

    def sep_expr(self):
        """Skip any separator tokens (semicolons, newlines)"""
        count = 0
        while self.current_token.type in [TokenType.SEP, TokenType.NL]:
            count += 1
            self.advance()

        return count

    def case_expr(self):
        """Handle CASE statements: CASE OF identifier values/statements ENDCASE"""
        self.advance()  # Skip 'CASE'

        if self.current_token.type != TokenType.KEYWORD or self.current_token.name != 'OF':
            raise Exception("Expected 'OF' after CASE")

        self.advance()  # Skip 'OF'

        if self.current_token.type != TokenType.IDENTIFIER:
            raise Exception("Expected identifier after CASE OF")

        var_name = self.current_token.name
        self.advance()  # Skip identifier

        # Parse case items
        case_items = []
        otherwise_node = None

        while self.current_token.type != TokenType.KEYWORD or self.current_token.name != 'ENDCASE':
            if self.current_token.type == TokenType.KEYWORD and self.current_token.name == 'OTHERWISE':
                self.advance()  # Skip 'OTHERWISE'

                if self.current_token.type != TokenType.COLON:
                    raise Exception("Expected ':' after OTHERWISE")

                self.advance()  # Skip ':'

                # Parse the statements for OTHERWISE
                otherwise_body = []
                while not (self.current_token.type == TokenType.KEYWORD and
                          (self.current_token.name == 'ENDCASE' or
                           self.current_token.name in ['OTHERWISE'])):
                    otherwise_body.append(self.expr())
                    self.sep_expr()  # Skip any separators

                otherwise_node = Node(NodeType.CASE_OTHERWISE, nodes=otherwise_body)
                continue

            # Parse the case value
            value_expr = self.expr()

            # Check for TO range syntax
            range_end = None
            if self.current_token.type == TokenType.KEYWORD and self.current_token.name == 'TO':
                self.advance()  # Skip 'TO'
                range_end = self.expr()

            if self.current_token.type != TokenType.COLON:
                raise Exception("Expected ':' after case value")

            self.advance()  # Skip ':'

            # Parse the statements for this case
            case_body = []
            while not (self.current_token.type == TokenType.KEYWORD and
                      (self.current_token.name == 'ENDCASE' or
                       self.current_token.name == 'OTHERWISE')) and \
                  not (self.current_token.type == TokenType.NUMBER) and \
                  not (self.current_token.type == TokenType.STRING) and \
                  self.current_token.type != TokenType.EOF:
                case_body.append(self.expr())
                self.sep_expr()  # Skip any separators

            # Create case item node
            if range_end:
                # This is a range case: value1 TO value2
                case_items.append(Node(NodeType.CASE_ITEM, nodes=[value_expr, range_end] + case_body))
            else:
                # Regular case: value
                case_items.append(Node(NodeType.CASE_ITEM, nodes=[value_expr] + case_body))

        if self.current_token.type != TokenType.KEYWORD or self.current_token.name != 'ENDCASE':
            raise Exception("Expected 'ENDCASE' to close CASE statement")

        self.advance()  # Skip 'ENDCASE'

        # If we have an otherwise node, add it to the case items
        if otherwise_node:
            case_items.append(otherwise_node)

        return Node(NodeType.CASE, name=var_name, nodes=case_items)

    def repeat_until_expr(self):
        """Handle REPEAT-UNTIL loops: REPEAT statements UNTIL condition"""
        self.advance()  # Skip 'REPEAT'

        # Parse the loop body
        body = self.block_expr(['UNTIL'])

        if self.current_token.type != TokenType.KEYWORD or self.current_token.name != 'UNTIL':
            raise Exception("Expected 'UNTIL' after REPEAT block")

        self.advance()  # Skip 'UNTIL'

        # Parse the condition
        condition = self.expr()

        return Node(NodeType.REPEAT_UNTIL, nodes=[body, condition])