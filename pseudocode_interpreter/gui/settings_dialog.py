import json
import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, 
                           QLabel, QFontComboBox, QSpinBox, QPushButton, 
                           QColorDialog, QTabWidget, QWidget, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPalette

class SettingsManager:
    """Manages application settings using JSON file storage"""
    
    def __init__(self, settings_file="pside_settings.json"):
        self.settings_file = settings_file
        self.default_settings = {
            "editor": {
                "font_family": "Courier New",
                "font_size": 10,
                "background_color": "#1E1E1E",
                "text_color": "#FFFFFF"
            },
            "output": {
                "font_family": "Courier New", 
                "font_size": 10,
                "background_color": "#1E1E1E",
                "text_color": "#90EE90"
            }
        }
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from JSON file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults to handle missing keys
                    settings = self.default_settings.copy()
                    settings.update(loaded_settings)
                    # Ensure nested dictionaries are properly merged
                    for section in ["editor", "output"]:
                        if section in loaded_settings:
                            settings[section].update(loaded_settings[section])
                    return settings
            else:
                return self.default_settings.copy()
        except Exception as e:
            print(f"Error loading settings: {e}")
            return self.default_settings.copy()
    
    def save_settings(self):
        """Save settings to JSON file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get_editor_settings(self):
        """Get editor-specific settings"""
        return self.settings["editor"]
    
    def get_output_settings(self):
        """Get output console-specific settings"""
        return self.settings["output"]
    
    def update_editor_settings(self, **kwargs):
        """Update editor settings"""
        self.settings["editor"].update(kwargs)
    
    def update_output_settings(self, **kwargs):
        """Update output settings"""
        self.settings["output"].update(kwargs)

class ColorButton(QPushButton):
    """Custom button for color selection"""
    
    def __init__(self, color="#FFFFFF"):
        super().__init__()
        self.color = QColor(color)
        self.setFixedSize(50, 30)
        self.update_button_color()
        self.clicked.connect(self.choose_color)
    
    def update_button_color(self):
        """Update button appearance to show selected color"""
        self.setStyleSheet(f"background-color: {self.color.name()}; border: 1px solid #666;")
    
    def choose_color(self):
        """Open color dialog to choose new color"""
        color = QColorDialog.getColor(self.color, self, "Choose Color")
        if color.isValid():
            self.color = color
            self.update_button_color()
    
    def get_color(self):
        """Get the selected color as hex string"""
        return self.color.name()
    
    def set_color(self, color_str):
        """Set color from hex string"""
        self.color = QColor(color_str)
        self.update_button_color()

class SettingsDialog(QDialog):
    """Settings dialog for configuring editor and output appearance"""
    
    def __init__(self, settings_manager, parent=None):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.setWindowTitle("PsIDE Settings")
        self.setModal(True)
        self.setFixedSize(500, 400)
        
        self.init_ui()
        self.load_current_settings()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # Editor tab
        editor_tab = QWidget()
        self.setup_editor_tab(editor_tab)
        tab_widget.addTab(editor_tab, "Code Editor")
        
        # Output tab
        output_tab = QWidget()
        self.setup_output_tab(output_tab)
        tab_widget.addTab(output_tab, "Output Console")
        
        layout.addWidget(tab_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        # Reset to defaults button
        reset_button = QPushButton("Reset to Defaults")
        reset_button.clicked.connect(self.reset_to_defaults)
        button_layout.addWidget(reset_button)
        
        button_layout.addStretch()
        
        # Cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        # OK button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept_settings)
        ok_button.setDefault(True)
        button_layout.addWidget(ok_button)
        
        layout.addLayout(button_layout)
    
    def setup_editor_tab(self, tab):
        """Setup the editor settings tab"""
        layout = QVBoxLayout(tab)
        
        # Font settings group
        font_group = QGroupBox("Font Settings")
        font_layout = QVBoxLayout(font_group)
        
        # Font family
        font_family_layout = QHBoxLayout()
        font_family_layout.addWidget(QLabel("Font Family:"))
        self.editor_font_combo = QFontComboBox()
        font_family_layout.addWidget(self.editor_font_combo)
        font_layout.addLayout(font_family_layout)
        
        # Font size
        font_size_layout = QHBoxLayout()
        font_size_layout.addWidget(QLabel("Font Size:"))
        self.editor_font_size = QSpinBox()
        self.editor_font_size.setRange(6, 72)
        font_size_layout.addWidget(self.editor_font_size)
        font_size_layout.addStretch()
        font_layout.addLayout(font_size_layout)
        
        layout.addWidget(font_group)
        
        # Color settings group
        color_group = QGroupBox("Color Settings")
        color_layout = QVBoxLayout(color_group)
        
        # Background color
        bg_color_layout = QHBoxLayout()
        bg_color_layout.addWidget(QLabel("Background Color:"))
        self.editor_bg_color = ColorButton()
        bg_color_layout.addWidget(self.editor_bg_color)
        bg_color_layout.addStretch()
        color_layout.addLayout(bg_color_layout)
        
        # Text color
        text_color_layout = QHBoxLayout()
        text_color_layout.addWidget(QLabel("Text Color:"))
        self.editor_text_color = ColorButton()
        text_color_layout.addWidget(self.editor_text_color)
        text_color_layout.addStretch()
        color_layout.addLayout(text_color_layout)
        
        layout.addWidget(color_group)
        layout.addStretch()
    
    def setup_output_tab(self, tab):
        """Setup the output console settings tab"""
        layout = QVBoxLayout(tab)
        
        # Font settings group
        font_group = QGroupBox("Font Settings")
        font_layout = QVBoxLayout(font_group)
        
        # Font family
        font_family_layout = QHBoxLayout()
        font_family_layout.addWidget(QLabel("Font Family:"))
        self.output_font_combo = QFontComboBox()
        font_family_layout.addWidget(self.output_font_combo)
        font_layout.addLayout(font_family_layout)
        
        # Font size
        font_size_layout = QHBoxLayout()
        font_size_layout.addWidget(QLabel("Font Size:"))
        self.output_font_size = QSpinBox()
        self.output_font_size.setRange(6, 72)
        font_size_layout.addWidget(self.output_font_size)
        font_size_layout.addStretch()
        font_layout.addLayout(font_size_layout)
        
        layout.addWidget(font_group)
        
        # Color settings group
        color_group = QGroupBox("Color Settings")
        color_layout = QVBoxLayout(color_group)
        
        # Background color
        bg_color_layout = QHBoxLayout()
        bg_color_layout.addWidget(QLabel("Background Color:"))
        self.output_bg_color = ColorButton()
        bg_color_layout.addWidget(self.output_bg_color)
        bg_color_layout.addStretch()
        color_layout.addLayout(bg_color_layout)
        
        # Text color
        text_color_layout = QHBoxLayout()
        text_color_layout.addWidget(QLabel("Text Color:"))
        self.output_text_color = ColorButton()
        text_color_layout.addWidget(self.output_text_color)
        text_color_layout.addStretch()
        color_layout.addLayout(text_color_layout)
        
        layout.addWidget(color_group)
        layout.addStretch()
    
    def load_current_settings(self):
        """Load current settings into the dialog"""
        editor_settings = self.settings_manager.get_editor_settings()
        output_settings = self.settings_manager.get_output_settings()
        
        # Editor settings
        self.editor_font_combo.setCurrentText(editor_settings["font_family"])
        self.editor_font_size.setValue(editor_settings["font_size"])
        self.editor_bg_color.set_color(editor_settings["background_color"])
        self.editor_text_color.set_color(editor_settings["text_color"])
        
        # Output settings
        self.output_font_combo.setCurrentText(output_settings["font_family"])
        self.output_font_size.setValue(output_settings["font_size"])
        self.output_bg_color.set_color(output_settings["background_color"])
        self.output_text_color.set_color(output_settings["text_color"])
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        reply = QMessageBox.question(
            self, "Reset Settings",
            "Are you sure you want to reset all settings to their defaults?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Reset to default settings
            self.settings_manager.settings = self.settings_manager.default_settings.copy()
            self.load_current_settings()
    
    def accept_settings(self):
        """Accept and save the settings"""
        # Update editor settings
        self.settings_manager.update_editor_settings(
            font_family=self.editor_font_combo.currentText(),
            font_size=self.editor_font_size.value(),
            background_color=self.editor_bg_color.get_color(),
            text_color=self.editor_text_color.get_color()
        )
        
        # Update output settings
        self.settings_manager.update_output_settings(
            font_family=self.output_font_combo.currentText(),
            font_size=self.output_font_size.value(),
            background_color=self.output_bg_color.get_color(),
            text_color=self.output_text_color.get_color()
        )
        
        # Save settings to file
        if self.settings_manager.save_settings():
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Failed to save settings!") 