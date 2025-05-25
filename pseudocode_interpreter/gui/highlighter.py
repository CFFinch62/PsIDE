from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
from PyQt6.QtCore import QRegularExpression

# Syntax Highlighter for the code editor
class PseudocodeHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.highlighting_rules = []
        
        # Define formats for different syntax elements
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6"))  # Blue for keywords
        keyword_format.setFontWeight(QFont.Weight.Bold)
        
        builtin_format = QTextCharFormat()
        builtin_format.setForeground(QColor("#C586C0"))  # Purple for built-in functions
        
        operator_format = QTextCharFormat()
        operator_format.setForeground(QColor("#D4D4D4"))  # Light gray for operators
        
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#B5CEA8"))  # Green for numbers
        
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178"))  # Orange for strings
        
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955"))  # Dark green for comments
        
        # Keywords
        keywords = [
            'IF', 'THEN', 'ELSE', 'ENDIF', 'FOR', 'TO', 'STEP', 'NEXT',
            'WHILE', 'DO', 'ENDWHILE', 'DEF', 'RETURN', 'AND', 'OR', 'NOT',
            'TRUE', 'FALSE', 'REPEAT', 'UNTIL', 'CASE', 'OF', 'OTHERWISE', 'ENDCASE'
        ]
        
        # Add keyword rules
        for word in keywords:
            pattern = f'\\b{word}\\b'
            self.highlighting_rules.append((pattern, keyword_format))
            
        # Built-in functions
        builtins = ['PRINT', 'INPUT', 'read', 'INCLUDE']
        
        # Add builtin rules
        for word in builtins:
            pattern = f'\\b{word}\\b'
            self.highlighting_rules.append((pattern, builtin_format))
            
        # Number rule
        self.highlighting_rules.append((r'\b[0-9]+(\.[0-9]+)?\b', number_format))
        
        # String rule - match both single and double quoted strings
        self.highlighting_rules.append((r'"[^"\\]*(\\.[^"\\]*)*"', string_format))
        self.highlighting_rules.append((r"'[^'\\]*(\\.[^'\\]*)*'", string_format))
        
        # Operator rule
        operators = [
            '\\+', '-', '\\*', '/', '\\^', '=', '==', '!=', '<', '>', '<=', '>='
        ]
        for op in operators:
            self.highlighting_rules.append((op, operator_format))
            
        # Comment rule - assuming // for comments
        self.highlighting_rules.append((r'//[^\n]*', comment_format))
        
    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text"""
        for pattern, format in self.highlighting_rules:
            regex = QRegularExpression(pattern)
            match = regex.match(text)
            while match.hasMatch():
                start = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start, length, format)
                match = regex.match(text, start + length) 