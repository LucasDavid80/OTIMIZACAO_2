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
    probs = [P0 * (rho ** n) for n in range(K + 1)]
    return {"rho": rho, "P0": P0, "L": L, "Lq": Lq, "W": W, "Wq": Wq, "probs": probs}


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
    return {"rho": rho, "P0": P0, "L": L, "Lq": Lq, "W": W, "Wq": Wq, "probs": probs}


def calcular_mm1n(lamb, mu, N):
    soma = sum((math.factorial(N) / math.factorial(N - n)) * (lamb / mu) ** n for n in range(N + 1))
    P0 = 1 / soma
    L = N - (mu / lamb) * (1 - P0)
    Lq = N - ((lamb + mu) / lamb) * (1 - P0)
    lamb_barra = lamb * (N - L)
    W = L / lamb_barra
    Wq = Lq / lamb_barra
    probs = [(math.factorial(N) / math.factorial(N - n)) * (lamb / mu) ** n * P0 for n in range(N + 1)]
    return {"P0": P0, "L": L, "Lq": Lq, "W": W, "Wq": Wq, "probs": probs}


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
    return {"P0": P0, "L": L, "Lq": Lq, "W": W, "Wq": Wq, "probs": probs}


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
    n_classes = len(lambdas)
    lamb_total = sum(lambdas)
    rhos = [l / (s * mu) for l in lambdas]
    rho_total = sum(rhos)

    if rho_total >= 1:
        return None

    r = lamb_total / mu
    soma_erlang = sum(r ** j / math.factorial(j) for j in range(s))
    F = math.factorial(s) * (s * mu - lamb_total) / r ** s * soma_erlang + s * mu

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
    if mu <= 0 or s <= 0:
        return None

    rho_total = sum(lambdas) / (s * mu)

    if rho_total >= 1:
        return None

    resultados = []

    soma_anterior = 0

    for k, lamb_k in enumerate(lambdas):

        soma_atual = soma_anterior + lamb_k

        fator1 = 1 - (soma_anterior / (s * mu))
        fator2 = 1 - (soma_atual / (s * mu))

        W = (1 / mu) / (fator1 * fator2)

        Wq = W - (1 / mu)

        lambda_acumulado = soma_atual

        L = lambda_acumulado * W

        Lq = L - (lambda_acumulado / mu)

        resultados.append({
            "classe": k + 1,
            "lamb": lamb_k,
            "mu": mu,
            "rho": lamb_k / (s * mu),
            "rho_total": rho_total,
            "W": W,
            "Wq": Wq,
            "L": L,
            "Lq": Lq
        })

        soma_anterior = soma_atual

    return resultados


def calcular_prob_n_mm1(lamb, mu, n):
    """
    Calcula a probabilidade de haver exatamente n clientes no sistema (M/M/1).
    Fórmula do material: P(n) = (1 - rho) * rho^n
    """
    rho = lamb / mu
    return (1 - rho) * (rho ** n)


def calcular_prob_greater_r_mm1(lamb, mu, r):
    """
    Calcula a probabilidade de haver mais de r clientes no sistema (M/M/1).
    Fórmula do material: P(n > r) = (lambda / mu)^(r + 1)
    """
    rho = lamb / mu
    return rho ** (r + 1)


def calcular_prob_w_greater_t_mm1(lamb, mu, t):
    """
    Calcula a probabilidade de o tempo de espera no sistema (W) ser maior que t (M/M/1).
    Fórmula do material: P(W > t) = e^(-mu * (1 - rho) * t)
    """
    rho = lamb / mu
    return math.exp(-mu * (1 - rho) * t)


def calcular_prob_wq_greater_t_mm1(lamb, mu, t):
    """
    Calcula a probabilidade de o tempo de espera na fila (Wq) ser maior que t (M/M/1).
    Fórmula do material: P(Wq > t) = rho * e^(-mu * (1 - rho) * t)
    """
    rho = lamb / mu
    return rho * math.exp(-mu * (1 - rho) * t)


def calcular_prob_n_mms(lamb, mu, s, n):
    """
    Calcula a probabilidade de haver exatamente n clientes no sistema (M/M/s).
    Fórmula do material:
    n <= s: Pn = ((lambda/mu)^n / n!) * P0
    n >= s: Pn = ((lambda/mu)^n / (s! * s^(n-s))) * P0
    """
    rho = lamb / (s * mu)
    soma = sum((lamb / mu) ** i / math.factorial(i) for i in range(s))
    termo = ((lamb / mu) ** s) / (math.factorial(s) * (1 - rho))
    P0 = 1 / (soma + termo)
    if n <= s:
        return ((lamb / mu) ** n) / math.factorial(n) * P0
    else:
        return ((lamb / mu) ** n) / (math.factorial(s) * (s ** (n - s))) * P0


def calcular_prob_w_greater_t_mms(lamb, mu, s, t):
    """
    Calcula a probabilidade de o tempo de espera no sistema (W) ser maior que t (M/M/s).
    Fórmula do material:
    P(W > t) = e^(-mu*t) * [ 1 + (P0 * (lambda/mu)^s) / (s! * (1 - rho)) * (1 - e^(-mu*t*(s - 1 - lambda/mu))) / (s - 1 - lambda/mu) ]
    """
    rho = lamb / (s * mu)
    soma = sum((lamb / mu) ** i / math.factorial(i) for i in range(s))
    termo = ((lamb / mu) ** s) / (math.factorial(s) * (1 - rho))
    P0 = 1 / (soma + termo)
    
    coef = (P0 * (lamb / mu) ** s) / (math.factorial(s) * (1 - rho))
    exponent = s - 1 - (lamb / mu)
    
    if abs(exponent) < 1e-9:
        term = mu * t
    else:
        term = (1 - math.exp(-mu * t * exponent)) / exponent
        
    return math.exp(-mu * t) * (1 + coef * term)


def calcular_prob_wq_greater_t_mms(lamb, mu, s, t):
    """
    Calcula a probabilidade de o tempo de espera na fila (Wq) ser maior que t (M/M/s).
    Fórmula do material:
    P(Wq > t) = (1 - P(Wq = 0)) * e^(-s*mu*(1-rho)*t)
    onde P(Wq = 0) = sum_{n=0}^{s-1} Pn
    """
    rho = lamb / (s * mu)
    soma = sum((lamb / mu) ** i / math.factorial(i) for i in range(s))
    termo = ((lamb / mu) ** s) / (math.factorial(s) * (1 - rho))
    P0 = 1 / (soma + termo)
    
    P_wq_0 = sum(((lamb / mu) ** n) / math.factorial(n) * P0 for n in range(s))
    return (1 - P_wq_0) * math.exp(-s * mu * (1 - rho) * t)


def calcular_poisson_prob(rate, T, x):
    """
    Calcula a probabilidade de ocorrerem exatamente x eventos em um intervalo T
    sob um processo de Poisson com taxa 'rate'.
    Fórmula do material: P(x) = (rate * T)^x * e^(-rate * T) / x!
    """
    mean = rate * T
    return (math.exp(-mean) * (mean ** x)) / math.factorial(x)