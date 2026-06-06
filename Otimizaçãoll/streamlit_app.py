import streamlit as st
import math

# ===========================
# LÓGICA DE CÁLCULO
# ===========================

def calcular_mm1(lamb, mu):
    if lamb >= mu: return None
    rho = lamb / mu
    P0 = 1 - rho
    L = lamb / (mu - lamb)
    Lq = lamb**2 / (mu * (mu - lamb))
    W = L / lamb
    Wq = Lq / lamb
    return {"rho": rho, "P0": P0, "L": L, "Lq": Lq, "W": W, "Wq": Wq}

def calcular_mms(lamb, mu, s):
    rho = lamb / (s * mu)
    if rho >= 1: return None
    soma = sum((lamb / mu) ** n / math.factorial(n) for n in range(s))
    termo = ((lamb / mu) ** s) / (math.factorial(s) * (1 - rho))
    P0 = 1 / (soma + termo)
    Lq = (P0 * ((lamb / mu) ** s) * rho / (math.factorial(s) * (1 - rho) ** 2))
    L = Lq + lamb / mu
    Wq = Lq / lamb
    W = L / lamb
    return {"rho": rho, "P0": P0, "L": L, "Lq": Lq, "W": W, "Wq": Wq}

def calcular_mm1k(lamb, mu, K):
    rho = lamb / mu
    if rho != 1:
        P0 = (1 - rho) / (1 - rho ** (K + 1))
        L = (rho / (1 - rho)) - ((K + 1) * rho ** (K + 1)) / (1 - rho ** (K + 1))
    else:
        P0 = 1 / (K + 1)
        L = K / 2
    Pk = P0 * rho ** K
    lamb_barra = lamb * (1 - Pk)
    Lq = L - (1 - P0)
    W = L / lamb_barra
    Wq = Lq / lamb_barra
    return {"rho": rho, "P0": P0, "L": L, "Lq": Lq, "W": W, "Wq": Wq}

def calcular_mmsk(lamb, mu, s, K):
    rho = lamb / (s * mu)
    soma1 = sum(((lamb / mu) ** n) / math.factorial(n) for n in range(s))
    soma2 = sum(((lamb / mu) ** n) / (math.factorial(s) * s ** (n - s)) for n in range(s, K + 1))
    P0 = 1 / (soma1 + soma2)
    probs = []
    for n in range(K + 1):
        if n < s: pn = ((lamb / mu) ** n) / math.factorial(n) * P0
        else: pn = (((lamb / mu) ** n) / (math.factorial(s) * s ** (n - s))) * P0
        probs.append(pn)
    L = sum(n * probs[n] for n in range(K + 1))
    Lq = sum(max(0, n - s) * probs[n] for n in range(K + 1))
    lamb_barra = lamb * (1 - probs[K])
    W = L / lamb_barra
    Wq = Lq / lamb_barra
    return {"rho": rho, "P0": P0, "L": L, "Lq": Lq, "W": W, "Wq": Wq}

def calcular_mm1n(lamb, mu, N):
    soma = sum((math.factorial(N) / math.factorial(N - n)) * (lamb / mu) ** n for n in range(N + 1))
    P0 = 1 / soma
    L = N - (mu / lamb) * (1 - P0)
    Lq = N - ((lamb + mu) / lamb) * (1 - P0)
    lamb_barra = lamb * (N - L)
    W = L / lamb_barra
    Wq = Lq / lamb_barra
    return {"P0": P0, "L": L, "Lq": Lq, "W": W, "Wq": Wq}

def calcular_mmsn(lamb, mu, s, N):
    soma = sum((math.factorial(N) / (math.factorial(N - n) * math.factorial(n))) * (lamb / mu) ** n for n in range(s))
    soma += sum((math.factorial(N) / (math.factorial(N - n) * math.factorial(s) * s ** (n - s))) * (lamb / mu) ** n for n in range(s, N + 1))
    P0 = 1 / soma
    probs = []
    for n in range(N + 1):
        if n < s: pn = (math.factorial(N) / (math.factorial(N - n) * math.factorial(n))) * (lamb / mu) ** n * P0
        else: pn = (math.factorial(N) / (math.factorial(N - n) * math.factorial(s) * s ** (n - s))) * (lamb / mu) ** n * P0
        probs.append(pn)
    L = sum(n * probs[n] for n in range(N + 1))
    Lq = L - (lamb / mu) * (N - L)
    lamb_barra = lamb * (N - L)
    W = L / lamb_barra
    Wq = Lq / lamb_barra
    return {"P0": P0, "L": L, "Lq": Lq, "W": W, "Wq": Wq}

# ===========================
# INTERFACE STREAMLIT
# ===========================

st.set_page_config(page_title="Modelos de Filas", layout="wide")
st.title("📊 Modelos de Teoria de Filas")

menu = ["M/M/1", "M/M/s", "M/M/1/K", "M/M/s/K", "M/M/1/N", "M/M/s/N"]
escolha = st.sidebar.selectbox("Escolha o Modelo", menu)

st.header(f"Configuração do Modelo {escolha}")

with st.expander("Parâmetros de Entrada", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        lamb = st.number_input("Taxa de chegada (λ)", min_value=0.01, value=1.0, step=0.1)
    with col2:
        mu = st.number_input("Taxa de atendimento (μ)", min_value=0.01, value=1.5, step=0.1)
    
    extra_params = {}
    if "s" in escolha.lower():
        extra_params['s'] = st.number_input("Número de servidores (s)", min_value=1, value=2)
    if "k" in escolha.lower():
        extra_params['K'] = st.number_input("Capacidade máxima (K)", min_value=1, value=10)
    if "n" in escolha.lower():
        extra_params['N'] = st.number_input("População (N)", min_value=1, value=50)

res = None
if escolha == "M/M/1": res = calcular_mm1(lamb, mu)
elif escolha == "M/M/s": res = calcular_mms(lamb, mu, extra_params['s'])
elif escolha == "M/M/1/K": res = calcular_mm1k(lamb, mu, extra_params['K'])
elif escolha == "M/M/s/K": res = calcular_mmsk(lamb, mu, extra_params['s'], extra_params['K'])
elif escolha == "M/M/1/N": res = calcular_mm1n(lamb, mu, extra_params['N'])
elif escolha == "M/M/s/N": res = calcular_mmsn(lamb, mu, extra_params['s'], extra_params['N'])

if res:
    st.markdown("---")
    st.subheader("🚀 Resultados")
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    
    if "rho" in res: m1.metric("Utilização (ρ)", f"{res['rho']:.4f}")
    m2.metric("Prob. Vazio (P0)", f"{res['P0']:.4f}")
    m3.metric("L (Sist.)", f"{res['L']:.4f}")
    m4.metric("Lq (Fila)", f"{res['Lq']:.4f}")
    m5.metric("W (Sist.)", f"{res['W']:.4f}")
    m6.metric("Wq (Fila)", f"{res['Wq']:.4f}")
elif res is None:
    st.error("⚠️ Sistema instável! Verifique os parâmetros (λ deve ser menor que sμ).")
