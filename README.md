# 📊 Modelos de Teoria de Filas com Streamlit

Este projeto é uma ferramenta interativa para simulação e cálculo de modelos de **Teoria de Filas**, utilizando a biblioteca **Streamlit** para fornecer uma interface web amigável.

## 🚀 Funcionalidades

O aplicativo permite calcular métricas principais (Utilização, $P_0$, $L$, $L_q$, $W$, $W_q$) para os seguintes modelos:
*   **M/M/1**: Um servidor, capacidade infinita.
*   **M/M/s**: Múltiplos servidores, capacidade infinita.
*   **M/M/1/K**: Um servidor, capacidade finita $K$.
*   **M/M/s/K**: Múltiplos servidores, capacidade finita $K$.
*   **M/M/1/N**: Um servidor, população finita $N$.
*   **M/M/s/N**: Múltiplos servidores, população finita $N$.

## 🛠️ Pré-requisitos

*   Python 3.8 ou superior instalado.
*   Acesso ao terminal/prompt de comando.

## 📦 Como rodar o projeto

Siga os passos abaixo para configurar o ambiente e executar a aplicação:

### 1. Clonar o repositório (ou navegar até a pasta)
```bash
cd OTIMIZACAO_2/Otimizaçãoll
```

### 2. Criar e ativar o ambiente virtual (venv)
É recomendável usar um ambiente isolado para as dependências:

**No Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**No Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências
Com a venv ativada, instale o Streamlit:
```bash
pip install -r requirements.txt
```

### 4. Executar a aplicação
Agora, basta rodar o comando do Streamlit:
```bash
streamlit run streamlit_app.py
```

A aplicação abrirá automaticamente no seu navegador padrão (geralmente em `http://localhost:8501`).

## 📁 Estrutura do Projeto

*   `streamlit_app.py`: Arquivo principal com a interface e lógica dos modelos.
*   `main.py`: Versão original em modo texto (CLI).
*   `requirements.txt`: Lista de dependências do projeto.
*   `.gitignore`: Arquivos e pastas ignorados pelo Git (como a `venv`).

---
Desenvolvido para a disciplina de Otimização.
