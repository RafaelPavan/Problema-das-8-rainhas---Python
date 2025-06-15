import time
import tracemalloc
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algoritmos.GeneticAlgorithm import executar_algoritmo_genetico
from algoritmos.SimulatedAnnealingAlgorithm import simulated_annealing



def calcular_conflitos(solucao):
    conflitos = 0
    for i in range(len(solucao)):
        for j in range(i + 1, len(solucao)):
            if abs(solucao[i] - solucao[j]) == abs(i - j):
                conflitos += 1
    return conflitos

def medir_tempo_uma_solucao(alg_func, nome):
    print(f"\n== {nome} - Tempo para uma solução válida ==")
    tracemalloc.start()
    inicio = time.time()
    solucao = alg_func()
    fim = time.time()
    uso_mem = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    conflitos = calcular_conflitos(solucao)
    print(f"Solução: {solucao}")
    print(f"Conflitos: {conflitos}")
    print(f"Tempo: {fim - inicio:.4f}s")
    print(f"Uso de memória: {uso_mem / 1024:.2f} KB")

def medir_92_solucoes(alg_func, nome):
    print(f"\n== {nome} - Tempo para 92 soluções únicas ==")
    tracemalloc.start()
    inicio = time.time()

    unicas = set()
    tentativas = 0
    max_tentativas = 100_000

    while len(unicas) < 92 and tentativas < max_tentativas:
        s = alg_func()
        if calcular_conflitos(s) == 0:
            unicas.add(tuple(s))
        tentativas += 1

    fim = time.time()
    uso_mem = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    print(f"Soluções únicas válidas encontradas: {len(unicas)}")
    print(f"Tentativas: {tentativas}")
    print(f"Tempo total: {fim - inicio:.2f}s")
    print(f"Uso de memória: {uso_mem / 1024:.2f} KB")

def main():
    medir_tempo_uma_solucao(simulated_annealing, "Simulated Annealing")
    medir_92_solucoes(simulated_annealing, "Simulated Annealing")

    medir_tempo_uma_solucao(executar_algoritmo_genetico, "Algoritmo Genético")
    medir_92_solucoes(executar_algoritmo_genetico, "Algoritmo Genético")

if __name__ == "__main__":
    main()
