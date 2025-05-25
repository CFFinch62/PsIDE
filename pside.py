#!/usr/bin/env python3
"""
Main entry point for the Pseudocode Interpreter IDE.
"""

import sys
from PyQt6.QtWidgets import QApplication
from pseudocode_interpreter.gui import PseudocodeIDE

def main():
    """Main function to start the application."""
    app = QApplication(sys.argv)
    window = PseudocodeIDE()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 