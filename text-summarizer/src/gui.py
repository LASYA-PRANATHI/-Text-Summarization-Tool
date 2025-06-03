import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QSpinBox, QMessageBox
)
from PySide6.QtCore import Qt
from src.summarizer import TextSummarizer

class SummarizerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.summarizer = TextSummarizer()

    def initUI(self):
        self.setWindowTitle('Text Summarizer')
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Input area
        input_layout = QHBoxLayout()
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Paste or type text here...")
        input_layout.addWidget(self.input_text)
        
        # Sentence count selector
        self.sentence_count = QSpinBox()
        self.sentence_count.setMinimum(1)
        self.sentence_count.setMaximum(10)
        self.sentence_count.setValue(3)
        input_layout.addWidget(self.sentence_count)
        
        layout.addLayout(input_layout)
        
        # Generate button
        self.generate_btn = QPushButton('Generate Summary')
        self.generate_btn.clicked.connect(self.generate_summary)
        layout.addWidget(self.generate_btn)
        
        # Output area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

    def generate_summary(self):
        try:
            input_text = self.input_text.toPlainText()
            if not input_text.strip():
                QMessageBox.warning(self, "Error", "Please enter some text")
                return
            
            num_sentences = self.sentence_count.value()
            summary = self.summarizer.get_summary(input_text, num_sentences)
            self.output_text.setText(summary)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SummarizerGUI()
    window.show()
    sys.exit(app.exec())