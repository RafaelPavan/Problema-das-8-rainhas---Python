import time
import tracemalloc
import matplotlib.pyplot as plt
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
    global tempo_exec_solucao_unica_sa
    global tempo_exec_solucao_unica_genetico
    global memoria_solucao_valida_sa
    global memoria_solucao_valida_genetico

    print(f"\n== {nome} - Tempo para uma solução válida ==")

    tracemalloc.start()
    inicio = time.time()
    solucao = alg_func()
    fim = time.time()
    uso_mem = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    if nome == 'Simulated Annealing':
        tempo_exec_solucao_unica_sa = fim - inicio
        memoria_solucao_valida_sa = uso_mem / 1024
    tempo_exec_solucao_unica_genetico = fim - inicio
    memoria_solucao_valida_genetico = uso_mem / 1024

    conflitos = calcular_conflitos(solucao)
    print(f"Solução: {solucao}")
    print(f"Conflitos: {conflitos}")
    print(f"Tempo: {fim - inicio:.4f}s")
    print(f"Uso de memória: {uso_mem / 1024:.2f} KB")

def medir_92_solucoes(alg_func, nome):
    global tempo_exec_92_solucoes_genetico
    global tempo_exec_92_solucoes_sa
    global tentativa_92_solucoes_sa
    global tentativa_92_solucoes_genetico
    global memoria_92_solucoes_sa
    global memoria_92_solucoes_genetico

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

    if nome == 'Simulated Annealing':
        tempo_exec_92_solucoes_sa = fim - inicio
        tentativa_92_solucoes_sa = tentativas
        memoria_92_solucoes_sa = uso_mem / 1024
    tempo_exec_92_solucoes_genetico = fim - inicio
    tentativa_92_solucoes_genetico = tentativas
    memoria_92_solucoes_genetico = uso_mem / 1024

    print(f"Soluções únicas válidas encontradas: {len(unicas)}")
    print(f"Tentativas: {tentativas}")
    print(f"Tempo total: {fim - inicio:.2f}s")
    print(f"Uso de memória: {uso_mem / 1024:.2f} KB")

def main():
    medir_tempo_uma_solucao(simulated_annealing, "Simulated Annealing")
    medir_92_solucoes(simulated_annealing, "Simulated Annealing")

    medir_tempo_uma_solucao(executar_algoritmo_genetico, "Algoritmo Genético")
    medir_92_solucoes(executar_algoritmo_genetico, "Algoritmo Genético")


    tempo_uma_solucao = {
        "Simulated Annealing": tempo_exec_solucao_unica_sa,
        "Algoritmo Genético": tempo_exec_solucao_unica_genetico
    }

    tempo_92_solucoes = {
        "Simulated Annealing": tempo_exec_92_solucoes_sa,
        "Algoritmo Genético": tempo_exec_92_solucoes_genetico
    }

    tentativas_92 = {
        "Simulated Annealing": tentativa_92_solucoes_sa,
        "Algoritmo Genético": tentativa_92_solucoes_genetico
    }

    memoria_solucao_valida = {
        "Simulated Annealing": memoria_solucao_valida_sa,
        "Algoritmo Genético": memoria_solucao_valida_genetico
    }

    memoria_92_solucoes = {
        "Simulated Annealing": memoria_92_solucoes_sa,
        "Algoritmo Genético": memoria_92_solucoes_genetico
    }


    fig, axs = plt.subplots(3, 2, figsize=(14, 12)) 
    axs = axs.flatten()  

    # Gráfico 1 - tempo para uma solução
    axs[0].bar(tempo_uma_solucao.keys(), tempo_uma_solucao.values(), color=['green', 'blue'])
    axs[0].set_title("Tempo para Encontrar Uma Solução Válida")
    axs[0].set_ylabel("Tempo (s)")
    axs[0].grid(axis='y')

    # Gráfico 2 - tempo para 92 soluções
    axs[1].bar(tempo_92_solucoes.keys(), tempo_92_solucoes.values(), color=['green', 'blue'])
    axs[1].set_title("Tempo Total para Encontrar 92 Soluções Únicas")
    axs[1].set_ylabel("Tempo (s)")
    axs[1].grid(axis='y')

    # Gráfico 3 - tentativas para 92 soluções
    axs[2].bar(tentativas_92.keys(), tentativas_92.values(), color=['green', 'blue'])
    axs[2].set_title("Tentativas até Encontrar 92 Soluções Únicas")
    axs[2].set_ylabel("Número de Tentativas")
    axs[2].grid(axis='y')

    # Gráfico 4 - memória para uma solução
    axs[3].bar(memoria_solucao_valida.keys(), memoria_solucao_valida.values(), color=['green', 'blue'])
    axs[3].set_title("Uso de Memória para Uma Solução Válida")
    axs[3].set_ylabel("Memória (KB)")
    axs[3].grid(axis='y')

    # Gráfico 5 - memória para 92 soluções
    axs[4].bar(memoria_92_solucoes.keys(), memoria_92_solucoes.values(), color=['green', 'blue'])
    axs[4].set_title("Uso de Memória para 92 Soluções Únicas")
    axs[4].set_ylabel("Memória (KB)")
    axs[4].grid(axis='y')

    fig.delaxes(axs[5])

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()