import streamlit as st
from models import (
    calcular_mm1, calcular_mms, calcular_mm1k, calcular_mmsk,
    calcular_mm1n, calcular_mmsn, calcular_mg1,
    calcular_prioridade_non_preemptive,
    calcular_prioridade_preemptive,
    calcular_prob_n_mm1, calcular_prob_greater_r_mm1,
    calcular_prob_w_greater_t_mm1, calcular_prob_wq_greater_t_mm1,
    calcular_prob_n_mms, calcular_prob_w_greater_t_mms,
    calcular_prob_wq_greater_t_mms, calcular_poisson_prob,
)

st.set_page_config(page_title="Modelos de Filas", layout="wide")



st.title("Simulador de Teoria de Filas")

# Expander de Fórmulas e Símbolos
with st.expander("📖 Fórmulas e Glossário de Símbolos", expanded=False):
    st.markdown("""
    ### 🔤 Glossário de Símbolos
    *   $\lambda$ (**lambda**): Taxa de chegada de clientes
    *   $\mu$ (**mu**): Taxa de atendimento por servidor
    *   $\\rho$ (**rho**): Fator de utilização do sistema (fator de ocupação)
    *   $\sigma$ (**sigma**): Desvio padrão do tempo de atendimento (no M/G/1)
    *   $\sigma_k$ (**sigma k**): Fator de utilização acumulado até a classe de prioridade $k$
    *   $P_0$ (**P zero**): Probabilidade do sistema estar vazio/ocioso
    *   $P_n$ (**P ene**): Probabilidade de haver exatamente $n$ clientes no sistema
    *   $L$ (**L**): Número médio de clientes no sistema
    *   $L_q$ (**L q**): Número médio de clientes na fila
    *   $W$ (**W**): Tempo médio de permanência no sistema (espera + atendimento)
    *   $W_q$ (**W q**): Tempo médio de espera na fila
    *   $s$ (**s**): Número de servidores/canais
    *   $K$ (**K**): Capacidade máxima do sistema (no M/M/1/K e M/M/s/K)
    *   $N$ (**N**): Tamanho da população finita (no M/M/1/N e M/M/s/N)
    
    ---
    
    ### 📐 Fórmulas de Conversão (Taxas)
    *   **Taxa de Chegada ($\lambda$):**
        $$\lambda = \\frac{1}{E[T_a]}$$
        *(onde $E[T_a]$ é o Tempo Médio Entre Chegadas)*
    *   **Taxa de Atendimento ($\mu$):**
        $$\mu = \\frac{1}{E[T_s]}$$
        *(onde $E[T_s]$ é o Tempo Médio de Atendimento)*
    *   **Modelos de População Finita (com $/N$):**
        *   $\lambda = 1 / \\text{Tempo Médio de Operação (Uptime)}$
        *   $\mu = 1 / \\text{Tempo Médio de Reparo (Downtime)}$
        
    ---
    
    ### 📊 Fórmulas Principais por Modelo
    
    #### Lei de Little (Geral)
    $$L = \\bar{\\lambda} W \\quad \\text{e} \\quad L_q = \\bar{\\lambda} W_q$$
    *(onde $\\bar{\\lambda}$ é a taxa de entrada efetiva no sistema)*
    
    #### Modelo M/M/1
    *   $\\rho = \\frac{\\lambda}{\\mu}$
    *   $P_0 = 1 - \\rho$
    *   $L = \\frac{\\lambda}{\\mu - \\lambda}$
    *   $L_q = \\frac{\\lambda^2}{\\mu(\\mu - \\lambda)}$
    *   $W = \\frac{1}{\\mu - \\lambda}$
    *   $W_q = \\frac{\\lambda}{\\mu(\\mu - \\lambda)}$
    *   $P_n = (1 - \\rho)\\rho^n$
    *   $P(N > r) = \\rho^{r+1}$
    *   $P(W > t) = e^{-\\mu(1-\\rho)t}$
    *   $P(W_q > t) = \\rho e^{-\\mu(1-\\rho)t}$
    
    #### Modelo M/G/1 (Pollaczek-Khintchine)
    *   $\\rho = \\frac{\\lambda}{\\mu}$
    *   $L_q = \\frac{\\lambda^2 \\sigma^2 + \\rho^2}{2(1 - \\rho)}$
    *   $L = L_q + \\rho$
    *   $W_q = \\frac{L_q}{\\lambda}$
    *   $W = W_q + \\frac{1}{\\mu}$
    
    #### Modelo M/M/s
    *   $\\rho = \\frac{\\lambda}{s\\mu}$
    *   $L_q = \\frac{P_0 (\\lambda/\\mu)^s \\rho}{s! (1-\\rho)^2}$
    *   $L = L_q + \\frac{\\lambda}{\\mu}$
    *   $W_q = \\frac{L_q}{\\lambda}$
    *   $W = W_q + \\frac{1}{\\mu}$
    """)

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

    mu = st.sidebar.number_input("Taxa de atendimento μ", min_value=0.0001, value=3.0, step=0.0001, format="%.4f", help="μ = 1 / (tempo médio de atendimento). Ex: se o serviço demora 20 min, μ = 1/20 = 0.05 atendimentos/min.")
    s  = st.sidebar.number_input("Número de servidores (s)", min_value=1, value=1, step=1)
    num_classes = st.sidebar.number_input("Número de classes", min_value=2, max_value=8, value=2, step=1)

    st.info("**Classe 1 = maior prioridade.** μ é igual para todas as classes.")

    lambdas = []
    cols = st.columns(int(num_classes))
    for i, col in enumerate(cols):
        with col:
            lamb_k = st.number_input(f"λ_{i+1}", min_value=0.0001, value=1.0, step=0.0001, format="%.4f", key=f"lamb_{i}", help="λ = 1 / (tempo médio entre chegadas de clientes desta classe).")
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


