import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
GAME_SPEED = 500  # Delay between each move (in milliseconds)
FONT_SIZE = 36
FONT_COLOR = (255, 255, 255)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()
font = pygame.font.Font(None, FONT_SIZE)

# Define colors
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Define the shapes of the Tetriminos
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [0, 0, 1]],  # L
    [[1, 1, 1], [1, 0, 0]]  # J
]

SHAPES_COLORS = [
    CYAN, YELLOW, GREEN, RED, PURPLE, BLUE, ORANGE
]


def draw_grid():
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(window, BLACK, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(window, BLACK, (0, y), (WINDOW_WIDTH, y))


def draw_tetrimino(tetrimino, x, y, color):
    for row in range(len(tetrimino)):
        for col in range(len(tetrimino[row])):
            if tetrimino[row][col] == 1:
                pygame.draw.rect(window, color,
                                 (x + col * GRID_SIZE, y + row * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def check_collision(tetrimino, x, y, grid):
    for row in range(len(tetrimino)):
        for col in range(len(tetrimino[row])):
            if tetrimino[row][col] == 1:
                if x + col < 0 or x + col >= GRID_WIDTH or y + row >= GRID_HEIGHT or grid[y + row][x + col]:
                    return True
    return False


def rotate_tetrimino(tetrimino):
    return list(zip(*reversed(tetrimino)))


def clear_rows(grid):
    full_rows = [row for row in range(GRID_HEIGHT) if all(grid[row])]
    for row in full_rows:
        del grid[row]
        grid.insert(0, [0] * GRID_WIDTH)
    return len(full_rows)


def draw_score(score):
    text = font.render("Score: " + str(score), True, FONT_COLOR)
    window.blit(text, (WINDOW_WIDTH - text.get_width() - 10, 10))


def game_over(score):
    game_over_text = font.render("Game Over", True, FONT_COLOR)
    score_text = font.render("Score: " + str(score), True, FONT_COLOR)
    window.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 2 - FONT_SIZE))
    window.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2 + FONT_SIZE))


def main():
    # Create the grid
    grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

    # Initialize the current tetrimino
    tetrimino = random.choice(SHAPES)
    tetrimino_color = random.choice(SHAPES_COLORS)
    tetrimino_x = GRID_WIDTH // 2 - len(tetrimino[0]) // 2
    tetrimino_y = 0

    score = 0

    game_running = True
    game_over_flag = False
    move_delay = 0

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not check_collision(tetrimino, tetrimino_x - 1, tetrimino_y, grid):
                    tetrimino_x -= 1
                elif event.key == pygame.K_RIGHT and not check_collision(tetrimino, tetrimino_x + 1, tetrimino_y, grid):
                    tetrimino_x += 1
                elif event.key == pygame.K_DOWN and not check_collision(tetrimino, tetrimino_x, tetrimino_y + 1, grid):
                    tetrimino_y += 1
                elif event.key == pygame.K_UP:
                    rotated = rotate_tetrimino(tetrimino)
                    if not check_collision(rotated, tetrimino_x, tetrimino_y, grid):
                        tetrimino = rotated

        if not game_over_flag:
            move_delay += clock.get_rawtime()
            if move_delay >= GAME_SPEED:
                move_delay = 0
                if not check_collision(tetrimino, tetrimino_x, tetrimino_y + 1, grid):
                    tetrimino_y += 1
                else:
                    for row in range(len(tetrimino)):
                        for col in range(len(tetrimino[row])):
                            if tetrimino[row][col] == 1:
                                grid[tetrimino_y + row][tetrimino_x + col] = 1

                    rows_cleared = clear_rows(grid)
                    score += rows_cleared

                    tetrimino = random.choice(SHAPES)
                    tetrimino_color = random.choice(SHAPES_COLORS)
                    tetrimino_x = GRID_WIDTH // 2 - len(tetrimino[0]) // 2
                    tetrimino_y = 0

                    if check_collision(tetrimino, tetrimino_x, tetrimino_y, grid):
                        game_over_flag = True

        # Clear the window
        window.fill(BLACK)

        # Draw the grid
        draw_grid()

        # Draw the tetrimino
        draw_tetrimino(tetrimino, tetrimino_x * GRID_SIZE, tetrimino_y * GRID_SIZE, tetrimino_color)

        # Draw the placed tetriminos
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                if grid[row][col] == 1:
                    pygame.draw.rect(window, SHAPES_COLORS[0],
                                     (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Draw the score
        draw_score(score)

        if game_over_flag:
            game_over(score)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()

