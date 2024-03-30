import pygame
import sys

# Инициализация Pygame
pygame.init()

# Установка размера окна
CELL_SIZE = 32  # Увеличьте размер ячейки для лучшей видимости
FPS = 60

def load_map(filename):
    with open(filename, 'r') as file:
        return [list(line.strip()) for line in file]

def find_player_position(game_map):
    for row_index, row in enumerate(game_map):
        for col_index, cell in enumerate(row):
            if cell == 'P':
                return col_index, row_index
    return None

def main():
    # Загрузка карты из файла
    game_map = load_map('map.txt')

    # Вычисление размеров сетки
    grid_width = len(game_map[0])
    grid_height = len(game_map)
    grid_pixel_width = grid_width * CELL_SIZE
    grid_pixel_height = grid_height * CELL_SIZE

    # Найти позицию игрока
    player_col, player_row = find_player_position(game_map)
    if player_col is None or player_row is None:
        raise ValueError("Player position not found in the map.")

    # Вычисление размера окна на основе размеров сетки
    WINDOW_WIDTH = grid_pixel_width
    WINDOW_HEIGHT = grid_pixel_height

    # Создание окна
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Tile-based Game')

    # Загрузка текстур
    ground_texture = pygame.image.load('grass.png')
    wall_texture = pygame.image.load('wall.png')
    player_texture = pygame.Surface((CELL_SIZE, CELL_SIZE))
    player_texture.fill((255, 0, 0))  # Красный цвет для игрока

    clock = pygame.time.Clock()
    while True:
        WINDOW.fill((0, 0, 0))

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Управление игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if player_col > 0 and game_map[player_row][player_col - 1] != 'W':
                player_col -= 1
        elif keys[pygame.K_RIGHT]:
            if player_col < grid_width - 1 and game_map[player_row][player_col + 1] != 'W':
                player_col += 1
        elif keys[pygame.K_UP]:
            if player_row > 0 and game_map[player_row - 1][player_col] != 'W':
                player_row -= 1
        elif keys[pygame.K_DOWN]:
            if player_row < grid_height - 1 and game_map[player_row + 1][player_col] != 'W':
                player_row += 1

        # Отрисовка
        for y in range(grid_height):
            for x in range(grid_width):
                if game_map[y][x] == 'W':
                    WINDOW.blit(wall_texture, (x * CELL_SIZE, y * CELL_SIZE))
                else:
                    WINDOW.blit(ground_texture, (x * CELL_SIZE, y * CELL_SIZE))

        # Отрисовка игрока
        WINDOW.blit(player_texture, (player_col * CELL_SIZE, player_row * CELL_SIZE))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