#prioridade com interrupção
elif escolha == "Prioridade Preemptiva":
    st.header("Prioridade Preemptiva")

    mu = st.sidebar.number_input("Taxa de atendimento μ", min_value=0.0001, value=3.0, step=0.0001, format="%.4f", help="μ = 1 / (tempo médio de atendimento). Ex: se o serviço demora 20 min, μ = 1/20 = 0.05 atendimentos/min.")
    s  = st.sidebar.number_input("Número de servidores (s)", min_value=1, value=1, step=1)
    num_classes = st.sidebar.number_input("Número de classes", min_value=2, max_value=8, value=2, step=1)

    st.info("**Classe 1 = maior prioridade.** Ao chegar cliente de classe superior, o serviço atual é interrompido. μ é igual para todas as classes.")

    lambdas = []
    cols = st.columns(int(num_classes))
    for i, col in enumerate(cols):
        with col:
            lamb_k = st.number_input(f"λ_{i+1}", min_value=0.0001, value=1.0, step=0.0001, format="%.4f", key=f"lamb_pre_{i}", help="λ = 1 / (tempo médio entre chegadas de clientes desta classe).")
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


#outros modelos
else:
    st.header(f"Modelo {escolha}")

    with st.container():
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            lamb = st.number_input("Taxa de chegada (λ)", min_value=0.0001, value=1.0, step=0.0001, format="%.4f", help="λ = 1 / (tempo médio entre chegadas). Ex: se chegam a cada 4 min, λ = 1/4 = 0.25 chegadas/min.")
        with col_in2:
            mu = st.number_input("Taxa de atendimento (μ)", min_value=0.0001, value=1.5, step=0.0001, format="%.4f", help="μ = 1 / (tempo médio de atendimento). Ex: se o serviço demora 15 min, μ = 1/15 = 0.0667 atendimentos/min.")

        col_ex1, col_ex2 = st.columns(2)
        s, K, N, sigma = 1, 1, 1, 0.0

        if "s" in escolha.lower() and "mg1" not in escolha.lower():
            s = col_ex1.number_input("Número de servidores (s)", min_value=1, value=2)
        if "k" in escolha.lower():
            K = col_ex2.number_input("Capacidade máxima (K)", min_value=1, value=10)
        if "n" in escolha.lower():
            N = col_ex1.number_input("População (N)", min_value=1, value=50)
        if "g/1" in escolha.lower():
            sigma = col_ex1.number_input("Desvio Padrão (σ)", min_value=0.0, value=0.0, step=0.0001, format="%.4f")

    res = None
    if escolha == "M/M/1":     res = calcular_mm1(lamb, mu)
    elif escolha == "M/M/s":   res = calcular_mms(lamb, mu, s)
    elif escolha == "M/M/1/K": res = calcular_mm1k(lamb, mu, K)
    elif escolha == "M/M/s/K": res = calcular_mmsk(lamb, mu, s, K)
    elif escolha == "M/M/1/N": res = calcular_mm1n(lamb, mu, N)
    elif escolha == "M/M/s/N": res = calcular_mmsn(lamb, mu, s, N)
    elif escolha == "M/G/1":   res = calcular_mg1(lamb, mu, sigma)

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

        # Seção de Probabilidades Adicionais (com base nos slides e exercícios)
        st.markdown("---")
        st.subheader("📊 Cálculos de Probabilidades (Fórmulas do Material)")
        
        tab1, tab2, tab3 = st.tabs([
            "👥 Probabilidade de Clientes (N)", 
            "⏱️ Tempo de Espera (W / Wq)", 
            "📈 Processo de Poisson (Chegadas/Atendimentos)"
        ])
        
        with tab1:
            st.markdown("### Probabilidade do número de clientes no sistema")
            n_val = st.number_input("Número de clientes (n)", min_value=0, value=1, step=1, key="prob_n_input")
            
            p_n = None
            p_gt = None
            p_le = None
            p_lt = None
            p_ge = None
            
            if escolha == "M/M/1":
                p_n = calcular_prob_n_mm1(lamb, mu, n_val)
                p_gt = calcular_prob_greater_r_mm1(lamb, mu, n_val)
                p_le = 1.0 - p_gt
                p_lt = 1.0 - calcular_prob_greater_r_mm1(lamb, mu, n_val - 1) if n_val > 0 else 0.0
                p_ge = p_n + p_gt
            elif escolha == "M/M/s":
                p_n = calcular_prob_n_mms(lamb, mu, s, n_val)
                p_le = sum(calcular_prob_n_mms(lamb, mu, s, k) for k in range(n_val + 1))
                p_gt = max(0.0, 1.0 - p_le)
                p_lt = sum(calcular_prob_n_mms(lamb, mu, s, k) for k in range(n_val)) if n_val > 0 else 0.0
                p_ge = max(0.0, 1.0 - p_lt)
            elif "probs" in res:
                probs = res["probs"]
                if n_val < len(probs):
                    p_n = probs[n_val]
                    p_le = sum(probs[:n_val + 1])
                    p_gt = max(0.0, 1.0 - p_le)
                    p_lt = sum(probs[:n_val]) if n_val > 0 else 0.0
                    p_ge = max(0.0, 1.0 - p_lt)
            
            if p_n is not None:
                c1, c2, c3 = st.columns(3)
                c1.metric(f"P(N = {n_val})", f"{p_n:.4%}", help="Exatamente n clientes no sistema")
                c2.metric(f"P(N > {n_val})", f"{p_gt:.4%}", help="Mais de n clientes no sistema")
                c3.metric(f"P(N ≤ {n_val})", f"{p_le:.4%}", help="No máximo n clientes no sistema")
                
                c4, c5, _ = st.columns(3)
                c4.metric(f"P(N < {n_val})", f"{p_lt:.4%}", help="Menos de n clientes no sistema")
                c5.metric(f"P(N ≥ {n_val})", f"{p_ge:.4%}", help="Pelo menos n clientes no sistema")
            else:
                st.info("Cálculos de probabilidade do número de clientes não estão disponíveis para este modelo.")
                
        with tab2:
            st.markdown("### Probabilidade do tempo de espera/permanência exceder um limite")
            if escolha in ["M/M/1", "M/M/s"]:
                t_val = st.number_input("Tempo limite (t)", min_value=0.0, value=1.0, step=0.1, key="prob_t_input")
                
                if escolha == "M/M/1":
                    p_w = calcular_prob_w_greater_t_mm1(lamb, mu, t_val)
                    p_wq = calcular_prob_wq_greater_t_mm1(lamb, mu, t_val)
                else: # M/M/s
                    p_w = calcular_prob_w_greater_t_mms(lamb, mu, s, t_val)
                    p_wq = calcular_prob_wq_greater_t_mms(lamb, mu, s, t_val)
                    
                c1, c2 = st.columns(2)
                c1.metric(f"P(W > {t_val})", f"{p_w:.4%}", help="Probabilidade de passar mais do que t no sistema")
                c2.metric(f"P(Wq > {t_val})", f"{p_wq:.4%}", help="Probabilidade de esperar mais do que t na fila")
            else:
                st.info("Probabilidade de espera temporal (W > t e Wq > t) está disponível analiticamente para M/M/1 e M/M/s.")
                
        with tab3:
            st.markdown("### Processo de Poisson (Chegadas e Atendimentos em um Período)")
            st.markdown("Verifique a probabilidade de chegadas ou atendimentos com base nos parâmetros atuais do sistema.")
            
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                t_window = st.number_input("Intervalo de tempo (T)", min_value=0.0001, value=1.0, step=0.1, key="poisson_t")
            with c_p2:
                events_x = st.number_input("Número de eventos (x)", min_value=0, value=5, step=1, key="poisson_x")
                
            p_arr = calcular_poisson_prob(lamb, t_window, events_x)
            p_serv = calcular_poisson_prob(mu, t_window, events_x)
            
            c1, c2 = st.columns(2)
            c1.metric(f"P(x = {events_x} chegadas em T = {t_window})", f"{p_arr:.4%}")
            c2.metric(f"P(x = {events_x} atendimentos em T = {t_window})", f"{p_serv:.4%}", help="Assumindo que o servidor está ocupado")
    elif res is None:
        st.error("A taxa de chegada deve ser menor que a capacidade total de atendimento (λ < sμ).")