import pytest
import math
from models import (
    calcular_mm1,
    calcular_mms,
    calcular_mm1k,
    calcular_mmsk,
    calcular_mm1n,
    calcular_mmsn,
    calcular_mg1,
    calcular_prioridade_non_preemptive,
    calcular_prioridade_preemptive,
    calcular_prob_n_mm1,
    calcular_prob_greater_r_mm1,
    calcular_prob_w_greater_t_mm1,
    calcular_prob_wq_greater_t_mm1,
    calcular_prob_n_mms,
    calcular_prob_w_greater_t_mms,
    calcular_prob_wq_greater_t_mms,
    calcular_poisson_prob,
)

# APROXIMAÇÃO DE COMPARAÇÃO DE FLOATS (Tolerância padrão para arredondamentos dos PDFs)
TOL = 1e-3


# ==============================================================================
# 1. MODELO M/M/1
# ==============================================================================

def test_mm1_armazem_caminhoes():
    """
    Lista MMs - Ex 5:
    Caminhões chegam no armazém à taxa de 3 por hora (lambda = 3).
    Tempo médio de atendimento é de 15 minutos (1/mu = 0.25h -> mu = 4).
    Gabarito esperado: Lq = 2.25, L = 3.0, Wq = 0.75h, W = 1.0h, rho = 0.75, P0 = 0.25.
    """
    res = calcular_mm1(lamb=3.0, mu=4.0)
    assert res is not None
    assert pytest.approx(res["Lq"], abs=TOL) == 2.25
    assert pytest.approx(res["L"], abs=TOL) == 3.0
    assert pytest.approx(res["Wq"], abs=TOL) == 0.75
    assert pytest.approx(res["W"], abs=TOL) == 1.0
    assert pytest.approx(res["rho"], abs=TOL) == 0.75
    assert pytest.approx(res["P0"], abs=TOL) == 0.25


def test_mm1_cooperativa_agricola():
    """
    Lista MMs - Ex 6:
    Equipe descarrega 5 caminhões por hora (mu = 5).
    A taxa de chegada para o tempo médio de espera na fila ser 0.8h é lambda = 4.
    Gabarito esperado para lambda = 4: Lq = 3.2, L = 4.0, W = 1.0, Wq = 0.8.
    """
    res = calcular_mm1(lamb=4.0, mu=5.0)
    assert res is not None
    assert pytest.approx(res["Lq"], abs=TOL) == 3.2
    assert pytest.approx(res["L"], abs=TOL) == 4.0
    assert pytest.approx(res["Wq"], abs=TOL) == 0.8
    assert pytest.approx(res["W"], abs=TOL) == 1.0


# ==============================================================================
# 2. MODELO M/M/s
# ==============================================================================

def test_mms_hospital_municipal():
    """
    Lista MMs - Ex 7 (s = 2 médicos):
    Taxa de chegada de 1 a cada 30min -> lambda = 2.0 por hora.
    Médico precisa de 20min em média -> mu = 3.0 por hora.
    Gabarito esperado para s = 2: rho = 0.3333, P0 = 0.5000, L = 0.7500, Lq = 0.0833, Wq = 0.0417, W = 0.3750.
    """
    res = calcular_mms(lamb=2.0, mu=3.0, s=2)
    assert res is not None
    assert pytest.approx(res["rho"], abs=TOL) == 0.3333
    assert pytest.approx(res["P0"], abs=TOL) == 0.5000
    assert pytest.approx(res["L"], abs=TOL) == 0.7500
    assert pytest.approx(res["Lq"], abs=TOL) == 0.0833
    assert pytest.approx(res["Wq"], abs=TOL) == 0.0417  # 1/24 horas
    assert pytest.approx(res["W"], abs=TOL) == 0.3750   # 3/8 horas


def test_mms_security_trust_bank():
    """
    Lista MMs - Ex 15:
    4 caixas (s = 4). Taxa de chegada lambda = 2.0/min. Tempo médio 1min (mu = 1.0).
    Projeção para 1 ano: lambda = 3.0/min.
    Gabarito esperado para lambda = 2.0 (atual): Lq = 0.1739.
    Gabarito esperado para lambda = 3.0 (projeção): Lq = 1.5283.
    """
    res_atual = calcular_mms(lamb=2.0, mu=1.0, s=4)
    assert res_atual is not None
    assert pytest.approx(res_atual["Lq"], abs=TOL) == 0.1739

    res_proj = calcular_mms(lamb=3.0, mu=1.0, s=4)
    assert res_proj is not None
    assert pytest.approx(res_proj["Lq"], abs=TOL) == 1.5283


