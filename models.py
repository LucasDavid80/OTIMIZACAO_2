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

def calcular_mg1(lamb, mu, sigma):
    rho = lamb / mu
    if rho >= 1: return None
    es = 1 / mu
    var_s = sigma ** 2
    wq = (lamb * (var_s + es**2)) / (2 * (1 - rho))
    w = wq + es
    lq = lamb * wq
    l = lamb * w
    p0 = 1 - rho
    return {"rho": rho, "P0": p0, "L": l, "Lq": lq, "W": w, "Wq": wq}

# Placeholders para Prioridades
def calcular_prioridade_non_preemptive():
    return None

def calcular_prioridade_preemptive():
    return None
