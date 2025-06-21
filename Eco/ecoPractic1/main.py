import pygame
import numpy as np

# Определение параметров
CELL_SIZE = 10  # Размер клетки
GRID_SIZE = (80, 60)  # Размер сетки (ширина, высота)
WIDTH, HEIGHT = GRID_SIZE[0] * CELL_SIZE, GRID_SIZE[1] * CELL_SIZE
FPS = 10  # Скорость обновления экрана

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра в жизнь")
clock = pygame.time.Clock()

def generate_grid(size):
    return np.zeros(size, dtype=int)

def draw_grid(surface, grid):
    surface.fill(BLACK)
    for x in range(GRID_SIZE[0]):
        for y in range(GRID_SIZE[1]):
            if grid[x, y] == 1:
                pygame.draw.rect(surface, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def update_grid(grid):
    new_grid = grid.copy()
    for x in range(GRID_SIZE[0]):
        for y in range(GRID_SIZE[1]):
            neighbors = np.sum(grid[max(0, x-1):min(GRID_SIZE[0], x+2), max(0, y-1):min(GRID_SIZE[1], y+2)]) - grid[x, y]
            if grid[x, y] == 1 and (neighbors < 2 or neighbors > 3):
                new_grid[x, y] = 0  # Клетка умирает
            elif grid[x, y] == 0 and neighbors == 3:
                new_grid[x, y] = 1  # Клетка оживает
    return new_grid

grid = generate_grid(GRID_SIZE)
running = True
simulating = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                simulating = not simulating
            elif event.key == pygame.K_r:
                grid = generate_grid(GRID_SIZE)
            elif event.key == pygame.K_c:
                grid = np.random.choice([0, 1], size=GRID_SIZE, p=[0.8, 0.2])
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            grid[x // CELL_SIZE, y // CELL_SIZE] ^= 1  # Инвертируем состояние клетки
    
    if simulating:
        grid = update_grid(grid)
    
    draw_grid(screen, grid)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()