# ==============================================================================
# 3. MODELO M/M/1/K
# ==============================================================================

def test_mm1k_agencia_bancaria():
    """
    Lista MMsk - Ex 1 (s = 1):
    Chegada lambda = 2.0 clientes/min. Serviço mu = 4.0 clientes/min (0.25 min).
    Capacidade máxima K = 5.
    Gabarito esperado: P0 = 0.5079, L = 0.9048, Lq = 0.4127, W = 0.4597, Wq = 0.2097.
    """
    res = calcular_mm1k(lamb=2.0, mu=4.0, K=5)
    assert res is not None
    assert pytest.approx(res["P0"], abs=TOL) == 0.5079
    assert pytest.approx(res["L"], abs=TOL) == 0.9048
    assert pytest.approx(res["Lq"], abs=TOL) == 0.4127
    assert pytest.approx(res["W"], abs=TOL) == 0.4597
    assert pytest.approx(res["Wq"], abs=TOL) == 0.2097


def test_mm1k_laboratorio_radiologia():
    """
    Lista MMsk - Ex 2:
    Capacidade comporta máximo de 4 pacientes (K = 4).
    Taxa de chegada lambda = 1.0/hora. Tempo médio de 45 minutos (1/mu = 0.75h -> mu = 4/3).
    Gabarito esperado: L = 1.4443, Wq = 0.8614, Pk (P4) = 0.1037 (probabilidade de encontrar cheio).
    """
    res = calcular_mm1k(lamb=1.0, mu=4.0/3.0, K=4)
    assert res is not None
    assert pytest.approx(res["L"], abs=TOL) == 1.4443
    assert pytest.approx(res["Wq"], abs=TOL) == 0.8614

    # Validando probabilidade de barramento (sistema cheio)
    # P_k = P0 * rho^K
    rho = 1.0 / (4.0/3.0)
    P_K = res["P0"] * (rho ** 4)
    assert pytest.approx(P_K, abs=TOL) == 0.1037


# ==============================================================================
# 4. MODELO M/M/s/K
# ==============================================================================

def test_mmsk_aeroporto_pistas():
    """
    Lista MMsk - Ex 4 (2 pistas):
    Chegada lambda = 15.0/hora. Pouso mu = 20.0/hora (3 min). s = 2.
    Apenas 3 aviões em espera (o gabarito do professor assume capacidade total do sistema K = 4).
    Gabarito esperado: Lq = 0.0848, Wq = 0.3455 min (0.00576h), P4 (bloqueio) = 0.0182.
    """
    res = calcular_mmsk(lamb=15.0, mu=20.0, s=2, K=4)
    assert res is not None
    assert pytest.approx(res["Lq"], abs=TOL) == 0.0848
    assert pytest.approx(res["Wq"], abs=TOL) == 0.00576  # 0.3455 minutos

    # Probs no sistema: calcular probabilidade de K (bloqueado)
    soma1 = sum(((15.0 / 20.0) ** n) / math.factorial(n) for n in range(2))
    soma2 = sum(((15.0 / 20.0) ** n) / (math.factorial(2) * 2 ** (n - 2)) for n in range(2, 5))
    P0_calc = 1.0 / (soma1 + soma2)
    P4_calc = (((15.0 / 20.0) ** 4) / (math.factorial(2) * 2 ** 2)) * P0_calc
    assert pytest.approx(P4_calc, abs=TOL) == 0.0182


def test_mmsk_radiologia_dois_equipamentos():
    """
    Lista MMsk - Ex 5 (2 equipamentos):
    Taxa de chegada lambda = 1.0/hora. Tempo médio 45 min (mu = 4/3). s = 2.
    O gabarito assume capacidade do sistema K = 4 (apesar do texto falar em comporta máximo 5 no lab).
    Gabarito esperado com K=4: L = 0.8212, Wq = 0.0864, P_bloqueio = 0.0182.
    """
    res = calcular_mmsk(lamb=1.0, mu=4.0/3.0, s=2, K=4)
    assert res is not None
    assert pytest.approx(res["L"], abs=TOL) == 0.8212
    assert pytest.approx(res["Wq"], abs=TOL) == 0.0864

    # Probs de bloqueio PK
    soma1 = sum(((1.0 / (4.0/3.0)) ** n) / math.factorial(n) for n in range(2))
    soma2 = sum(((1.0 / (4.0/3.0)) ** n) / (math.factorial(2) * 2 ** (n - 2)) for n in range(2, 5))
    P0_calc = 1.0 / (soma1 + soma2)
    P4_calc = (((1.0 / (4.0/3.0)) ** 4) / (math.factorial(2) * 2 ** 2)) * P0_calc
    assert pytest.approx(P4_calc, abs=TOL) == 0.0182


