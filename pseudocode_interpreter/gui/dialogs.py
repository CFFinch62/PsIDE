from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

# Custom Input Dialog for the INPUT command
class InputDialog(QDialog):
    def __init__(self, prompt, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Input Required")
        
        layout = QVBoxLayout()
        
        # Add prompt label
        self.prompt_label = QLabel(prompt)
        layout.addWidget(self.prompt_label)
        
        # Add input field
        self.input_field = QLineEdit()
        layout.addWidget(self.input_field)
        
        # Add buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def get_input(self):
        return self.input_field.text() 