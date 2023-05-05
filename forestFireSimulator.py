import numpy as np
import pygame


EMPTY, TREE, FIRE = 0, 1, 2
GREEN, ORANGE = (0, 255, 0), (255, 165, 0)
WIDTH, HEIGHT = 800, 800
GRID_SIZE = 8
FPS = 30

treeMap = np.array([(x, y) for x in range(-1, 2) for y in range(-1, 2) if not x == y == 0])

def get_random_forest(forest_fraction):
    grid = np.zeros((HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE), dtype=np.int8)
    tree_indices = np.random.choice(grid.size, int(forest_fraction * grid.size), replace=False)
    np.put(grid, tree_indices, TREE)
    return grid

def update_forest(grid, p, f):
    new_grid = np.zeros_like(grid)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == EMPTY and np.random.random() <= p:
                new_grid[i, j] = TREE
            elif grid[i, j] == TREE:
                new_grid[i, j] = TREE
                for di, dj in treeMap:
                    ni, nj = i + di, j + dj
                    if (0 <= ni < grid.shape[0] and 0 <= nj < grid.shape[1]
                            and grid[ni, nj] == FIRE):
                        new_grid[i, j] = FIRE
                        break
                else:
                    if np.random.random() <= f:
                        new_grid[i, j] = FIRE
            else:
                new_grid[i, j] = EMPTY
    return new_grid

def draw_forest(screen, grid):
   
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            color = GREEN if grid[y, x] == TREE else ORANGE if grid[y, x] == FIRE else (0, 0, 0)
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, color, rect)

def run_simulation(forest_fraction, p, f):
    pygame.init()
    pygame.display.set_caption("Forest Fire Simulation")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    grid = get_random_forest(forest_fraction)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        grid = update_forest(grid, p, f)
        draw_forest(screen, grid)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    forest_fraction = 0.2
    #p, f = 0.25, 0.01
    p, f = 0.05, 0.0001
    #p, f = 0.90, 0.1
    run_simulation(forest_fraction, p, f)