# ==============================================================================
# 5. MODELO M/M/1/N
# ==============================================================================

def test_mm1n_tecnico_duas_maquinas():
    """
    Lista MMsN - Ex 3:
    1 técnico (s = 1). População N = 2.
    Tempo médio de operação (1/lambda) = 10h -> lambda = 0.1/hora.
    Tempo médio de reparo (1/mu) = 8h -> mu = 0.125/hora.
    Gabarito esperado: P0 = 0.2577, L = 1.0722, Lq = 0.3299, W = 11.5556, Wq = 3.5556.
    """
    res = calcular_mm1n(lamb=0.1, mu=0.125, N=2)
    assert res is not None
    assert pytest.approx(res["P0"], abs=TOL) == 0.2577
    assert pytest.approx(res["L"], abs=TOL) == 1.0720
    assert pytest.approx(res["Lq"], abs=TOL) == 0.3300
    assert pytest.approx(res["W"], abs=TOL) == 11.5560
    assert pytest.approx(res["Wq"], abs=TOL) == 3.5560


def test_mm1n_forrester_manufacturing():
    """
    Lista MMsN - Ex 4 (1 técnico):
    1 técnico (s = 1). População N = 3.
    Tempo médio de operação (1/lambda) = 9h -> lambda = 1/9.
    Tempo médio de reparo (1/mu) = 2h -> mu = 0.5.
    Gabarito esperado: L = 0.7181, W = 2.832.
    """
    res = calcular_mm1n(lamb=1.0/9.0, mu=0.5, N=3)
    assert res is not None
    assert pytest.approx(res["L"], abs=TOL) == 0.7181
    assert pytest.approx(res["W"], abs=TOL) == 2.8320


# ==============================================================================
# 6. MODELO M/M/s/N
# ==============================================================================

def test_mmsn_quatro_maquinas_dois_tecnicos():
    """
    Lista MMsN - Ex 6:
    2 técnicos (s = 2). População N = 4.
    Quebra média a cada 100h -> lambda = 0.01/hora.
    Reparo médio de 10h -> mu = 0.1/hora.
    Gabarito esperado: P0 = 0.6820, L = 0.3677, Lq = 0.0045, W = 10.1239, Wq = 0.1239.
    """
    res = calcular_mmsn(lamb=0.01, mu=0.1, s=2, N=4)
    assert res is not None
    assert pytest.approx(res["P0"], abs=TOL) == 0.6820
    assert pytest.approx(res["L"], abs=TOL) == 0.3677
    assert pytest.approx(res["Lq"], abs=TOL) == 0.0045
    assert pytest.approx(res["W"], abs=TOL) == 10.1239
    assert pytest.approx(res["Wq"], abs=TOL) == 0.1239


def test_mmsn_forrester_dois_tecnicos():
    """
    Lista MMsN - Ex 4 (d - dois técnicos):
    2 técnicos (s = 2). População N = 3.
    Tempo de quebra 9h -> lambda = 1/9.
    Tempo de reparo 2h -> mu = 0.5.
    Gabarito esperado: L = 0.5528.
    """
    res = calcular_mmsn(lamb=1.0/9.0, mu=0.5, s=2, N=3)
    assert res is not None
    assert pytest.approx(res["L"], abs=TOL) == 0.5528


# ==============================================================================
# 7. MODELO M/G/1
# ==============================================================================

def test_mg1_teorico_sigma4():
    """
    Lista MG1 - Ex 1 (sigma = 4):
    lambda = 0.2, mu = 0.25, sigma = 4.0.
    Gabarito esperado: Lq = 3.20, L = 4.00, Wq = 16.00, W = 20.00.
    """
    res = calcular_mg1(lamb=0.2, mu=0.25, sigma=4.0)
    assert res is not None
    assert pytest.approx(res["Lq"], abs=TOL) == 3.2000
    assert pytest.approx(res["L"], abs=TOL) == 4.0000
    assert pytest.approx(res["Wq"], abs=TOL) == 16.0000
    assert pytest.approx(res["W"], abs=TOL) == 20.0000


