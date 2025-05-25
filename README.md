# Pseudocode Interpreter

A modular interpreter for executing pseudocode based on Cambridge International AS & A Level Computer Science 9618 and IGCSE Computer Science 0478 specifications.

## Features

### Core Language Features

#### Data Types
- **INTEGER**: Whole numbers (e.g., `5`, `-3`)
- **REAL**: Numbers with fractional parts (e.g., `4.7`, `-4.0`)
- **CHAR**: Single characters (e.g., `'x'`, `'@'`)
- **STRING**: Sequence of characters (e.g., `"Hello World"`)
- **BOOLEAN**: Logical values (`TRUE`, `FALSE`)
- **ARRAY**: Fixed-length structures of elements (e.g., `DECLARE Numbers : ARRAY[1:10] OF INTEGER`)

#### Variables and Assignment
- Variable declaration: `DECLARE <identifier> : <data type>`
- Assignment: `<identifier> ← <value>` or `<identifier> = <value>`

#### Operators
- **Arithmetic**: `+`, `-`, `*`, `/`, `^` (exponentiation), `MOD`, `DIV`
- **Comparison**: `=`, `<>`, `<`, `>`, `<=`, `>=`
- **Logical**: `AND`, `OR`, `NOT`

#### Control Structures
- **IF statements**:
  ```
  IF <condition> THEN
      <statements>
  ENDIF
  ```
  or
  ```
  IF <condition> THEN
      <statements>
  ELSE
      <statements>
  ENDIF
  ```

- **CASE statements**:
  ```
  CASE OF <expression>
      <value1> : <statements>
      <value2> : <statements>
      ...
      OTHERWISE : <statements>
  ENDCASE
  ```

- **FOR loops**:
  ```
  FOR <identifier> ← <value1> TO <value2>
      <statements>
  NEXT <identifier>
  ```
  or with step:
  ```
  FOR <identifier> ← <value1> TO <value2> STEP <increment>
      <statements>
  NEXT <identifier>
  ```

- **REPEAT loops**:
  ```
  REPEAT
      <statements>
  UNTIL <condition>
  ```

- **WHILE loops**:
  ```
  WHILE <condition> DO
      <statements>
  ENDWHILE
  ```

#### Procedures and Functions
- **Procedure definition**:
  ```
  PROCEDURE <identifier>(<parameters>)
      <statements>
  ENDPROCEDURE
  ```

- **Function definition**:
  ```
  FUNCTION <identifier>(<parameters>) RETURNS <data type>
      <statements>
      RETURN <expression>
  ENDFUNCTION
  ```
  
- Alternative syntax (DEF/DO):
  ```
  DEF <identifier>(<parameters>) DO
      <statements>
      RETURN <expression>
  ENDEF
  ```

#### Input/Output
- Input: `INPUT <identifier>` or `<identifier> = INPUT <prompt>`
- Output: `PRINT <expression>` or `OUTPUT <expression>`

#### Comments
- Single line: `REM this is a comment` or `// this is a comment`
- Inline: `PRINT "Hello" REM this is an inline comment`

### Standard Library

#### File I/O (`_fio_`)
- `readFile(filename)`: Read contents of a file
- `writeFile(filename, data)`: Write data to a file (overwrite)
- `appendFile(filename, data)`: Append data to a file
- `removeFile(filename)`: Delete a file
- `listDir(directory)`: List contents of a directory

#### Math Functions (`_math_`)
- `sqrt(n)`: Square root
- `floor(n)`, `ceil(n)`: Floor and ceiling functions
- `factorial(n)`: Factorial
- `sin(n)`, `cos(n)`, `tan(n)`: Trigonometric functions
- `deg(n)`, `rad(n)`: Convert between degrees and radians
- `mod(a,b)`: Modulo operation
- `hcf(a,b)`, `lcm(a,b)`: Highest common factor and lowest common multiple
- `permutations(n,r)`, `combinations(n,r)`: Permutations and combinations

#### String Operations (`_string_`)
- `toList(str)`: Convert string to list of characters
- `split(str, delimiter)`: Split string by delimiter

#### Shell Commands
- `shell(command)`: Execute shell commands

#### Include System
- `INCLUDE "filename"`: Include code from another file
- `INCLUDE "_library_"`: Include standard library

## Complete List of Keywords and Operators

### Keywords
- `AND` - Logical AND operator
- `APPEND` - File operation to append data
- `ARRAY` - Array data type declaration
- `BOOLEAN` - Boolean data type
- `BYREF` - Parameter passing by reference
- `BYVAL` - Parameter passing by value
- `CALL` - Call a procedure
- `CASE` - Start a case statement
- `CHAR` - Character data type
- `CONSTANT` - Declare a constant
- `DATE` - Date data type
- `DECLARE` - Declare a variable
- `DEF` - Alternative function definition
- `DIV` - Integer division
- `DO` - Used in WHILE and function definitions
- `ELSE` - Alternative branch in IF statement
- `ENDEF` - End of alternative function definition
- `ENDCASE` - End of case statement
- `ENDFUNCTION` - End of function definition
- `ENDIF` - End of IF statement
- `ENDPROCEDURE` - End of procedure definition
- `ENDTYPE` - End of type definition
- `ENDWHILE` - End of WHILE loop
- `FALSE` - Boolean false value
- `FOR` - Start of FOR loop
- `FUNCTION` - Function definition
- `IF` - Conditional statement
- `INCLUDE` - Include external code
- `INPUT` - Read user input
- `INTEGER` - Integer data type
- `MOD` - Modulo operation
- `NEXT` - End of FOR loop iteration
- `NOT` - Logical NOT operator
- `OF` - Used in CASE and ARRAY declarations
- `OR` - Logical OR operator
- `OTHERWISE` - Default case in CASE statement
- `OUTPUT` - Display output
- `PRINT` - Display output
- `PROCEDURE` - Procedure definition
- `READ` - Read data
- `REAL` - Real number data type
- `REM` - Comment
- `REPEAT` - Start of REPEAT loop
- `RETURN` - Return from function
- `RETURNS` - Function return type
- `STEP` - Increment in FOR loop
- `STRING` - String data type
- `THEN` - Used in IF statement
- `TO` - Range in FOR loop
- `TRUE` - Boolean true value
- `TYPE` - User-defined type
- `UNTIL` - Condition in REPEAT loop
- `WHILE` - Start of WHILE loop

### Operators
- `+` - Addition or string concatenation
- `-` - Subtraction
- `*` - Multiplication
- `/` - Division
- `^` - Exponentiation
- `=` - Assignment or equality comparison
- `<>` - Not equal
- `<` - Less than
- `>` - Greater than
- `<=` - Less than or equal
- `>=` - Greater than or equal
- `←` - Assignment (alternative)

## Installation

1. Ensure you have Python 3.7+ installed
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### GUI Version
```bash
python main.py
```

### Using Components Independently
```python
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

## Examples

See the `examples/` directory for sample pseudocode programs.
