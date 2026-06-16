import math


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
    Lq = P0 * ((lamb / mu) ** s) * rho / (math.factorial(s) * (1 - rho) ** 2)
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
    Pk = P0 * (rho ** K)
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
        if n < s:
            pn = ((lamb / mu) ** n) / math.factorial(n) * P0
        else:
            pn = (((lamb / mu) ** n) / (math.factorial(s) * s ** (n - s))) * P0
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
    soma = sum(
        (math.factorial(N) / (math.factorial(N - n) * math.factorial(n))) * (lamb / mu) ** n
        for n in range(s)
    )
    soma += sum(
        (math.factorial(N) / (math.factorial(N - n) * math.factorial(s) * s ** (n - s))) * (lamb / mu) ** n
        for n in range(s, N + 1)
    )
    P0 = 1 / soma
    probs = []
    for n in range(N + 1):
        if n < s:
            pn = (math.factorial(N) / (math.factorial(N - n) * math.factorial(n))) * (lamb / mu) ** n * P0
        else:
            pn = (math.factorial(N) / (math.factorial(N - n) * math.factorial(s) * s ** (n - s))) * (lamb / mu) ** n * P0
        probs.append(pn)
    L = sum(n * probs[n] for n in range(N + 1))
    Lq = L - (lamb / mu) * (N - L)
    lamb_barra = lamb * (N - L)
    W = L / lamb_barra
    Wq = Lq / lamb_barra
    return {"P0": P0, "L": L, "Lq": Lq, "W": W, "Wq": Wq}


def calcular_mg1(lamb, mu, sigma):
    rho = lamb / mu
    if rho >= 1: return None
    es = 1 / mu
    var_s = sigma ** 2
    wq = (lamb * (var_s + es ** 2)) / (2 * (1 - rho))
    w = wq + es
    lq = lamb * wq
    l = lamb * w
    p0 = 1 - rho
    return {"rho": rho, "P0": p0, "L": l, "Lq": lq, "W": w, "Wq": wq}


def calcular_prioridade_non_preemptive(lambdas, mu, s):
    """
    Prioridade Não-Preemptiva (exponencial, μ comum a todas as classes).

    Parâmetros
    ----------
    lambdas : list of float  — taxas de chegada por classe (ordem decrescente de prioridade)
    mu      : float          — taxa de atendimento (igual para todas as classes)
    s       : int            — número de servidores

    Retorna
    -------
    list of dict com chaves: classe, lamb, mu, rho, rho_total, Wq, W, Lq, L
    None se o sistema for instável.
    """
    n_classes = len(lambdas)
    lamb_total = sum(lambdas)
    rhos = [l / (s * mu) for l in lambdas]
    rho_total = sum(rhos)

    if rho_total >= 1:
        return None

    # Fator F do denominador (slide 11 do professor):
    # F = s! * (sμ - λ_total) / r^s * Σ_{j=0}^{s-1} r^j/j!  +  sμ
    r = lamb_total / mu
    soma_erlang = sum(r ** j / math.factorial(j) for j in range(s))
    F = math.factorial(s) * (s * mu - lamb_total) / r ** s * soma_erlang + s * mu

    # σ_k = Σ_{i=1}^{k} λi / (s*μ)  acumulado (σ_0 = 0)
    sigma = [0.0]
    for l in lambdas:
        sigma.append(sigma[-1] + l / (s * mu))

    resultados = []
    for k in range(n_classes):
        Wk  = 1.0 / (F * (1 - sigma[k]) * (1 - sigma[k + 1])) + 1.0 / mu
        Wqk = Wk - 1.0 / mu
        Lk  = lambdas[k] * Wk
        Lqk = Lk - lambdas[k] / mu
        resultados.append({
            "classe":    k + 1,
            "lamb":      lambdas[k],
            "mu":        mu,
            "rho":       rhos[k],
            "rho_total": rho_total,
            "Wq": Wqk, "W": Wk,
            "Lq": Lqk, "L": Lk,
        })
    return resultados


def calcular_prioridade_preemptive(lambdas, mu, s):
    """
    Prioridade Preemptiva (exponencial, μ comum a todas as classes).

    Na disciplina preemptiva, um cliente de classe k em serviço é
    interrompido ao chegar um cliente de classe superior (menor índice).
    Pela formulação de Kleinrock, a espera de cada classe k depende
    apenas das classes de prioridade maior ou igual a k (σ_k acumulado).

    Parâmetros
    ----------
    lambdas : list of float  — taxas de chegada por classe (ordem decrescente de prioridade)
    mu      : float          — taxa de atendimento (igual para todas as classes)
    s       : int            — número de servidores

    Retorna
    -------
    list of dict com chaves: classe, lamb, mu, rho, rho_total, Wq, W, Lq, L
    None se o sistema for instável.
    """
    n_classes = len(lambdas)
    lamb_total = sum(lambdas)
    rhos = [l / (s * mu) for l in lambdas]
    rho_total = sum(rhos)

    if rho_total >= 1:
        return None

    # Fator F — mesmo da non-preemptive (depende do tráfego total e de s)
    r = lamb_total / mu
    soma_erlang = sum(r ** j / math.factorial(j) for j in range(s))
    F = math.factorial(s) * (s * mu - lamb_total) / r ** s * soma_erlang + s * mu

    # σ_k acumulado: σ_0 = 0, σ_k = Σ_{i=1}^{k} λi / (s*μ)
    sigma = [0.0]
    for l in lambdas:
        sigma.append(sigma[-1] + l / (s * mu))

    resultados = []
    for k in range(n_classes):
        # Formulação preemptiva de Kleinrock:
        # Wqk = 1/F * [1/(1 - σ_k) - 1/(1 - σ_{k+1})]  /  λ_k
        # que equivale a calcular a diferença das funções acumuladas dividida por λ_k,
        # produzindo o tempo médio de espera na fila para a classe k.
        #
        # Como F já contém a dimensão de taxa (serve como denominador da fórmula geral),
        # usamos a forma compacta:
        #   Wqk = (1/F) * (σ_{k+1} - σ_k) / ((1 - σ_k) * (1 - σ_{k+1}))
        # que é a versão preemptiva — diferente da non-preemptive que usa
        # 1 / (F * (1-σ_k) * (1-σ_{k+1}))  diretamente sem o fator (σ_{k+1}-σ_k).
        delta_sigma = sigma[k + 1] - sigma[k]   # = λ_k / (s*μ) = ρ_k
        Wqk = delta_sigma / (F * (1 - sigma[k]) * (1 - sigma[k + 1]))
        Wk  = Wqk + 1.0 / mu
        Lqk = lambdas[k] * Wqk
        Lk  = lambdas[k] * Wk
        resultados.append({
            "classe":    k + 1,
            "lamb":      lambdas[k],
            "mu":        mu,
            "rho":       rhos[k],
            "rho_total": rho_total,
            "Wq": Wqk, "W": Wk,
            "Lq": Lqk, "L": Lk,
        })
    return resultados