import sys
from io import StringIO
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class ConsoleOutput(QTextEdit):
    """Console with separate output display"""
    
    def __init__(self, namespace=None):
        super().__init__()
        self.setReadOnly(True)
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a2e;
                color: #e0e0e0;
                font-family: 'Courier New';
                font-size: 11px;
                border: 1px solid #0f3460;
                border-radius: 5px;
            }
        """)
        
        self.namespace = namespace or {}
        self.namespace['print'] = self.print_output
        self.namespace['display'] = self.print_output
        
        self.prompt = ">>> "
        self.commands = []
        self.history = []
        self.history_pos = 0
        
        self.append(f'<span style="color: #4fc3f7;">Python Console Ready</span>')
        self.append_prompt()
    
    def append_prompt(self):
        self.append(f'<span style="color: #66bb6a;">{self.prompt}</span>')
        self.moveCursor(QTextCursor.MoveOperation.End)
    
    def print_output(self, *args, **kwargs):
        """Redirect print to console"""
        text = ' '.join(str(arg) for arg in args)
        self.append(f'<span style="color: #ffffff;">{text}</span>')
        self.moveCursor(QTextCursor.MoveOperation.End)
    
    def execute_command(self, command):
        """Execute a command"""
        if not command.strip():
            self.append_prompt()
            return
        
        self.history.append(command)
        self.history_pos = len(self.history)
        
        try:
            # Execute in namespace
            result = eval(command, self.namespace)
            if result is not None:
                self.append(f'<span style="color: #ffd54f;">{repr(result)}</span>')
        except Exception as e:
            try:
                # Try executing as statement
                exec(command, self.namespace)
            except Exception as e:
                self.append(f'<span style="color: #ef5350;">Error: {e}</span>')
        
        self.append_prompt()
        self.moveCursor(QTextCursor.MoveOperation.End)
    
    def keyPressEvent(self, event):
        """Handle keyboard input"""
        key = event.key()
        cursor = self.textCursor()
        
        if key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
            # Get last line
            text = self.toPlainText()
            lines = text.split('\n')
            if lines:
                last_line = lines[-1]
                command = last_line[len(self.prompt):] if last_line.startswith(self.prompt) else last_line
                self.commands.append(command)
                self.execute_command(command)
        elif key == Qt.Key.Key_Up:
            if self.history:
                self.history_pos = max(0, self.history_pos - 1)
                self.replace_last_line(self.prompt + self.history[self.history_pos])
        elif key == Qt.Key.Key_Down:
            if self.history and self.history_pos < len(self.history) - 1:
                self.history_pos += 1
                self.replace_last_line(self.prompt + self.history[self.history_pos])
            else:
                self.history_pos = len(self.history)
                self.replace_last_line(self.prompt)
        else:
            super().keyPressEvent(event)
    
    def replace_last_line(self, text):
        """Replace the last line of console"""
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock,
                           QTextCursor.MoveMode.KeepAnchor)
        cursor.removeSelectedText()
        cursor.insertText(text)
        self.moveCursor(QTextCursor.MoveOperation.End)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interactive Console")
        self.setGeometry(100, 100, 800, 600)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Add a label
        label = QLabel("Interactive Python Console")
        label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 5px;")
        layout.addWidget(label)
        
        # Add console
        namespace = {
            'app': self,
            'QMessageBox': QMessageBox,
            'QWidget': QWidget,
        }
        self.console = ConsoleOutput(namespace)
        layout.addWidget(self.console)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())