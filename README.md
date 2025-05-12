PTBR 🇧🇷:


# Analisador de Código IA  
**Status:** Funcionando ✅

---

## 🚀 Visão Geral  
O **Analisador de Código IA** é uma ferramenta desktop multiplataforma (Linux, Windows e macOS) que auxilia desenvolvedores e equipes de QA a elevar a qualidade do código e reduzir riscos de segurança. Alimentado pelo motor de IA **TGPT**, o aplicativo faz:

- **Análise estática completa** de projetos em diversas linguagens (Python, JavaScript, Java etc.),  
- **Explanação linha a linha** do que cada trecho faz, facilitando revisão de código e onboarding,  
- **Detecção precoce** de vulnerabilidades, antipadrões e melhorias de performance.

Com interface gráfica intuitiva em **PyQt5**, os usuários importam arquivos ou pastas inteiras, recebem relatórios estruturados e podem interagir clicando em trechos de código para obter explicações contextuais em tempo real.

---

## 🎯 Benefícios para a Equipe  
- **Qualidade do Software:** Identificação automática de falhas de segurança e inconsistências antes da fase de testes.  
- **Onboarding mais rápido:** Novos membros entendem a base de código com explicações geradas instantaneamente.  
- **Padronização de código:** Sugerimos correções de estilo e padrões recomendados.  
- **Produtividade:** Menos tempo gasto em revisões manuais, mais foco em features de alto valor.

---

## 🛠️ Tecnologias e Arquitetura  
- **Frontend:** PyQt5 (GUI multiplataforma)  
- **Backend:** Python 3.9+, subprocess calls para CLI do **TGPT**  
- **IA/NLP:** TGPT (https://github.com/aandrew-me/tgpt)  
- **Concorrência:** `threading` para manter a interface responsiva  
- **Gerenciamento de arquivos:** `tempfile`, `os` e `pathlib`  
- **Controle de versão:** Git  

---

## ⚙️ Instalação e Uso

1. **Pré-requisitos**  
   - Python 3.8 ou superior  
   - Acesso à internet para consultas TGPT  
   - TGPT instalado globalmente:  
     ```bash
     curl -sSL https://raw.githubusercontent.com/aandrew-me/tgpt/main/install | bash -s /usr/local/bin
     ```

2. **Clonar e instalar dependências**  
   ```bash
   git clone https://github.com/nizpew/AI-code-analysis.git
   cd AI-code-analysis
   pip install -r requirements.txt




# ------------ENGLISH README 🇺🇸: ------------------

# AI Code Analyzer  
**Status:** Working ✅

---

## 🚀 Overview  
The **AI Code Analyzer** is a cross-platform desktop tool (Linux, Windows, and macOS) that helps developers and QA teams enhance code quality and reduce security risks. Powered by the **TGPT** AI engine, the application performs:

- **Comprehensive static analysis** of projects in various languages (Python, JavaScript, Java, etc.),  
- **Line-by-line explanation** of what each snippet does, facilitating code review and onboarding,  
- **Early detection** of vulnerabilities, anti-patterns, and performance improvements.

With an intuitive graphical interface in **PyQt5**, users can import files or entire folders, receive structured reports, and interact by clicking on code snippets to get contextual explanations in real-time.

---

## 🎯 Benefits for the Team  
- **Software Quality:** Automatic identification of security flaws and inconsistencies before the testing phase.  
- **Faster Onboarding:** New members understand the codebase with instantly generated explanations.  
- **Code Standardization:** We suggest style corrections and recommended patterns.  
- **Productivity:** Less time spent on manual reviews, more focus on high-value features.

---

## 🛠️ Technologies and Architecture  
- **Frontend:** PyQt5 (cross-platform GUI)  
- **Backend:** Python 3.9+, subprocess calls to the **TGPT** CLI  
- **AI/NLP:** TGPT (https://github.com/aandrew-me/tgpt)  
- **Concurrency:** `threading` to keep the interface responsive  
- **File Management:** `tempfile`, `os`, and `pathlib`  
- **Version Control:** Git  

---

## ⚙️ Installation and Usage

1. **Prerequisites**  
   - Python 3.8 or higher  
   - Internet access for TGPT queries  
   - TGPT installed globally:  
     ```bash
     curl -sSL https://raw.githubusercontent.com/aandrew-me/tgpt/main/install | bash -s /usr/local/bin
     ```

2. **Clone and install dependencies**  
   ```bash
   git clone https://github.com/nizpew/AI-code-analysis.git
   cd AI-code-analysis
   pip install -r requirements.txt
   ```
