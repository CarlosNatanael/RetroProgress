# 🎮 RetroProgress: RetroAchievements Overlay

O **RetroProgress** é um overlay minimalista e sem bordas, desenvolvido em Python e PySide6, para exibir o progresso de conquistas Hardcore do jogo atual no RetroAchievements. Ideal para streamers que utilizam ferramentas como OBS/Streamlabs.

---

## ✨ Funcionalidades

* **Progresso em Tempo Real:** Atualização automática a cada 5 segundos.
* **Segurança (Keyring):** Credenciais (Usuário e API Key) armazenadas de forma segura e criptografada no sistema operacional.
* **Interface Moderna:** Tela de configuração Dark Mode com estilo minimalista.
* **Fechamento Fácil:** Encerra usando Clique Direito do Mouse ou a tecla `ESC`.

---

## 🚀 Como Usar

### 1. Obtenha sua API Key

Para usar o RetroProgress, você precisará do seu **Nome de Usuário** e da sua **API Key** no RetroAchievements:

1.  Faça login no site do RetroAchievements.
2.  Acesse **Account Settings** (Configurações da Conta).
3.  A chave está listada como **"Web API Key"** na seção "Developer". Copie o valor.

### 2. Configuração Inicial

Na primeira execução, o aplicativo exibirá a tela de configuração:

1.  Insira seu **Nome de Usuário** do RetroAchievements.
2.  Cole a **Web API Key** que você copiou.
3.  Clique em **"Salvar e Iniciar"**.

Suas credenciais serão armazenadas com segurança no seu sistema e não precisarão ser digitadas novamente.

### 3. Uso do Overlay

* **Arrastar:** Use o **Clique Esquerdo** do mouse para arrastar o overlay para a posição desejada na tela.
* **Progresso:** O aplicativo monitorará automaticamente o jogo mais recente que você está jogando.

### 4. Como Encerrar ou Resetar

O overlay é sem bordas, então ele não tem o botão 'X' (Fechar). Use as seguintes opções:

* **Encerrar (Fechar o Programa):** Clique com o **Botão Direito** do mouse em qualquer parte do overlay, ou pressione a tecla **`ESC`**.
* **Resetar (Trocar de Usuário/API Key):** Se você precisar trocar de conta ou corrigir uma API Key inválida, clique no botão **⚙️** (Engrenagem) no canto direito do overlay. O aplicativo pedirá as credenciais novamente.

---

## ⚙️ Configurações Técnicas

* **Intervalo de Atualização:** `UPDATE_INTERVAL_MS` está configurado para **5000ms (5 segundos)**.
* **Bibliotecas Necessárias:** `PySide6`, `requests`, `keyring`.