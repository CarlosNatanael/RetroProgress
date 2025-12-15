import sys
import requests
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout
)
from PySide6.QtCore import Qt, QTimer
try:
    from config import RA_USER, RA_API_KEY
except ImportError:
    RA_USER = None
    RA_API_KEY = None

RA_GAME_ID = 724
UPDATE_INTERVAL_MS = 30000

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
        self.label_progresso = QLabel("Aguardando RA...") # Texto inicial
        
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

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(UPDATE_INTERVAL_MS)
        self.update_progress()

    def update_progress(self):
        try:
            url = "https://retroachievements.org/API/API_GetGameInfoAndUserProgress.php"
            params = {
                'g': RA_GAME_ID,
                'u': RA_USER,
                'y': RA_API_KEY
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            unlocked = data.get('NumAchieved', 0)
            total = data.get('NumAchievements', 0)

            self.label_progresso.setText(f"🏆 {unlocked}/{total}")

        except requests.exceptions.RequestException as e:
            print(f"Erro ao carregar dados do RA: {e}")
            self.label_progresso.setText("ERRO")
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = OverlayWidget()
    widget.show()
    sys.exit(app.exec())