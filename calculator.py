from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys


class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_expression = ""

    def initUI(self):
        self.setWindowTitle("Modern Calculator")
        self.setGeometry(100, 100, 350, 500)

        layout = QVBoxLayout()

        # Display label with reduced height
        self.display = QLabel("0", self)
        self.display.setFont(QFont("Arial", 20))
        self.display.setStyleSheet("background: #f5f5dc; border: 2px solid #333; padding: 2px; height: 40px;")
        self.display.setAlignment(Qt.AlignRight)
        layout.addWidget(self.display)

        # Grid layout for buttons
        grid_layout = QGridLayout()
        buttons = [
            ('DEL', 0, 0), ('LOG', 0, 1), ('%', 0, 2), ('÷', 0, 3),
            ('1', 1, 0), ('2', 1, 1), ('3', 1, 2), ('×', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('+', 2, 3),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('-', 3, 3),
            ('RESULT', 4, 0), ('0', 4, 1), ('.', 4, 2), ('=', 4, 3)
        ]

        for btn_text, row, col in buttons:
            button = QPushButton(btn_text, self)
            button.setFont(QFont("Arial", 18))
            button.setStyleSheet("background: #d3f8d3; border: 1px solid #333; padding: 10px;")
            button.clicked.connect(lambda checked, text=btn_text: self.on_button_click(text))
            grid_layout.addWidget(button, row, col)

        layout.addLayout(grid_layout)
        self.setLayout(layout)

    def on_button_click(self, button_text):
        if button_text == "DEL":
            self.current_expression = self.current_expression[:-1]
        elif button_text == "RESULT" or button_text == "=":
            try:
                expression = self.current_expression.replace("×", "*").replace("÷", "/")
                self.current_expression = str(eval(expression))
            except Exception:
                self.current_expression = "Error"
        else:
            self.current_expression += button_text

        self.display.setText(self.current_expression if self.current_expression else "0")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculatorApp()
    window.show()
    sys.exit(app.exec_())