def test_mg1_armazem_descarga_tempo_constante():
    """
    Lista MG1 - Ex 2:
    lambda = 3.0 por hora. Tempo de atendimento = 15 min (mu = 4.0).
    A resposta Lq = 1.125 assume atendimento CONSTANTE (Deterministic - M/D/1, sigma = 0).
    Gabarito esperado: Lq = 1.125, L = 1.875, Wq = 0.375, W = 0.625.
    """
    res = calcular_mg1(lamb=3.0, mu=4.0, sigma=0.0)
    assert res is not None
    assert pytest.approx(res["Lq"], abs=TOL) == 1.1250
    assert pytest.approx(res["L"], abs=TOL) == 1.8750
    assert pytest.approx(res["Wq"], abs=TOL) == 0.3750
    assert pytest.approx(res["W"], abs=TOL) == 0.6250


# ==============================================================================
# 8. PRIORIDADE NÃO-PREEMPTIVA
# ==============================================================================

def test_prioridade_non_preemptive_ferramentaria():
    """
    Lista MG1 - Ex 6 (Não-preemptivo):
    lambda = [2.0, 4.0, 2.0], mu = 10.0, s = 1.
    Gabarito esperado para tempo no sistema (W): W1 = 0.20, W2 = 0.35, W3 = 1.10.
    """
    res = calcular_prioridade_non_preemptive(lambdas=[2.0, 4.0, 2.0], mu=10.0, s=1)
    assert res is not None
    assert len(res) == 3
    assert pytest.approx(res[0]["W"], abs=TOL) == 0.2000
    assert pytest.approx(res[1]["W"], abs=TOL) == 0.3500
    assert pytest.approx(res[2]["W"], abs=TOL) == 1.1000


def test_prioridade_non_preemptive_southeast_airlines():
    """
    Lista MG1 - Ex 4 (Não-preemptivo):
    lambda_1 = 2 (primeira classe), lambda_2 = 10 (econômica). mu = 20. s = 1.
    Gabarito esperado:
      Classe 1: Wq = 0.033, W = 0.083, Lq = 0.067, L = 0.167
      Classe 2: Wq = 0.083, W = 0.133, Lq = 0.833, L = 1.333
    """
    res = calcular_prioridade_non_preemptive(lambdas=[2.0, 10.0], mu=20.0, s=1)
    assert res is not None
    assert len(res) == 2

    # Classe 1
    assert pytest.approx(res[0]["Wq"], abs=TOL) == 0.0333
    assert pytest.approx(res[0]["W"], abs=TOL) == 0.0833
    assert pytest.approx(res[0]["Lq"], abs=TOL) == 0.0667
    assert pytest.approx(res[0]["L"], abs=TOL) == 0.1667

    # Classe 2
    assert pytest.approx(res[1]["Wq"], abs=TOL) == 0.0833
    assert pytest.approx(res[1]["W"], abs=TOL) == 0.1333
    assert pytest.approx(res[1]["Lq"], abs=TOL) == 0.8333
    assert pytest.approx(res[1]["L"], abs=TOL) == 1.3333


# ==============================================================================
# 9. PRIORIDADE PREEMPTIVA
# ==============================================================================

def test_prioridade_preemptive_ferramentaria():
    """
    Lista MG1 - Ex 6 (Preemptivo):
    lambda = [2.0, 4.0, 2.0], mu = 10.0, s = 1.
    Gabarito esperado: W1 = 0.125, W2 = 0.3125, W3 = 1.25.
    """
    res = calcular_prioridade_preemptive(lambdas=[2.0, 4.0, 2.0], mu=10.0, s=1)
    assert res is not None
    assert len(res) == 3
    assert pytest.approx(res[0]["W"], abs=TOL) == 0.1250
    assert pytest.approx(res[1]["W"], abs=TOL) == 0.3125
    assert pytest.approx(res[2]["W"], abs=TOL) == 1.2500


def test_prioridade_preemptive_hospital_municipal():
    """
    Lista MG1 - Ex 7 (Preemptivo, s = 1):
    críticos lambda_1 = 0.1, graves lambda_2 = 0.4, estáveis lambda_3 = 1.5.
    mu = 3.0. s = 1.
    Gabarito esperado para tempo na fila (Wq): Wq1 = 0.011, Wq2 = 0.080, Wq3 = 0.867.
    """
    res = calcular_prioridade_preemptive(lambdas=[0.1, 0.4, 1.5], mu=3.0, s=1)
    assert res is not None
    assert len(res) == 3
    assert pytest.approx(res[0]["Wq"], abs=TOL) == 0.011
    assert pytest.approx(res[1]["Wq"], abs=TOL) == 0.080
    assert pytest.approx(res[2]["Wq"], abs=TOL) == 0.867


