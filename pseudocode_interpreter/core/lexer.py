from typing import List
from .tokens import Token, TokenType

# Lexer class
class Lexer:
    # Keywords that the language recognizes
    KEYWORDS = ['IF', 'THEN', 'ELSE', 'ELIF', 'ENDIF', 'FOR', 'TO', 'STEP', 'NEXT',
                'WHILE', 'DO', 'ENDWHILE', 'DEF', 'ENDEF', 'RETURN', 'PRINT', 'INPUT', 'read',
                'AND', 'OR', 'NOT', 'TRUE', 'FALSE', 'INCLUDE',
                'REPEAT', 'UNTIL', 'CASE', 'OF', 'OTHERWISE', 'ENDCASE', 'DECLARE',
                'FUNCTION', 'ENDFUNCTION', 'PROCEDURE', 'ENDPROCEDURE', 'RETURNS',
                'MOD', 'DIV', 'REM', 'ARRAY', 'INTEGER', 'REAL', 'STRING', 'BOOLEAN']

    def __init__(self, code: str):
        self.code = code
        self.cursor_pos = 0
        self.current_char = self.code[0] if len(self.code) > 0 else None

    def advance(self):
        """Advance the cursor position and set the current character"""
        self.cursor_pos += 1
        if self.cursor_pos < len(self.code):
            self.current_char = self.code[self.cursor_pos]
        else:
            self.current_char = None

    def generate_tokens(self) -> List[Token]:
        """Convert code string into a list of tokens"""
        tokens = []

        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
            elif self.current_char == '\n':
                tokens.append(Token(TokenType.NL))
                self.advance()
            elif self.current_char.isdigit() or self.current_char == '.':
                tokens.append(self.generate_number())
            elif self.current_char.isalpha():
                word_token = self.generate_word()
                if word_token is not None:  # Skip REM comments
                    tokens.append(word_token)
            elif self.current_char == '"' or self.current_char == "'":
                tokens.append(self.generate_string())
            elif self.current_char == '+':
                tokens.append(Token(TokenType.PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TokenType.MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TokenType.MULTIPLY))
                self.advance()
            elif self.current_char == '/':
                # Check for '//' comment
                self.advance()
                if self.current_char == '/':
                    # Skip the entire comment line
                    while self.current_char is not None and self.current_char != '\n':
                        self.advance()
                else:
                    # It's a division operator
                    tokens.append(Token(TokenType.DIVIDE))
            elif self.current_char == '^':
                tokens.append(Token(TokenType.POW))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TokenType.LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TokenType.RPAREN))
                self.advance()
            elif self.current_char == '[':
                tokens.append(Token(TokenType.LSQBRACKET))
                self.advance()
            elif self.current_char == ']':
                tokens.append(Token(TokenType.RSQBRACKET))
                self.advance()
            elif self.current_char == ':':
                tokens.append(Token(TokenType.COLON))
                self.advance()
            elif self.current_char == '←':
                tokens.append(Token(TokenType.EQ))
                self.advance()
            elif self.current_char == '=':
                # Check for '=='
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(TokenType.EE))
                    self.advance()
                else:
                    tokens.append(Token(TokenType.EQ))
            elif self.current_char == '<':
                self.advance()
                # Check for '<=' or '<-' or '<>'
                if self.current_char == '=':
                    tokens.append(Token(TokenType.LTE))
                    self.advance()
                elif self.current_char == '-':
                    tokens.append(Token(TokenType.EQ))  # Treat '<-' as assignment
                    self.advance()
                elif self.current_char == '>':
                    tokens.append(Token(TokenType.NE))  # '<>' is not equal
                    self.advance()
                else:
                    tokens.append(Token(TokenType.LT))
            elif self.current_char == '>':
                # Check for '>='
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(TokenType.GTE))
                    self.advance()
                else:
                    tokens.append(Token(TokenType.GT))
            elif self.current_char == '!':
                # Check for '!='
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(TokenType.NE))
                    self.advance()
                else:
                    raise Exception("Invalid character after '!'")
            elif self.current_char == ',':
                tokens.append(Token(TokenType.COMMA))
                self.advance()
            elif self.current_char == ';':
                tokens.append(Token(TokenType.SEP))
                self.advance()
            else:
                raise Exception(f"Illegal character '{self.current_char}'")

        return tokens

    def generate_number(self) -> Token:
        """Generate a number token from consecutive digits and decimal point"""
        num_str = ""
        decimal_point_count = 0

        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                decimal_point_count += 1
                if decimal_point_count > 1:
                    break

            num_str += self.current_char
            self.advance()

        if num_str.startswith('.'):
            num_str = '0' + num_str
        if num_str.endswith('.'):
            num_str += '0'

        return Token(TokenType.NUMBER, float(num_str))

    def generate_word(self) -> Token:
        """Generate an identifier or keyword token from consecutive letters"""
        word = ""

        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            word += self.current_char
            self.advance()

        # Handle REM comments
        if word.upper() == 'REM':
            # Skip the rest of the line as a comment
            while self.current_char is not None and self.current_char != '\n':
                self.advance()
            # Return None to indicate this should be skipped
            return None

        if word.upper() in self.KEYWORDS:
            return Token(TokenType.KEYWORD, name=word.upper())
        else:
            return Token(TokenType.IDENTIFIER, name=word)

    def generate_string(self) -> Token:
        """Generate a string token from text between quotes"""
        string = ""
        quote_char = self.current_char
        self.advance()  # Skip the opening quote

        # Handle escape characters and collect the string
        while self.current_char is not None and self.current_char != quote_char:
            if self.current_char == '\\':
                self.advance()
                if self.current_char == 'n':
                    string += '\n'
                elif self.current_char == 't':
                    string += '\t'
                elif self.current_char == '\\':
                    string += '\\'
                elif self.current_char == quote_char:
                    string += quote_char
                else:
                    string += '\\' + self.current_char
            else:
                string += self.current_char
            self.advance()

        # Skip the closing quote
        self.advance()

        return Token(TokenType.STRING, name=string)