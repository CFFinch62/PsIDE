"""
Pseudocode Interpreter - A modular IDE for writing and executing pseudocode.

This package contains:
- core: The lexer, parser, and interpreter components
- gui: The graphical user interface components
"""

__version__ = "1.0.0"
__author__ = "Chuck Finch - Fragillidae Software"

from .core import *
from .gui import *

__all__ = [
    # Core components
    'Token', 'TokenType', 'Lexer',
    'Node', 'NodeType', 'Parser', 
    'Variable', 'Number', 'String', 'List', 'Function', 'SymbolTable',
    'Interpreter',
    # GUI components
    'PseudocodeIDE', 'PseudocodeHighlighter', 'InputDialog'
] 