def test_probabilidades_exercicios():
    # Exercício 1 (M/M/1 com lambda = 12, mu = 16)
    # 1c: P(N <= 4) = 1 - P(N > 4) = 1 - rho^5 = 1 - 0.75^5 = 0.7627
    p_n_le_4 = 1 - calcular_prob_greater_r_mm1(lamb=12.0, mu=16.0, r=4)
    assert pytest.approx(p_n_le_4, abs=TOL) == 0.7627
    
    # 1g: P(W > 20 dias) = P(W > 2/3 meses) = e^(-16 * (1 - 0.75) * 2/3) = e^(-8/3) = 0.06948
    p_w_gt_20 = calcular_prob_w_greater_t_mm1(lamb=12.0, mu=16.0, t=20.0/30.0)
    assert pytest.approx(p_w_gt_20, abs=TOL) == 0.069
    
    # 1h: P(Wq > 15 dias) = P(Wq > 0.5 meses) = 0.75 * e^(-2) = 0.1015
    p_wq_gt_15 = calcular_prob_wq_greater_t_mm1(lamb=12.0, mu=16.0, t=0.5)
    assert pytest.approx(p_wq_gt_15, abs=TOL) == 0.1015

    # Exercício 2 (M/M/1 com lambda = 12.8, mu = 16.0)
    # 2e: P(W > 30 min) = P(W > 0.5 h) = e^(-1.6) = 0.2019
    p_w_gt_30 = calcular_prob_w_greater_t_mm1(lamb=12.8, mu=16.0, t=0.5)
    assert pytest.approx(p_w_gt_30, abs=TOL) == 0.2019

    # 2f: P(Wq > 15 min) = P(Wq > 0.25 h) = 0.8 * e^(-0.8) = 0.3595
    p_wq_gt_15 = calcular_prob_wq_greater_t_mm1(lamb=12.8, mu=16.0, t=0.25)
    assert pytest.approx(p_wq_gt_15, abs=TOL) == 0.3595

    # 2g: Poisson arrivals (x = 10, rate = 12.8, T = 1.0)
    p_arr_10 = calcular_poisson_prob(rate=12.8, T=1.0, x=10)
    assert pytest.approx(p_arr_10, abs=TOL) == 0.0898

    # 2h: Poisson services (y = 12, rate = 16.0, T = 1.0)
    p_serv_12 = calcular_poisson_prob(rate=16.0, T=1.0, x=12)
    assert pytest.approx(p_serv_12, abs=TOL) == 0.066

    # 2i: P(N = 10) = 0.2 * 0.8^10 = 0.0215
    p_n_10 = calcular_prob_n_mm1(lamb=12.8, mu=16.0, n=10)
    assert pytest.approx(p_n_10, abs=TOL) == 0.0215

    # Exercício 3 (M/M/1 com lambda = 8.0, mu = 10.0)
    # 3: P(N < 6) = P(N <= 5) = 1 - rho^6 = 1 - 0.8^6 = 0.7378
    p_n_lt_6 = 1 - calcular_prob_greater_r_mm1(lamb=8.0, mu=10.0, r=5)
    assert pytest.approx(p_n_lt_6, abs=TOL) == 0.7378

    # Exercício 5 (M/M/1 com lambda = 3.0, mu = 4.0)
    # 5e: P(N = 6) = 0.25 * 0.75^6 = 0.0445
    p_n_6 = calcular_prob_n_mm1(lamb=3.0, mu=4.0, n=6)
    assert pytest.approx(p_n_6, abs=TOL) == 0.0445
    
    # 5g: P(W > 2) = e^(-2) = 0.1353
    p_w_gt_2 = calcular_prob_w_greater_t_mm1(lamb=3.0, mu=4.0, t=2.0)
    assert pytest.approx(p_w_gt_2, abs=TOL) == 0.1353
    
    # 5h: P(Wq > 1.5) = 0.75 * e^(-1.5) = 0.1673
    p_wq_gt_1_5 = calcular_prob_wq_greater_t_mm1(lamb=3.0, mu=4.0, t=1.5)
    assert pytest.approx(p_wq_gt_1_5, abs=TOL) == 0.1673

    # Exercício 7 (M/M/s com s = 2, lambda = 2.0, mu = 3.0)
    # 7h: P(Wq > 0.5) (s=2) = 0.023
    p_wq_gt_0_5_s2 = calcular_prob_wq_greater_t_mms(lamb=2.0, mu=3.0, s=2, t=0.5)
    assert pytest.approx(p_wq_gt_0_5_s2, abs=TOL) == 0.023
    
    # 7i: P(W > 1.0) (s=2) = 0.0655
    p_w_gt_1_s2 = calcular_prob_w_greater_t_mms(lamb=2.0, mu=3.0, s=2, t=1.0)
    assert pytest.approx(p_w_gt_1_s2, abs=TOL) == 0.0655
