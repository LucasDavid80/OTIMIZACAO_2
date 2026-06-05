import math

# ===========================
# M/M/1
# ===========================
def mm1():
    print("\n=== MODELO M/M/1 ===")

    lamb = float(input("Taxa de chegada λ: "))
    mu = float(input("Taxa de atendimento μ: "))

    if lamb >= mu:
        print("Sistema instável!")
        return

    rho = lamb / mu

    P0 = 1 - rho
    L = lamb / (mu - lamb)
    Lq = lamb**2 / (mu * (mu - lamb))
    W = L / lamb
    Wq = Lq / lamb

    mostrar_resultados(P0, L, Lq, W, Wq, rho)


# ===========================
# M/M/s
# ===========================
def mm_s():
    print("\n=== MODELO M/M/s ===")

    lamb = float(input("Taxa de chegada λ: "))
    mu = float(input("Taxa de atendimento μ: "))
    s = int(input("Número de servidores s: "))

    rho = lamb / (s * mu)

    if rho >= 1:
        print("Sistema instável!")
        return

    soma = sum((lamb / mu) ** n / math.factorial(n)
               for n in range(s))

    termo = ((lamb / mu) ** s) / (
            math.factorial(s) * (1 - rho)
    )

    P0 = 1 / (soma + termo)

    Lq = (
            P0 *
            ((lamb / mu) ** s) *
            rho /
            (math.factorial(s) * (1 - rho) ** 2)
    )

    L = Lq + lamb / mu

    Wq = Lq / lamb
    W = L / lamb

    mostrar_resultados(P0, L, Lq, W, Wq, rho)

# M/M/1/K
def mm1k():
    print("\n=== MODELO M/M/1/K ===")

    lamb = float(input("Taxa de chegada λ: "))
    mu = float(input("Taxa de atendimento μ: "))
    K = int(input("Capacidade máxima K: "))

    rho = lamb / mu

    P0 = (1 - rho) / (1 - rho ** (K + 1))

    Pk = P0 * rho ** K

    L = (
            rho / (1 - rho)
            - ((K + 1) * rho ** (K + 1))
            / (1 - rho ** (K + 1))
    )

    lamb_barra = lamb * (1 - Pk)

    Lq = L - (1 - P0)

    W = L / lamb_barra
    Wq = Lq / lamb_barra

    mostrar_resultados(P0, L, Lq, W, Wq, rho)


# ===========================
# M/M/s/K
# ===========================
def mmsk():
    print("\n=== MODELO M/M/s/K ===")

    lamb = float(input("Taxa de chegada λ: "))
    mu = float(input("Taxa de atendimento μ: "))
    s = int(input("Número de servidores s: "))
    K = int(input("Capacidade máxima K: "))

    rho = lamb / (s * mu)

    soma1 = sum(
        ((lamb / mu) ** n) / math.factorial(n)
        for n in range(s)
    )

    soma2 = sum(
        ((lamb / mu) ** n) /
        (math.factorial(s) * s ** (n - s))
        for n in range(s, K + 1)
    )

    P0 = 1 / (soma1 + soma2)

    probs = []

    for n in range(K + 1):

        if n < s:
            pn = ((lamb / mu) ** n) / math.factorial(n) * P0

        else:
            pn = (
                    ((lamb / mu) ** n)
                    /
                    (math.factorial(s) * s ** (n - s))
            ) * P0

        probs.append(pn)

    L = sum(n * probs[n] for n in range(K + 1))

    Lq = sum(
        max(0, n - s) * probs[n]
        for n in range(K + 1)
    )

    lamb_barra = lamb * (1 - probs[K])

    W = L / lamb_barra
    Wq = Lq / lamb_barra

    mostrar_resultados(P0, L, Lq, W, Wq, rho)


# ===========================
# M/M/1/N
# ===========================
def mm1n():
    print("\n=== MODELO M/M/1/N ===")

    lamb = float(input("Taxa de chegada λ: "))
    mu = float(input("Taxa de atendimento μ: "))
    N = int(input("População N: "))

    soma = 0

    for n in range(N + 1):
        soma += (
                math.factorial(N)
                /
                math.factorial(N - n)
        ) * (lamb / mu) ** n

    P0 = 1 / soma

    L = N - (mu / lamb) * (1 - P0)

    Lq = N - ((lamb + mu) / lamb) * (1 - P0)

    lamb_barra = lamb * (N - L)

    W = L / lamb_barra
    Wq = Lq / lamb_barra

    mostrar_resultados(P0, L, Lq, W, Wq)


# ===========================
# M/M/s/N
# ===========================
def mmsn():
    print("\n=== MODELO M/M/s/N ===")

    lamb = float(input("Taxa de chegada λ: "))
    mu = float(input("Taxa de atendimento μ: "))
    s = int(input("Número de servidores s: "))
    N = int(input("População N: "))

    soma = 0

    for n in range(s):

        soma += (
                math.factorial(N)
                /
                (
                        math.factorial(N - n)
                        * math.factorial(n)
                )
        ) * (lamb / mu) ** n

    for n in range(s, N + 1):

        soma += (
                math.factorial(N)
                /
                (
                        math.factorial(N - n)
                        * math.factorial(s)
                        * s ** (n - s)
                )
        ) * (lamb / mu) ** n

    P0 = 1 / soma

    probs = [P0]

    for n in range(1, N + 1):

        if n < s:

            pn = (
                    math.factorial(N)
                    /
                    (
                            math.factorial(N - n)
                            * math.factorial(n)
                    )
            ) * (lamb / mu) ** n * P0

        else:

            pn = (
                    math.factorial(N)
                    /
                    (
                            math.factorial(N - n)
                            * math.factorial(s)
                            * s ** (n - s)
                    )
            ) * (lamb / mu) ** n * P0

        probs.append(pn)

    L = sum(n * probs[n] for n in range(N + 1))

    Lq = L - (lamb / mu) * (N - L)

    lamb_barra = lamb * (N - L)

    W = L / lamb_barra
    Wq = Lq / lamb_barra

    mostrar_resultados(P0, L, Lq, W, Wq)


# ===========================
# IMPRESSÃO
# ===========================
def mostrar_resultados(P0, L, Lq, W, Wq, rho=None):

    print("\nRESULTADOS")

    if rho is not None:
        print(f"ρ  = {rho:.4f}")

    print(f"P0 = {P0:.4f}")
    print(f"L  = {L:.4f}")
    print(f"Lq = {Lq:.4f}")
    print(f"W  = {W:.4f}")
    print(f"Wq = {Wq:.4f}")


# ===========================
# MENU
# ===========================
while True:

    print("\n==========================")
    print("MODELOS DE FILAS")
    print("==========================")
    print("1 - M/M/1")
    print("2 - M/M/s")
    print("3 - M/M/1/K")
    print("4 - M/M/s/K")
    print("5 - M/M/1/N")
    print("6 - M/M/s/N")
    print("0 - Sair")

    opcao = input("\nEscolha o modelo: ")

    if opcao == "1":
        mm1()

    elif opcao == "2":
        mm_s()

    elif opcao == "3":
        mm1k()

    elif opcao == "4":
        mmsk()

    elif opcao == "5":
        mm1n()

    elif opcao == "6":
        mmsn()

    elif opcao == "0":
        break

    else:
        print("Opção inválida!")