# 📊 Modelos de Teoria de Filas com Streamlit

Este projeto é uma ferramenta interativa para simulação e cálculo de modelos de **Teoria de Filas**, utilizando a biblioteca **Streamlit** para fornecer uma interface web amigável. Ele foi desenvolvido e validado com base nos slides e listas de exercícios da disciplina de Otimização II.

## 🚀 Funcionalidades

O aplicativo permite calcular métricas principais (Utilização $\rho$, $P_0$, $L$, $L_q$, $W$, $W_q$) para uma ampla variedade de modelos de filas:
*   **M/M/1**: Um servidor, capacidade infinita.
*   **M/M/s**: Múltiplos servidores, capacidade infinita.
*   **M/M/1/K**: Um servidor, capacidade finita $K$.
*   **M/M/s/K**: Múltiplos servidores, capacidade finita $K$.
*   **M/M/1/N**: Um servidor, população finita $N$.
*   **M/M/s/N**: Múltiplos servidores, população finita $N$.
*   **M/G/1**: Um servidor, tempo de atendimento genérico com desvio padrão $\sigma$ (inclui o modelo determinístico **M/D/1** ao definir $\sigma = 0$).
*   **Prioridade Não-Preemptiva**: Filas de prioridade múltipla sem interrupção de atendimento em andamento.
*   **Prioridade Preemptiva**: Filas de prioridade múltipla com interrupção imediata de serviço para classes superiores.

### 📊 Abas Adicionais de Probabilidades
O simulador também executa cálculos de probabilidade analíticos conforme o material didático:
*   **Probabilidade de Clientes (N)**: Calcular $P(N = n)$, $P(N > n)$, $P(N \le n)$, $P(N < n)$ e $P(N \ge n)$.
*   **Tempo de Espera**: Probabilidade do tempo de espera no sistema ou fila exceder um limite ($P(W > t)$ e $P(W_q > t)$) para modelos M/M/1 e M/M/s.
*   **Processo de Poisson**: Probabilidade de número exato de chegadas ou serviços em um intervalo de tempo $T$.

## 🛠️ Pré-requisitos

*   Python 3.8 ou superior instalado.
*   Acesso ao terminal/prompt de comando.

## 📦 Como rodar o projeto

Siga os passos abaixo para configurar o ambiente e executar a aplicação:

### 1. Clonar o repositório
```bash
git clone https://github.com/LucasDavid80/OTIMIZACAO_2.git
cd OTIMIZACAO_2
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
Com a venv ativa, instale as dependências (Streamlit, PyPDF e Pytest):
```bash
pip install -r requirements.txt
```

### 4. Executar os Testes Unitários
Para validar que todas as fórmulas estão corretas e batendo com o gabarito das listas da disciplina:
```bash
pytest test_models.py
```

### 5. Executar a aplicação
Agora, basta rodar o comando do Streamlit:
```bash
streamlit run streamlit_app.py
```

A aplicação abrirá automaticamente no seu navegador padrão (geralmente em `http://localhost:8501`).

## 📁 Estrutura do Projeto

*   `streamlit_app.py`: Interface gráfica interativa web construída em Streamlit.
*   `models.py`: Implementação pura em Python de todas as fórmulas de teoria das filas.
*   `test_models.py`: Suíte de testes automatizados com `pytest` cobrindo mais de 18 cenários de exercícios.
*   `main.py`: Versão original em modo texto (CLI).
*   `requirements.txt`: Lista de dependências do projeto (Streamlit, pypdf, pytest).
*   `.gitignore`: Arquivos ignorados pelo Git (como a pasta `venv` e caches do Pytest).

---
Desenvolvido para a disciplina de Otimização II.
