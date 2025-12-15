import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout
)
from PySide6.QtCore import Qt

class OverlayWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(200, 100)

        layout = QVBoxLayout(self)

        self.label_progresso = QLabel("62/109")
        self.label_progresso.setStyleSheet("""
            QLabel {
                background-color: rgba(30, 30, 30, 220);
                color: #FFFFFF;
                padding: 10px;
                border-radius: 5px;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        self.label_progresso.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.label_progresso)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = OverlayWidget()
    widget.show()

    sys.exit(app.exec())