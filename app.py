import sys
import requests
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QHBoxLayout, QDialog, QLineEdit, QPushButton, QFormLayout, QMessageBox
)
from PySide6.QtCore import Qt, QTimer, QUrl, QByteArray
from utilidades_config import load_credentials, save_credentials, clear_credentials
from PySide6.QtGui import QPixmap
from io import BytesIO
from datetime import datetime

# --- CONFIG ---
UPDATE_INTERVAL_MS = 5000
RA_BASE_URL = "https://retroachievements.org/API"
RA_IMG_BASE = "https://media.retroachievements.org"

class ConfigWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuração RetroProgress")
        self.setFixedSize(350, 250)
        self.creds_saved = False

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setStyleSheet("""
            QDialog {
                background-color: #2c3e50; /* Fundo escuro */
                border: 2px solid #3498db; /* Borda azul */
                border-radius: 10px; /* Cantos arredondados */
            }
            QLabel {
                color: #ecf0f1; /* Texto claro */
                font-weight: bold;
            }
            QPushButton {
                background-color: #3498db; /* Azul vibrante */
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9; /* Azul mais escuro no hover */
            }
            QLineEdit {
                background-color: #34495e; /* Fundo do campo um pouco mais claro que o fundo */
                color: #ecf0f1;
                border: 1px solid #7f8c8d;
                padding: 5px;
                border-radius: 4px;
            }
        """)

        layout = QFormLayout(self)
        layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        
        title_label = QLabel("RetroProgress - Configuração de API")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
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
        user, key = load_credentials()
        if user:
             self.user_input.setText(user)
        self.setLayout(layout)

    def save_and_start(self):
        user = self.user_input.text().strip()
        key = self.key_input.text().strip()

        if not user or not key:
            QMessageBox.warning(self, "Erro", "Usuário e Chave API devem ser preenchidos.", QMessageBox.Ok)
            return
        
        save_credentials(user, key)
        self.creds_saved = True
        self.accept()

class OverlayWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.current_game_id = 0

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
        self.config_button = QPushButton("⚙️")
        self.config_button.setFixedSize(30, 30)
        self.config_button.setFlat(True)
        self.config_button.clicked.connect(self.show_config_window)
        main_layout.addWidget(self.config_button)

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
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Fazendo download do emblema: {image_url}") # LOG
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
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Erro ao baixar emblema: {e}") # LOG
            self.label_emblema.setText("X")
        
    def update_progress(self):
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] --- INICIANDO REQUISIÇÕES (Intervalo: 5s) ---") # LOG
        try:
            # --- PASSO 1: Obter o ID do Jogo Atual ---
            summary_url = f"{RA_BASE_URL}/API_GetUserSummary.php"
            summary_params = {'z': RA_USER, 'y': RA_API_KEY, 'u': RA_USER}
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Requisitando Sumário do Usuário...") # LOG
            summary_response = requests.get(summary_url, params=summary_params, timeout=10)
            summary_response.raise_for_status()
            summary_data = summary_response.json()

            last_game_id = summary_data.get('LastGameID')

            if not last_game_id or int(last_game_id) == 0:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Status: Nenhum jogo em progresso.") # LOG
                self.label_progresso.setText("Nenhum jogo em progresso.")
                self.label_emblema.clear()
                return
            
            self.current_game_id = last_game_id
            
            # --- PASSO 2: Obter o Progresso do Jogo Atual ---
            progress_url = f"{RA_BASE_URL}/API_GetGameInfoAndUserProgress.php"
            progress_params = {
                'g': self.current_game_id, 
                'u': RA_USER,
                'z': RA_USER,
                'y': RA_API_KEY
            }
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Requisitando Progresso do Game ID: {self.current_game_id}") # LOG
            progress_response = requests.get(progress_url, params=progress_params, timeout=10)
            progress_response.raise_for_status()
            progress_data = progress_response.json()
            
            unlocked = progress_data.get('NumAwardedToUserHardcore', 0) 
            total = progress_data.get('NumAchievements', 0)

            game_title = progress_data.get('Title', 'Jogo Desconhecido')

            self.label_progresso.setText(f"{game_title}\n {unlocked}/{total}")
            print(f"[{datetime.now().strftime('%H:%M:%S')}] SUCESSO. Progresso: {unlocked}/{total} ({game_title})") # LOG

            icon_path = progress_data.get('ImageIcon')
            self._fetch_and_set_emblen(icon_path)

            self.adjustSize()
        
        except requests.exceptions.RequestException as e:
            status_code = getattr(e.response, 'status_code', 'N/A')
            if status_code == 401 or status_code == 403:
                self.label_progresso.setText("ERRO: Credenciais RA Inválidas. Clique no ⚙️")
                self.cred_error_state = True
                self.timer.stop()
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ERRO 401/403: Requer reconfiguração.")
            else:
                # Outros erros (conexão, servidor, etc.)
                self.label_progresso.setText("ERRO: Verifique a conexão. (Status: {status_code})")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ERRO de conexão/API (Status: {status_code}): {e}") # LOG DETALHADO
            self.label_progresso.setText("ERRO: Verifique a conexão, Usuario ou API Key.")
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ERRO inesperado: {e}") # LOG
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

    def show_config_window(self):
            """Para o timer, limpa as credenciais e reinicia o aplicativo."""
            self.timer.stop()
            clear_credentials()
            self.close()
            QApplication.instance().restart_required = True

def run_app():
    app = QApplication(sys.argv)
    app.restart_required = False 
    while True:
        global RA_USER, RA_API_KEY
        RA_USER, RA_API_KEY = load_credentials()

        if not RA_USER or not RA_API_KEY:
            config_dialog = ConfigWindow()
            if config_dialog.exec():
                RA_USER, RA_API_KEY = load_credentials()
            else:
                return 0 
        if RA_USER and RA_API_KEY:
            widget = OverlayWidget()
            widget.show()
            
            app.exec() 

            if getattr(QApplication.instance(), 'restart_required', False):
                QApplication.instance().restart_required = False
                continue 
            else:
                return 0 
        else:
            QMessageBox.critical(None, "Erro Crítico", "As credenciais não foram fornecidas. O aplicativo será encerrado.")
            return 1

if __name__ == "__main__":
    sys.exit(run_app())