import pygame
import sys
import random
import math

# Configurações
TAM_CELULA = 60
NUM_RAINHAS = 8
LARGURA = TAM_CELULA * NUM_RAINHAS
ALTURA = TAM_CELULA * NUM_RAINHAS + 50

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

solucao = []

# ======= Simulated Annealing =======

def gerar_solucao_inicial():
    return list(range(NUM_RAINHAS))

def calcular_conflitos(solucao):
    conflitos = 0
    for i in range(NUM_RAINHAS):
        for j in range(i + 1, NUM_RAINHAS):
            if abs(solucao[i] - solucao[j]) == abs(i - j):
                conflitos += 1
    return conflitos

def gerar_vizinho(solucao):
    vizinho = solucao[:]
    i, j = random.sample(range(NUM_RAINHAS), 2)
    vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
    return vizinho

def simulated_annealing():
    temperatura = 100.0
    resfriamento = 0.99
    min_temp = 1e-3
    max_iter = 10000

    estado_atual = gerar_solucao_inicial()
    random.shuffle(estado_atual)
    custo_atual = calcular_conflitos(estado_atual)

    for _ in range(max_iter):
        if custo_atual == 0:
            break

        novo_estado = gerar_vizinho(estado_atual)
        novo_custo = calcular_conflitos(novo_estado)
        delta = novo_custo - custo_atual

        if delta < 0 or random.random() < math.exp(-delta / temperatura):
            estado_atual = novo_estado
            custo_atual = novo_custo

        temperatura *= resfriamento
        if temperatura < min_temp:
            break

    return estado_atual

# === Interface Gráfica ===

def desenhar_tabuleiro(screen):
    for linha in range(NUM_RAINHAS):
        for coluna in range(NUM_RAINHAS):
            cor = BRANCO if (linha + coluna) % 2 == 0 else PRETO
            rect = pygame.Rect(coluna * TAM_CELULA, linha * TAM_CELULA, TAM_CELULA, TAM_CELULA)
            pygame.draw.rect(screen, cor, rect)

def desenhar_rainhas(screen):
    for coluna, linha in enumerate(solucao):
        center_x = coluna * TAM_CELULA + TAM_CELULA // 2
        center_y = linha * TAM_CELULA + TAM_CELULA // 2
        radius = TAM_CELULA // 3
        pygame.draw.circle(screen, VERMELHO, (center_x, center_y), radius)

def desenhar_botao(screen, font):
    botao_largura = 250
    botao_altura = 40
    botao_x = 10
    botao_y = ALTURA - 50
    botao_rect = pygame.Rect(botao_x, botao_y, botao_largura, botao_altura)
    pygame.draw.rect(screen, AZUL, botao_rect)
    texto = font.render("Gerar Nova Solução", True, BRANCO)
    texto_rect = texto.get_rect(center=botao_rect.center)
    screen.blit(texto, texto_rect)
    return botao_rect

def main():
    global solucao
    pygame.init()
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("8 Rainhas - Simulated Annealing")
    font = pygame.font.SysFont(None, 36)

    clock = pygame.time.Clock()
    solucao = simulated_annealing()
    botao_rect = desenhar_botao(screen, font)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(event.pos):
                    solucao = simulated_annealing()

        screen.fill(BRANCO)
        desenhar_tabuleiro(screen)
        desenhar_rainhas(screen)
        botao_rect = desenhar_botao(screen, font)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
