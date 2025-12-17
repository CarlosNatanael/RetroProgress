# 🎮 RetroProgress Overlay

O **RetroProgress** é um overlay minimalista e sem bordas, desenvolvido em Python e PySide6, para exibir o progresso de conquistas Hardcore do jogo atual no RetroAchievements. Ideal para streamers que utilizam ferramentas como OBS/Streamlabs.

<p align="center">
  <img width="397" height="126" alt="image" src="https://github.com/user-attachments/assets/48653829-8d91-4f6e-b290-28e8a4037542" />
</p>

---

## ✨ Funcionalidades

* **Progresso em Tempo Real**: Atualização automática a cada 5 segundos.
* **Segurança (Keyring)**: Credenciais (Usuário e API Key) armazenadas de forma segura e criptografada no sistema operacional.
* **Interface Ultra-Minimalista**: Sem botões ou bordas para não interferir na transmissão.
* **Controle por Atalhos**: Gerenciamento completo do app via teclado e mouse.

---

## 🚀 Como Usar

### 1. Obtenha sua API Key
Para usar o RetroProgress, você precisará do seu **Nome de Usuário** e da sua **Web API Key** no RetroAchievements:
1. Faça login no site do [RetroAchievements](https://retroachievements.org).
2. Acesse **Account Settings** (Configurações da Conta).
3. A chave está listada como **"Web API Key"** Copie o valor.

### 2. Configuração Inicial
Na primeira execução, o aplicativo exibirá a tela de configuração:

<p align="center">
  <img width="390" height="312" alt="image" src="https://github.com/user-attachments/assets/e196c6c3-cc8c-437f-86a1-afce9888a8d0" />
</p>

1. Insira seu **Nome de Usuário**.
2. Cole a **Web API Key** capturada anteriormente.
3. Clique em **"Salvar e Iniciar"**.

### 3. Movimentação
* **Arrastar**: Clique e segure com o **Botão Esquerdo** do mouse em qualquer parte do overlay para posicioná-lo na tela.

---

## ⌨️ Atalhos e Controles

Como o overlay não possui botões visíveis, utilize os seguintes comandos:

| Ação | Comando |
| :--- | :--- |
| **Fechar Aplicativo** | Pressione **ESC** ou clique com o **Botão Direito**. |
| **Trocar Conta / Reset** | Pressione **Ctrl + Q** para abrir a tela de login novamente. |

---

## ⚙️ Configurações Técnicas

* **Intervalo de Atualização**: 5000ms (5 segundos).
* **Tecnologias**: Python, PySide6, Requests, Keyring.
