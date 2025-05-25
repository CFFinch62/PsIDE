# Pseudocode Interpreter - Modular Structure

This is a refactored version of the Pseudocode Interpreter with a clean, modular architecture for better maintainability and extensibility.

## Project Structure

```
pseudocode_interpreter/
├── __init__.py                 # Main package initialization
├── core/                       # Core interpreter components
│   ├── __init__.py            # Core module exports
│   ├── tokens.py              # Token types and Token class
│   ├── lexer.py               # Lexical analysis (tokenization)
│   ├── ast_nodes.py           # AST node types and Node class
│   ├── parser.py              # Syntax analysis (parsing)
│   ├── values.py              # Value types (Number, String, List, etc.)
│   └── interpreter.py         # Code execution and interpretation
├── gui/                       # Graphical user interface components
│   ├── __init__.py            # GUI module exports
│   ├── main_window.py         # Main IDE window
│   ├── highlighter.py         # Syntax highlighting
│   └── dialogs.py             # Input dialogs and other UI dialogs
└── utils/                     # Utility functions
    └── __init__.py            # Utils module exports

main.py                        # Application entry point
test_modular.py               # Test script for modular structure
```

## Module Descriptions

### Core Module (`pseudocode_interpreter/core/`)

The core module contains all the language processing components:

- **`tokens.py`**: Defines token types and the Token class used by the lexer
- **`lexer.py`**: Converts raw source code into tokens (lexical analysis)
- **`ast_nodes.py`**: Defines AST node types and the Node class for the parse tree
- **`parser.py`**: Converts tokens into an Abstract Syntax Tree (syntax analysis)
- **`values.py`**: Runtime value types (Number, String, List, Function, etc.) and symbol table
- **`interpreter.py`**: Executes the AST and manages program state

### GUI Module (`pseudocode_interpreter/gui/`)

The GUI module contains all user interface components:

- **`main_window.py`**: The main IDE window with editor, output console, and menus
- **`highlighter.py`**: Syntax highlighting for the code editor
- **`dialogs.py`**: Custom dialogs like the input dialog for the INPUT command

### Utils Module (`pseudocode_interpreter/utils/`)

Reserved for utility functions and helper classes.

## Benefits of the Modular Structure

1. **Separation of Concerns**: Each module has a clear, single responsibility
2. **Easier Maintenance**: Changes to one component don't affect others
3. **Better Testing**: Individual components can be tested in isolation
4. **Improved Readability**: Smaller files are easier to understand and navigate
5. **Extensibility**: New features can be added to specific modules without cluttering others
6. **Reusability**: Core components can be used independently (e.g., in a CLI version)

## Running the Application

### GUI Version
```bash
python main.py
```

### Testing the Modular Structure
```bash
python test_modular.py
```

## Using Components Independently

The modular structure allows you to use individual components:

```python
# Use just the lexer and parser
from pseudocode_interpreter.core import Lexer, Parser

code = "x = 5 + 3"
lexer = Lexer(code)
tokens = lexer.generate_tokens()
parser = Parser(tokens)
ast = parser.parse()
```

```python
# Use the complete interpreter
from pseudocode_interpreter.core import Lexer, Parser, Interpreter

code = """
x = 10
PRINT x
"""

lexer = Lexer(code)
tokens = lexer.generate_tokens()
parser = Parser(tokens)
ast = parser.parse()
interpreter = Interpreter()
result = interpreter.interpret(ast)
print(interpreter.output_text)
```

## Adding New Features

### Adding a New Language Feature
1. Add new token types to `core/tokens.py` if needed
2. Update the lexer in `core/lexer.py` to recognize new syntax
3. Add new AST node types to `core/ast_nodes.py` if needed
4. Update the parser in `core/parser.py` to handle the new syntax
5. Add the execution logic to `core/interpreter.py`

### Adding New GUI Features
1. Create new dialog classes in `gui/dialogs.py`
2. Add new functionality to `gui/main_window.py`
3. Update syntax highlighting in `gui/highlighter.py` if needed

## Migration from Original File

The original `pseudocode_interpreter.py` file has been completely refactored into this modular structure while preserving all functionality. The main changes are:

- **No Functional Changes**: All features work exactly as before
- **Better Organization**: Code is organized into logical modules
- **Improved Imports**: Clean import statements in each module
- **Better Error Handling**: Errors are isolated to specific modules
- **Future-Proof**: Easy to extend and modify individual components

## Dependencies

- Python 3.7+
- PyQt6

Install dependencies:
```bash
pip install -r requirements.txt
``` 