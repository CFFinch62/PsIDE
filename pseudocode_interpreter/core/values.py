# Value Classes for the Interpreter
class Number:
    def __init__(self, value: float = 0.0):
        self.value = value
        self.is_return = False

    def __repr__(self):
        # Display integers without decimal places
        if self.value == int(self.value):
            return str(int(self.value))
        else:
            return str(self.value)

    def __eq__(self, other):
        if isinstance(other, Number):
            return self.value == other.value
        return False

class String:
    def __init__(self, value: str = ""):
        self.value = value

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, String):
            return self.value == other.value
        return False

class List:
    def __init__(self, values=None):
        self.values = values or []

    def __repr__(self):
        return f"[{', '.join(str(value) for value in self.values)}]"

    def __eq__(self, other):
        if isinstance(other, List):
            if len(self.values) != len(other.values):
                return False
            for i in range(len(self.values)):
                if self.values[i] != other.values[i]:
                    return False
            return True
        return False

class Function:
    def __init__(self, name="", args_node=None, body_node=None, return_node=None):
        self.name = name
        self.args_node = args_node
        self.body_node = body_node
        self.return_node = return_node

    def __repr__(self):
        return f"<function {self.name}>"

# Symbol Table for variables
class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def get(self, name):
        """Get a variable from the symbol table or parent tables"""
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise Exception(f"Variable '{name}' not defined")

    def set(self, name, value):
        """Set a variable in the symbol table"""
        self.symbols[name] = value
        return value

    def remove(self, name):
        """Remove a variable from the symbol table"""
        if name in self.symbols:
            del self.symbols[name]

    def has(self, name):
        """Check if a variable exists"""
        if name in self.symbols:
            return True
        elif self.parent:
            return self.parent.has(name)
        else:
            return False
            
    def create_child_table(self):
        """Create a new symbol table with this table as parent"""
        return SymbolTable(self)

# Variable class - wrapper for all value types
class Variable:
    def __init__(self, value=None):
        self.value = value
        self.type = "number"  # Default type
        self.is_boolean = False
        self.boolean_name = None

        # Determine type safely
        if value is not None:
            self.type = self._determine_type(value)

    def _determine_type(self, value):
        if isinstance(value, Number):
            return "number"
        elif isinstance(value, String):
            return "string"
        elif isinstance(value, List):
            return "list"
        elif isinstance(value, Function):
            return "function"
        elif isinstance(value, (int, float)):
            self.value = Number(float(value))
            return "number"
        elif isinstance(value, str):
            self.value = String(value)
            return "string"
        elif isinstance(value, list):
            # Convert each item to Variable, but avoid infinite recursion
            items = []
            for item in value:
                if isinstance(item, Variable):
                    items.append(item)
                else:
                    # Create Variable directly without recursion
                    var = Variable()
                    if isinstance(item, (int, float)):
                        var.value = Number(float(item))
                        var.type = "number"
                    elif isinstance(item, str):
                        var.value = String(item)
                        var.type = "string"
                    else:
                        var.value = Number(0.0)
                        var.type = "number"
                    items.append(var)
            self.value = List(items)
            return "list"
        else:
            self.value = Number(0.0)
            return "number"

    def copy(self):
        """Create a deep copy of this Variable"""
        import copy as copy_module
        new_var = Variable()
        new_var.type = self.type
        new_var.is_boolean = self.is_boolean
        new_var.boolean_name = self.boolean_name
        
        # Deep copy the value based on type
        if self.type == "number":
            new_var.value = Number(self.value.value)
        elif self.type == "string":
            new_var.value = String(self.value.value)
        elif self.type == "list":
            # Deep copy list values
            new_values = []
            for item in self.value.values:
                if hasattr(item, 'copy'):
                    new_values.append(item.copy())
                else:
                    new_values.append(copy_module.deepcopy(item))
            new_var.value = List(new_values)
        elif self.type == "function":
            # Functions are immutable, so we can share the reference
            new_var.value = self.value
        else:
            new_var.value = copy_module.deepcopy(self.value)
            
        return new_var

    def __repr__(self):
        if self.is_boolean and self.boolean_name:
            return self.boolean_name
        return str(self.value)

    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.value == other.value
        return False