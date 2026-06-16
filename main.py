from models import (
    calcular_mm1, calcular_mms, calcular_mm1k, calcular_mmsk,
    calcular_mm1n, calcular_mmsn, calcular_mg1,
    calcular_prioridade_non_preemptive,
)


def mostrar_resultados(res):
    if res is None:
        print("\nErro: Sistema instável (λ >= sμ) ou parâmetros inválidos.")
        return
    print("\n" + "=" * 30)
    print("      RESULTADOS")
    print("=" * 30)
    if "rho" in res:
        print(f"Utilização (ρ):      {res['rho']:.4f}")
    print(f"Prob. Vazio (P0):    {res['P0']:.4f}")
    print(f"L (no Sistema):      {res['L']:.4f}")
    print(f"Lq (na Fila):        {res['Lq']:.4f}")
    print(f"W (no Sistema):      {res['W']:.4f}")
    print(f"Wq (na Fila):        {res['Wq']:.4f}")
    print("=" * 30)


def mostrar_resultados_prioridade(resultados):
    if resultados is None:
        print("\nErro: Sistema instável (ρ total ≥ 1) ou parâmetros inválidos.")
        return
    print("\n" + "=" * 55)
    print("   RESULTADOS — PRIORIDADE NÃO-PREEMPTIVA")
    print("=" * 55)
    print(f"  ρ total = {resultados[0]['rho_total']:.4f}")
    print("=" * 55)
    for r in resultados:
        print(f"\n  Classe {r['classe']}  (λ={r['lamb']}, μ={r['mu']}, ρ={r['rho']:.4f})")
        print(f"    Wq (espera na fila):   {r['Wq']:.4f}")
        print(f"    W  (tempo no sistema): {r['W']:.4f}")
        print(f"    Lq (clientes na fila): {r['Lq']:.4f}")
        print(f"    L  (clientes no sist): {r['L']:.4f}")
    print("=" * 55)


def main():
    while True:
        print("\n==========================")
        print("    MODELOS DE FILAS")
        print("==========================")
        print("1 - M/M/1")
        print("2 - M/M/s")
        print("3 - M/M/1/K")
        print("4 - M/M/s/K")
        print("5 - M/M/1/N")
        print("6 - M/M/s/N")
        print("7 - M/G/1")
        print("8 - Prioridade Não-Preemptiva")
        print("0 - Sair")

        opcao = input("\nEscolha o modelo: ").strip()
        if opcao == "0":
            break
        if opcao not in "12345678":
            print("Opção inválida!")
            continue

        if opcao == "8":
            mu = float(input("Taxa de atendimento μ: "))
            s = int(input("Número de servidores s: "))
            num_classes = int(input("Número de classes de prioridade: "))
            lambdas = []
            for i in range(num_classes):
                lamb = float(input(f"  λ_{i+1} (taxa de chegada da classe {i+1}): "))
                lambdas.append(lamb)
            resultados = calcular_prioridade_non_preemptive(lambdas, mu, s)
            mostrar_resultados_prioridade(resultados)
            continue

        lamb = float(input("Taxa de chegada λ: "))
        mu   = float(input("Taxa de atendimento μ: "))

        res = None
        if opcao == "1":
            res = calcular_mm1(lamb, mu)
        elif opcao == "2":
            s = int(input("Número de servidores s: "))
            res = calcular_mms(lamb, mu, s)
        elif opcao == "3":
            K = int(input("Capacidade máxima K: "))
            res = calcular_mm1k(lamb, mu, K)
        elif opcao == "4":
            s = int(input("Número de servidores s: "))
            K = int(input("Capacidade máxima K: "))
            res = calcular_mmsk(lamb, mu, s, K)
        elif opcao == "5":
            N = int(input("População N: "))
            res = calcular_mm1n(lamb, mu, N)
        elif opcao == "6":
            s = int(input("Número de servidores s: "))
            N = int(input("População N: "))
            res = calcular_mmsn(lamb, mu, s, N)
        elif opcao == "7":
            sigma = float(input("Desvio padrão do serviço σ: "))
            res = calcular_mg1(lamb, mu, sigma)
        if opcao == "8":
            mu = float(input("Taxa de atendimento μ: "))
            s = int(input("Número de servidores s: "))
            num_classes = int(input("Número de classes de prioridade: "))
            lambdas = []
            for i in range(num_classes):
                lamb = float(input(f"  λ_{i+1} (taxa de chegada da classe {i+1}): "))
                lambdas.append(lamb)
            resultados = calcular_prioridade_non_preemptive(lambdas, mu, s)
            mostrar_resultados_prioridade(resultados)

        mostrar_resultados(res)


if __name__ == "__main__":
    main()