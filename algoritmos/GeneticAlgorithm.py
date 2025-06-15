import pygame
import sys
import random

# Parâmetros do tabuleiro
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

# === Genetic Algorithm ===
def executar_algoritmo_genetico():
    
    def fitness(ind):
        return sum(1 for i in range(NUM_RAINHAS) for j in range(i + 1, NUM_RAINHAS)
                   if abs(ind[i] - ind[j]) == abs(i - j))  # só diagonais

    def crossover(p1, p2):
        point = random.randint(0, NUM_RAINHAS - 1)
        child = p1[:point] + [g for g in p2 if g not in p1[:point]]
        return child

    def mutate(ind):
        i, j = random.sample(range(NUM_RAINHAS), 2)
        ind[i], ind[j] = ind[j], ind[i]

    population = [random.sample(range(NUM_RAINHAS), NUM_RAINHAS) for _ in range(100)]

    for generation in range(1000):
        population.sort(key=fitness)
        if fitness(population[0]) == 0:
            return population[0]
        next_gen = population[:10]  # elitismo
        while len(next_gen) < 100:
            parents = random.sample(population[:50], 2)
            child = crossover(parents[0], parents[1])
            if random.random() < 0.3:
                mutate(child)
            next_gen.append(child)
        population = next_gen
    return population[0]

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
    pygame.display.set_caption("8 Rainhas - Algoritmo Genético")
    font = pygame.font.SysFont(None, 36)

    clock = pygame.time.Clock()
    solucao = executar_algoritmo_genetico()
    botao_rect = desenhar_botao(screen, font)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(event.pos):
                    solucao = executar_algoritmo_genetico()

        screen.fill(BRANCO)
        desenhar_tabuleiro(screen)
        desenhar_rainhas(screen)
        botao_rect = desenhar_botao(screen, font)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
