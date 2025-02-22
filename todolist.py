import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QListWidget,
    QListWidgetItem, QFrame, QSizePolicy, QMessageBox,
    QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QFont, QColor

class TodoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enhanced To-Do List")
        # Reduced width, but still tall enough
        self.setGeometry(300, 100, 600, 800)
        self.tasks = []  # Each task: {"title": str, "completed": bool}

        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        main_layout = QVBoxLayout()
        # Generous margins and spacing to avoid truncation
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(40)

        # Title
        title_label = QLabel("My Tasks")
        title_label.setFont(QFont("Arial", 26))
        main_layout.addWidget(title_label, alignment=Qt.AlignLeft)

        # Input area
        input_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("What do you need to do?")
        self.task_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.task_input.setFixedHeight(45)
        input_layout.addWidget(self.task_input)

        self.add_button = QPushButton("Add Task")
        self.add_button.setFixedHeight(45)
        self.add_button.clicked.connect(self.add_task)
        input_layout.addWidget(self.add_button)
        main_layout.addLayout(input_layout)

        # Active tasks section
        active_label = QLabel("Active Tasks")
        active_label.setFont(QFont("Arial", 18))
        main_layout.addWidget(active_label, alignment=Qt.AlignLeft)

        self.task_list = QListWidget()
        # Increased spacing to avoid overlap
        self.task_list.setSpacing(35)
        main_layout.addWidget(self.task_list)

        # Completed tasks section
        completed_label = QLabel("Completed")
        completed_label.setFont(QFont("Arial", 18))
        main_layout.addWidget(completed_label, alignment=Qt.AlignLeft)

        self.completed_list = QListWidget()
        self.completed_list.setSpacing(35)
        main_layout.addWidget(self.completed_list)

        self.setLayout(main_layout)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                             stop:0 #cfd8dc, stop:1 #90a4ae);
            }
            QLabel {
                color: #1c313a;
            }
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border: 2px solid #90a4ae;
                border-radius: 12px;
                background-color: #ffffff;
                color: #1c313a;
            }
            QPushButton {
                font-size: 14px;
                font-weight: normal;
                background-color: #00796b;
                color: #ffffff;
                border: none;
                border-radius: 12px;
                padding: 0 25px;
                transition: background-color 0.3s;
            }
            QPushButton:hover {
                background-color: #00695c;
            }
            QPushButton:pressed {
                background-color: #004d40;
            }
            QListWidget {
                background-color: transparent;
                border: none;
            }
            /* Task Card Styling */
            QFrame#TaskCard {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 15px;
                padding: 20px;
            }
            QFrame#TaskCard:hover {
                border: 1px solid #4fc3f7;
            }
            /* Checkbox Styling */
            QPushButton#Checkbox {
                background-color: #ffffff;
                border: 2px solid #00796b;
                border-radius: 14px;
            }
            QPushButton#Checkbox:checked {
                background-color: #43a047;
                border: 2px solid #43a047;
            }
        """)

    def add_task(self):
        task_text = self.task_input.text().strip()
        if not task_text:
            return
        task = {"title": task_text, "completed": False}
        self.tasks.append(task)
        self.update_task_list()
        self.task_input.clear()

    def update_task_list(self):
        self.task_list.clear()
        self.completed_list.clear()
        for task in self.tasks:
            if not task["completed"]:
                self.create_task_card(task["title"], self.task_list, task)
            else:
                self.create_task_card(task["title"], self.completed_list, task, completed=True)

    def create_task_card(self, text, list_widget, task_data, completed=False):
        item = QListWidgetItem()
        card_frame = QFrame()
        card_frame.setObjectName("TaskCard")
        card_layout = QHBoxLayout(card_frame)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(30)

        # Drop shadow effect
        shadow = QGraphicsDropShadowEffect(card_frame)
        shadow.setBlurRadius(25)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 100))
        card_frame.setGraphicsEffect(shadow)

        # Checkbox toggle button
        checkbox = QPushButton()
        checkbox.setObjectName("Checkbox")
        checkbox.setCheckable(True)
        checkbox.setFixedSize(30, 30)
        checkbox.setChecked(completed)
        checkbox.clicked.connect(lambda: self.toggle_task(task_data))
        card_layout.addWidget(checkbox)

        # Task label
        task_label = QLabel(text)
        task_label.setFont(QFont("Arial", 16))
        task_label.setStyleSheet("color: #1c313a;")
        task_label.setWordWrap(True)
        task_label.setMinimumWidth(250)
        card_layout.addWidget(task_label)

        card_layout.addStretch()
        card_frame.setLayout(card_layout)

        # "Pop" animation
        animation = QPropertyAnimation(card_frame, b"geometry")
        animation.setDuration(300)
        animation.setEasingCurve(QEasingCurve.OutBounce)
        current_geom = card_frame.geometry()
        animation.setStartValue(QRect(current_geom.x(), current_geom.y(), current_geom.width(), 0))
        animation.setEndValue(current_geom)
        animation.start()

        # Increase item height
        size = card_frame.sizeHint()
        size.setHeight(size.height() + 30)
        item.setSizeHint(size)

        list_widget.addItem(item)
        list_widget.setItemWidget(item, card_frame)

    def toggle_task(self, task_data):
        task_data["completed"] = not task_data["completed"]
        self.update_task_list()
        if task_data["completed"]:
            QMessageBox.information(self, "Congratulations", "Congrats, you have done the task!")
        else:
            QMessageBox.information(self, "Keep Going", "You need to complete the task!")

def main():
    app = QApplication(sys.argv)
    window = TodoApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

