import sys
import requests
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QHBoxLayout, QDialog, QLineEdit, QPushButton, QFormLayout, QMessageBox
)
from PySide6.QtCore import Qt, QTimer, QByteArray
from utilidades_config import load_credentials, save_credentials, clear_credentials
from PySide6.QtGui import QPixmap

# --- CONFIG ---
UPDATE_INTERVAL_MS = 5000
RA_BASE_URL = "https://retroachievements.org/API"
RA_IMG_BASE = "https://media.retroachievements.org"

class ConfigWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("RetroProgress - Configuração")
        self.setFixedSize(350, 250)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setStyleSheet("""
            QDialog {
                background-color: #1f1f1f;
                border: 1px solid #444444;
                border-radius: 8px;
            }
            QLabel {
                color: #e0e0e0;
                font-weight: bold;
                padding-top: 5px;
            }
            QLineEdit {
                background-color: #2c2c2c;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #1a73e8;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 15px;
            }
            QPushButton:hover {
                background-color: #0b50a3;
            }
        """)

        layout = QFormLayout(self)
        layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        
        title_label = QLabel("RetroProgress - Configuração de API")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; margin-bottom: 10px; color: #1a73e8;")
        layout.addRow(title_label)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Seu nome de Usuário RA")
        layout.addRow(QLabel("Usuário RA:"), self.user_input)

        self.key_input = QLineEdit()
        self.key_input.setEchoMode(QLineEdit.Password)
        self.key_input.setPlaceholderText("Sua chave de API RA")
        layout.addRow(QLabel("API Key:"), self.key_input)

        self.save_button = QPushButton("Salvar e Iniciar")
        self.save_button.clicked.connect(self.save_and_start)
        layout.addRow(self.save_button)

        user, _ = load_credentials()
        if user:
             self.user_input.setText(user)

    def save_and_start(self):
        user = self.user_input.text().strip()
        key = self.key_input.text().strip()

        if not user or not key:
            QMessageBox.warning(self, "Erro", "Usuário e Chave API devem ser preenchidos.")
            return
        
        save_credentials(user, key)
        self.accept()

class OverlayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        main_layout = QHBoxLayout(self)
        self.label_emblema = QLabel()
        self.label_emblema.setFixedSize(64, 64)
        main_layout.addWidget(self.label_emblema)
        
        self.label_progresso = QLabel("Carregando...")
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

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(UPDATE_INTERVAL_MS)
        self.update_progress()

    def _fetch_and_set_emblen(self, icon_path):
        if not icon_path:
            self.label_emblema.clear()
            return
        try:
            response = requests.get(f"{RA_IMG_BASE}{icon_path}", timeout=5)
            response.raise_for_status()
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray(response.content))
            self.label_emblema.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        except:
            self.label_emblema.setText("X")
        
    def update_progress(self):
        try:
            summary_params = {'z': RA_USER, 'y': RA_API_KEY, 'u': RA_USER}
            summary_response = requests.get(f"{RA_BASE_URL}/API_GetUserSummary.php", params=summary_params, timeout=10)
            summary_data = summary_response.json()
            last_game_id = summary_data.get('LastGameID')

            if not last_game_id or int(last_game_id) == 0:
                self.label_progresso.setText("Nenhum jogo ativo")
                self.label_emblema.clear()
                return
            
            progress_params = {'g': last_game_id, 'u': RA_USER, 'z': RA_USER, 'y': RA_API_KEY}
            progress_response = requests.get(f"{RA_BASE_URL}/API_GetGameInfoAndUserProgress.php", params=progress_params, timeout=10)
            data = progress_response.json()
            
            unlocked = data.get('NumAwardedToUserHardcore', 0)
            total = data.get('NumAchievements', 0)
            self.label_progresso.setText(f"{data.get('Title', '---')}\n{unlocked}/{total}")
            self._fetch_and_set_emblen(data.get('ImageIcon'))
            self.adjustSize()
        except:
            self.label_progresso.setText("Erro de Conexão")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPosition().toPoint()
        elif event.button() == Qt.RightButton:
            self.timer.stop()
            QApplication.instance().quit()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()

    def keyPressEvent(self, event):
        # ESC -> Sair
        if event.key() == Qt.Key_Escape:
            self.timer.stop()
            QApplication.instance().quit()
        # CTRL + Q -> Resetar Login
        elif event.key() == Qt.Key_Q and (event.modifiers() & Qt.ControlModifier):
            self.timer.stop()
            clear_credentials()
            QApplication.instance().restart_required = True
            self.close()
            QApplication.instance().exit()

def run_app():
    app = QApplication(sys.argv)
    while True:
        global RA_USER, RA_API_KEY
        RA_USER, RA_API_KEY = load_credentials()
        if not RA_USER or not RA_API_KEY:
            if not ConfigWindow().exec(): return 0
            RA_USER, RA_API_KEY = load_credentials()
        
        if RA_USER and RA_API_KEY:
            QApplication.instance().restart_required = False
            widget = OverlayWidget()
            widget.show()
            app.exec()
            if not getattr(QApplication.instance(), 'restart_required', False): break
        else: break
    return 0

if __name__ == "__main__":
    sys.exit(run_app())