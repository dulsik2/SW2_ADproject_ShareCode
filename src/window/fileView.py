# editor.py

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QDialog, QFileDialog
from PyQt5.QtWidgets import QLineEdit, QPushButton, QLabel, QMessageBox, QComboBox, QListWidgetItem, QPlainTextEdit
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout

import src.session as session
import syntax

class FileViewWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.show()

    def initUI(self):
        editor = QPlainTextEdit()
        editor.setStyleSheet("""
            QPlainTextEdit{
                font-family:'Consolas';
                color: #ccc;
                background-color: #2b2b2b;
                font-size: 10pt;
            }
        """)
        highlight = syntax.PythonHighlighter(editor.document())
        editor.setPlainText(session.contents)

        main_vbox = QVBoxLayout()
        main_vbox.setContentsMargins(0, 0, 0, 0)
        main_vbox.addWidget(editor)
        self.setLayout(main_vbox)
        self.setWindowTitle("File")
        self.setGeometry(400, 100, 1000, 700)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileViewWindow()
    sys.exit(app.exec_())