import sys
import requests
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QHBoxLayout
)
from PySide6.QtCore import Qt, QTimer, QUrl, QByteArray
from PySide6.QtGui import QPixmap
from io import BytesIO
try:
    from config import RA_USER, RA_API_KEY
except ImportError:
    RA_USER = None
    RA_API_KEY = None

# --- CONFIG ---
UPDATE_INTERVAL_MS = 30000
RA_BASE_URL = "https://retroachievements.org/API"
RA_IMG_BASE = "https://media.retroachievements.org"

class OverlayWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.current_game_id = 0

        # Configurações de Janela (Sempre no topo, sem moldura, transparente)
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        main_layout = QHBoxLayout(self)
        
        self.label_emblema = QLabel()
        self.label_emblema.setFixedSize(64, 64)
        self.label_emblema.setStyleSheet("background-color: transparent;")
        main_layout.addWidget(self.label_emblema)
        
        self.label_progresso = QLabel("Iniciando RetroProgress...")
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
        main_layout.addWidget(self.label_progresso)

        self.setLayout(main_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(UPDATE_INTERVAL_MS)

        self.update_progress()

    def _fetch_and_set_emblen(self, icon_path):
        if not icon_path:
            self.label_emblema.clear()
            return

        image_url = f"{RA_IMG_BASE}{icon_path}"
        try:
            response = requests.get(image_url, timeout=5)
            response.raise_for_status()
            
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray(response.content))

            scaled_pixmap = pixmap.scaled(
                self.label_emblema.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            self.label_emblema.setPixmap(scaled_pixmap)
        
        except requests.exceptions.RequestException as e:
            print(f"Erro ao baixar emblema: {e}")
            self.label_emblema.setText("X")
        
    def update_progress(self):
        try:
            summary_url = f"{RA_BASE_URL}/API_GetUserSummary.php"
            summary_params = {'z': RA_USER, 'y': RA_API_KEY, 'u': RA_USER}
            
            summary_response = requests.get(summary_url, params=summary_params, timeout=10)
            summary_response.raise_for_status()
            summary_data = summary_response.json()
            
            last_game_id = summary_data.get('LastGameID')
            
            if not last_game_id or int(last_game_id) == 0:
                self.label_progresso.setText("Nenhum jogo em progresso.")
                self.label_emblema.clear()
                return

            self.current_game_id = last_game_id
            progress_url = f"{RA_BASE_URL}/API_GetGameInfoAndUserProgress.php"
            progress_params = {
                'g': self.current_game_id, 
                'u': RA_USER,
                'z': RA_USER,
                'y': RA_API_KEY
            }
            progress_response = requests.get(progress_url, params=progress_params, timeout=10)
            progress_response.raise_for_status()
            progress_data = progress_response.json()
            
            unlocked = progress_data.get('NumAchieved', 0)
            total = progress_data.get('NumAchievements', 0)

            game_title = progress_data.get('Title', 'Jogo Desconhecido')

            self.label_progresso.setText(f"{game_title}\n {unlocked}/{total}")

            icon_path = progress_data.get('ImageIcon')
            self._fetch_and_set_emblen(icon_path)

            self.adjustSize()
        
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão API: {e}")
            self.label_progresso.setText("ERRO: Verifique a conexão, Usuario ou API Key.")
        except Exception as e:
            print(f"Erro inesperado: {e}")
            self.label_progresso.setText("ERRO")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPosition().toPoint() - self.dragPos
            self.move(self.pos() + delta)

            self.dragPos = event.globalPosition().toPoint()
            event.accept()
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = None
            event.accept()

if __name__ == "__main__":
    if not RA_USER or not RA_API_KEY:
        print("Erro: configure RA_USER e RA_API_KEY")

    app = QApplication(sys.argv)
    widget = OverlayWidget()
    widget.show()
    sys.exit(app.exec())