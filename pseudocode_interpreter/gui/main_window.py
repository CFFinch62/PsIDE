import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QTextEdit, QPushButton, QFileDialog, QSplitter, 
                           QMenuBar, QMenu, QStatusBar, QDialog, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QAction, QKeySequence

from ..core import Lexer, Parser, Interpreter, Variable
from .highlighter import PseudocodeHighlighter
from .dialogs import InputDialog
from .settings_dialog import SettingsManager, SettingsDialog

# Main Application Window
class PseudocodeIDE(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize settings manager
        self.settings_manager = SettingsManager()
        
        # Window properties
        self.setWindowTitle("PSIDE - PSeudocode Interpreter Development Environment")
        self.setGeometry(100, 100, 1000, 700)
        
        # Current file path
        self.current_file = None
        self.cwd = os.getcwd()
        
        # Create interpreter
        self.interpreter = Interpreter()
        self.interpreter.cwd = self.cwd
        
        # Initialize UI
        self.init_ui()
        
        # Apply initial settings
        self.apply_settings()
        
    def init_ui(self):
        """Initialize the user interface"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create splitter for code editor and output
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Code editor
        self.code_editor = QTextEdit()
        self.code_editor.setFont(QFont("Courier New", 10))
        self.code_editor.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.code_editor.setPlaceholderText("Enter your pseudocode here...")
        
        # Apply syntax highlighting
        self.highlighter = PseudocodeHighlighter(self.code_editor.document())
        
        splitter.addWidget(self.code_editor)
        
        # Output console
        self.output_console = QTextEdit()
        self.output_console.setFont(QFont("Courier New", 10))
        self.output_console.setReadOnly(True)
        self.output_console.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.output_console.setPlaceholderText("Output will appear here...")
        
        splitter.addWidget(self.output_console)
        
        # Set initial sizes for the splitter (70% code editor, 30% output)
        splitter.setSizes([700, 300])
        
        main_layout.addWidget(splitter)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Run button
        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.run_code)
        button_layout.addWidget(self.run_button)
        
        # Clear output button
        self.clear_button = QPushButton("Clear Output")
        self.clear_button.clicked.connect(self.clear_output)
        button_layout.addWidget(self.clear_button)
        
        main_layout.addLayout(button_layout)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
    def create_menu_bar(self):
        """Create the menu bar with all actions"""
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("&File")
        
        # New action
        new_action = QAction("&New", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        # Open action
        open_action = QAction("&Open", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        # Save action
        save_action = QAction("&Save", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        # Save As action
        save_as_action = QAction("Save &As", self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menu_bar.addMenu("&Edit")
        
        # Undo action
        undo_action = QAction("&Undo", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.triggered.connect(self.code_editor.undo)
        edit_menu.addAction(undo_action)
        
        # Redo action
        redo_action = QAction("&Redo", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.triggered.connect(self.code_editor.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        # Cut action
        cut_action = QAction("Cu&t", self)
        cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        cut_action.triggered.connect(self.code_editor.cut)
        edit_menu.addAction(cut_action)
        
        # Copy action
        copy_action = QAction("&Copy", self)
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        copy_action.triggered.connect(self.code_editor.copy)
        edit_menu.addAction(copy_action)
        
        # Paste action
        paste_action = QAction("&Paste", self)
        paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        paste_action.triggered.connect(self.code_editor.paste)
        edit_menu.addAction(paste_action)
        
        # Run menu
        run_menu = menu_bar.addMenu("&Run")
        
        # Run action
        run_action = QAction("&Run", self)
        run_action.setShortcut("F5")
        run_action.triggered.connect(self.run_code)
        run_menu.addAction(run_action)
        
        # Clear output action
        clear_action = QAction("&Clear Output", self)
        clear_action.triggered.connect(self.clear_output)
        run_menu.addAction(clear_action)
        
        # View menu
        view_menu = menu_bar.addMenu("&View")
        
        # Settings action
        settings_action = QAction("&Settings", self)
        settings_action.triggered.connect(self.open_settings)
        view_menu.addAction(settings_action)
        
        # Help menu
        help_menu = menu_bar.addMenu("&Help")
        
        # About action
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def new_file(self):
        """Create a new, empty file"""
        # Check if current file has unsaved changes
        if self.code_editor.document().isModified():
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "Do you want to save changes to the current file?",
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Save:
                self.save_file()
            elif reply == QMessageBox.StandardButton.Cancel:
                return
                
        # Clear the editor
        self.code_editor.clear()
        self.code_editor.document().setModified(False)
        self.current_file = None
        self.setWindowTitle("Pseudocode Interpreter")
        self.status_bar.showMessage("New file created")
        
    def open_file(self):
        """Open a file and load its contents into the editor"""
        # Check if current file has unsaved changes
        if self.code_editor.document().isModified():
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "Do you want to save changes to the current file?",
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Save:
                self.save_file()
            elif reply == QMessageBox.StandardButton.Cancel:
                return
                
        # Show file dialog to select a file
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "All Files (*);;Text Files (*.txt);;Pseudocode Files (*.pseudo)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    
                self.code_editor.setPlainText(content)
                self.code_editor.document().setModified(False)
                self.current_file = file_path
                self.cwd = os.path.dirname(os.path.abspath(file_path))
                self.interpreter.cwd = self.cwd
                self.setWindowTitle(f"Pseudocode Interpreter - {os.path.basename(file_path)}")
                self.status_bar.showMessage(f"Opened {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open file: {str(e)}")
                
    def save_file(self):
        """Save the current file"""
        if self.current_file:
            try:
                with open(self.current_file, 'w') as file:
                    file.write(self.code_editor.toPlainText())
                    
                self.code_editor.document().setModified(False)
                self.status_bar.showMessage(f"Saved {self.current_file}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
        else:
            self.save_file_as()
            
    def save_file_as(self):
        """Save the current file with a new name"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save File As", "", "All Files (*);;Text Files (*.txt);;Pseudocode Files (*.pseudo)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(self.code_editor.toPlainText())
                    
                self.code_editor.document().setModified(False)
                self.current_file = file_path
                self.cwd = os.path.dirname(os.path.abspath(file_path))
                self.interpreter.cwd = self.cwd
                self.setWindowTitle(f"Pseudocode Interpreter - {os.path.basename(file_path)}")
                self.status_bar.showMessage(f"Saved as {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
                
    def run_code(self):
        """Execute the code in the editor"""
        code = self.code_editor.toPlainText()
        
        if not code.strip():
            self.status_bar.showMessage("No code to run")
            return
            
        self.status_bar.showMessage("Running code...")
        self.output_console.clear()
        
        try:
            # Create a custom version of input function for GUI dialogs
            original_input = self.interpreter.visit_input
            
            def gui_input(node):
                # Get variable name from node
                var_name = node.name
                
                # Create input dialog
                dialog = InputDialog("", self)
                result = ""
                
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    result = dialog.get_input()
                else:
                    # User canceled, return empty string
                    result = ""
                    
                # Try to convert to number if possible
                try:
                    value = Variable(float(result))
                except ValueError:
                    value = Variable(result)
                    
                # Store the input value in the variable
                self.interpreter.current_symbol_table.set(var_name, value)
                
                return value
                    
            # Replace input function
            self.interpreter.visit_input = gui_input
            
            # Tokenize the code
            lexer = Lexer(code)
            tokens = lexer.generate_tokens()
            
            # Parse the tokens into an AST
            parser = Parser(tokens)
            ast = parser.parse()
            
            # Execute the AST
            result = self.interpreter.interpret(ast)
            
            # Display the output
            if self.interpreter.output_text:
                self.output_console.insertPlainText(self.interpreter.output_text)
                
            # Add the result if it's not empty
            if result and str(result) != '0.0':
                self.output_console.insertPlainText(f"\nResult: {result}\n")
                
            self.status_bar.showMessage("Code executed successfully")
            
        except Exception as e:
            self.output_console.insertPlainText(f"Error: {str(e)}\n")
            self.status_bar.showMessage(f"Error executing code: {str(e)}")
            
        finally:
            # Restore original input function
            if 'original_input' in locals():
                self.interpreter.visit_input = original_input
                
    def clear_output(self):
        """Clear the output console"""
        self.output_console.clear()
        self.status_bar.showMessage("Output cleared")
        
    def show_about(self):
        """Show the about dialog"""
        QMessageBox.about(
            self,
            "About PsIDE",
            "PsIDE - Psuedocode Interpreter Development Environment\n\n"
            "A simple IDE for writing and executing pseudocode."
            "This application allows you to write pseudocode with syntax highlighting, "
            "execute it, and see the output in real-time.\n\n"
            "(c) 2025 Chuck Finch - Fragillidae Software\n\n"
            "Version 1.0.1"
        )
    
    def open_settings(self):
        """Open the settings dialog"""
        dialog = SettingsDialog(self.settings_manager, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Settings were saved, apply them
            self.apply_settings()
            self.status_bar.showMessage("Settings applied")
    
    def apply_settings(self):
        """Apply current settings to the editor and output console"""
        editor_settings = self.settings_manager.get_editor_settings()
        output_settings = self.settings_manager.get_output_settings()
        
        # Apply editor settings
        editor_font = QFont(editor_settings["font_family"], editor_settings["font_size"])
        self.code_editor.setFont(editor_font)
        self.code_editor.setStyleSheet(
            f"background-color: {editor_settings['background_color']}; "
            f"color: {editor_settings['text_color']};"
        )
        
        # Apply output settings
        output_font = QFont(output_settings["font_family"], output_settings["font_size"])
        self.output_console.setFont(output_font)
        self.output_console.setStyleSheet(
            f"background-color: {output_settings['background_color']}; "
            f"color: {output_settings['text_color']};"
        ) 