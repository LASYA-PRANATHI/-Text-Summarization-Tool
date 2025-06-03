import sys
import os

# Add the parent directory to Python's path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui import SummarizerGUI
from PySide6.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SummarizerGUI()
    window.show()
    sys.exit(app.exec())