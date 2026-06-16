import streamlit as st
from models import (
    calcular_mm1, calcular_mms, calcular_mm1k, calcular_mmsk,
    calcular_mm1n, calcular_mmsn, calcular_mg1,
    calcular_prioridade_non_preemptive,
    calcular_prioridade_preemptive,
)

st.set_page_config(page_title="Modelos de Filas", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ff0000; padding: 15px; border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

st.title("Simulador de Teoria de Filas")
st.sidebar.header("Configurações")

menu = [
    "M/M/1", "M/M/s", "M/M/1/K", "M/M/s/K",
    "M/M/1/N", "M/M/s/N", "M/G/1",
    "Prioridade Não-Preemptiva",
    "Prioridade Preemptiva",
]
escolha = st.sidebar.selectbox("Selecione o Modelo", menu)


#prioridade sem interrupção
if escolha == "Prioridade Não-Preemptiva":
    st.header("Prioridade Não-Preemptiva")

    mu = st.sidebar.number_input("Taxa de atendimento μ", min_value=0.01, value=3.0, step=0.1)
    s  = st.sidebar.number_input("Número de servidores (s)", min_value=1, value=1, step=1)
    num_classes = st.sidebar.number_input("Número de classes", min_value=2, max_value=8, value=2, step=1)

    st.info("**Classe 1 = maior prioridade.** μ é igual para todas as classes.")

    lambdas = []
    cols = st.columns(int(num_classes))
    for i, col in enumerate(cols):
        with col:
            lamb_k = st.number_input(f"λ_{i+1}", min_value=0.001, value=1.0, step=0.1, key=f"lamb_{i}")
            lambdas.append(lamb_k)

    st.markdown("---")

    resultados = calcular_prioridade_non_preemptive(lambdas, mu, int(s))

    if resultados is None:
        rho_info = sum(lambdas) / (int(s) * mu)
        st.error(f"ρ total = {rho_info:.4f} ≥ 1")
    else:
        rho_total = resultados[0]["rho_total"]
        st.success(f"ρ total = {rho_total:.4f}")
        st.subheader("Resultados por Classe")
        for r in resultados:
            titulo = f"Classe {r['classe']}  (λ={r['lamb']}, μ={r['mu']}, ρ={r['rho']:.4f})"
            with st.expander(titulo, expanded=True):
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Wq", f"{r['Wq']:.4f}")
                c2.metric("W",  f"{r['W']:.4f}")
                c3.metric("Lq", f"{r['Lq']:.4f}")
                c4.metric("L",  f"{r['L']:.4f}")


#outro modelos
else:
    st.header(f"Modelo {escolha}")

    with st.container():
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            lamb = st.number_input("Taxa de chegada (λ)", min_value=0.01, value=1.0, step=0.1)
        with col_in2:
            mu = st.number_input("Taxa de atendimento (μ)", min_value=0.01, value=1.5, step=0.1)

        col_ex1, col_ex2 = st.columns(2)
        s, K, N, sigma = 1, 1, 1, 0.0

        if "s" in escolha.lower() and "mg1" not in escolha.lower():
            s = col_ex1.number_input("Número de servidores (s)", min_value=1, value=2)
        if "k" in escolha.lower():
            K = col_ex2.number_input("Capacidade máxima (K)", min_value=1, value=10)
        if "n" in escolha.lower():
            N = col_ex1.number_input("População (N)", min_value=1, value=50)
        if "g/1" in escolha.lower():
            sigma = col_ex1.number_input("Desvio Padrão (σ)", min_value=0.0, value=0.0, step=0.1)

    res = None
    if escolha == "M/M/1":         res = calcular_mm1(lamb, mu)
    elif escolha == "M/M/s":       res = calcular_mms(lamb, mu, s)
    elif escolha == "M/M/1/K":     res = calcular_mm1k(lamb, mu, K)
    elif escolha == "M/M/s/K":     res = calcular_mmsk(lamb, mu, s, K)
    elif escolha == "M/M/1/N":     res = calcular_mm1n(lamb, mu, N)
    elif escolha == "M/M/s/N":     res = calcular_mmsn(lamb, mu, s, N)
    elif escolha == "M/G/1":       res = calcular_mg1(lamb, mu, sigma)
    elif escolha == "Prioridade Preemptiva":
        st.header("Prioridade Preemptiva")

        mu = st.sidebar.number_input("Taxa de atendimento μ", min_value=0.01, value=3.0, step=0.1)
        s  = st.sidebar.number_input("Número de servidores (s)", min_value=1, value=1, step=1)
        num_classes = st.sidebar.number_input("Número de classes", min_value=2, max_value=8, value=2, step=1)

        st.info("**Classe 1 = maior prioridade.** Ao chegar cliente de classe superior, o serviço atual é interrompido. μ é igual para todas as classes.")

        lambdas = []
        cols = st.columns(int(num_classes))
        for i, col in enumerate(cols):
            with col:
                lamb_k = st.number_input(f"λ_{i+1}", min_value=0.001, value=1.0, step=0.1, key=f"lamb_pre_{i}")
                lambdas.append(lamb_k)

        st.markdown("---")

        resultados = calcular_prioridade_preemptive(lambdas, mu, int(s))

        if resultados is None:
            rho_info = sum(lambdas) / (int(s) * mu)
            st.error(f"ρ total = {rho_info:.4f} ≥ 1")
        else:
            rho_total = resultados[0]["rho_total"]
            st.success(f"ρ total = {rho_total:.4f}")
            st.subheader("Resultados por Classe")
            for r in resultados:
                titulo = f"Classe {r['classe']}  (λ={r['lamb']}, μ={r['mu']}, ρ={r['rho']:.4f})"
                with st.expander(titulo, expanded=True):
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Wq", f"{r['Wq']:.4f}")
                    c2.metric("W",  f"{r['W']:.4f}")
                    c3.metric("Lq", f"{r['Lq']:.4f}")
                    c4.metric("L",  f"{r['L']:.4f}")

    if res:
        st.markdown("---")
        st.subheader("Resultados")
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        m1.metric("Utilização (ρ)", f"{res['rho']:.4f}" if "rho" in res else "N/A")
        m2.metric("P0 (Vazio)",    f"{res['P0']:.4f}")
        m3.metric("L (Sistema)",   f"{res['L']:.4f}")
        m4.metric("Lq (Fila)",     f"{res['Lq']:.4f}")
        m5.metric("W (Sistema)",   f"{res['W']:.4f}")
        m6.metric("Wq (Fila)",     f"{res['Wq']:.4f}")
    elif res is None and escolha not in ("Prioridade Preemptiva", "Prioridade Não-Preemptiva"):
        st.error("A taxa de chegada deve ser menor que a capacidade total de atendimento (λ < sμ).")