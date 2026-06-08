from models import (
    calcular_mm1, calcular_mms, calcular_mm1k, calcular_mmsk,
    calcular_mm1n, calcular_mmsn, calcular_mg1
)

def mostrar_resultados(res):
    if res is None:
        print("\nErro: Sistema instável (λ >= sμ) ou parâmetros inválidos.")
        return

    print("\n" + "="*30)
    print("      RESULTADOS")
    print("="*30)
    if "rho" in res: print(f"Utilização (ρ):      {res['rho']:.4f}")
    print(f"Prob. Vazio (P0):    {res['P0']:.4f}")
    print(f"L (no Sistema):      {res['L']:.4f}")
    print(f"Lq (na Fila):        {res['Lq']:.4f}")
    print(f"W (no Sistema):      {res['W']:.4f}")
    print(f"Wq (na Fila):        {res['Wq']:.4f}")
    print("="*30)

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
        print("0 - Sair")
        
        opcao = input("\nEscolha o modelo: ")
        if opcao == "0": break
        if opcao not in "1234567":
            print("Opção inválida!")
            continue

        lamb = float(input("Taxa de chegada λ: "))
        mu = float(input("Taxa de atendimento μ: "))
        
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

        mostrar_resultados(res)

if __name__ == "__main__":
    main()
