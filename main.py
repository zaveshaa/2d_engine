import pygame
import sys

# Инициализация Pygame
pygame.init()

# Установка размера окна
CELL_SIZE = 16  # Увеличьте размер ячейки для лучшей видимости
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
    water_texture = pygame.image.load('water.png')
    sand_texture = pygame.image.load('sand.png')  # Новая текстура для песка
    player_image = pygame.image.load('player.png')
    boat_image = pygame.image.load('boat.png')  # Текстура для лодки
    player_image_height = player_image.get_height() // 2  # Уменьшаем высоту изображения игрока в два раза

    # Состояние игрока (обычный или в лодке)
    is_in_boat = False
    boat_movement_cooldown = 0

    clock = pygame.time.Clock()
    while True:
        WINDOW.fill((0, 0, 0))

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if is_in_boat:
                        is_in_boat = False
                    else:
                        if boat_movement_cooldown == 0:
                            is_in_boat = True
                            boat_movement_cooldown = 10 * FPS  # 10 секунд задержки
        if boat_movement_cooldown > 0:
            boat_movement_cooldown -= 1

        # Управление игроком
        if not is_in_boat:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if player_col > 0 and game_map[player_row][player_col - 1] not in ['B', 'W']:
                    player_col -= 1
                    pygame.time.delay(100)  # Задержка 100 миллисекунд
            elif keys[pygame.K_RIGHT]:
                if player_col < grid_width - 1 and game_map[player_row][player_col + 1] not in ['B', 'W']:
                    player_col += 1
                    pygame.time.delay(100)  # Задержка 100 миллисекунд
            elif keys[pygame.K_UP]:
                if player_row > 0 and game_map[player_row - 1][player_col] not in ['B', 'W']:
                    player_row -= 1
                    pygame.time.delay(100)  # Задержка 100 миллисекунд
            elif keys[pygame.K_DOWN]:
                if player_row < grid_height - 1 and game_map[player_row + 1][player_col] not in ['B', 'W']:
                    player_row += 1
                    pygame.time.delay(100)  # Задержка 100 миллисекунд
        else:
            # В состоянии лодки
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if player_col > 0 and game_map[player_row][player_col - 1] == 'B':
                    player_col -= 1
                    pygame.time.delay(100)  # Задержка 100 миллисекунд
            elif keys[pygame.K_RIGHT]:
                if player_col < grid_width - 1 and game_map[player_row][player_col + 1] == 'B':
                    player_col += 1
                    pygame.time.delay(100)  # Задержка 100 миллисекунд
            elif keys[pygame.K_UP]:
                if player_row > 0 and game_map[player_row - 1][player_col] == 'B':
                    player_row -= 1
                    pygame.time.delay(100)  # Задержка 100 миллисекунд
            elif keys[pygame.K_DOWN]:
                if player_row < grid_height - 1 and game_map[player_row + 1][player_col] == 'B':
                    player_row += 1
                    pygame.time.delay(100)  # Задержка 100 миллисекунд

        # Отрисовка
        for y in range(grid_height):
            for x in range(grid_width):
                if game_map[y][x] == 'B':
                    WINDOW.blit(water_texture, (x * CELL_SIZE, y * CELL_SIZE))  # Используем текстуру воды
                elif game_map[y][x] == 'S':
                    WINDOW.blit(sand_texture, (x * CELL_SIZE, y * CELL_SIZE))
                elif game_map[y][x] == 'W':
                    WINDOW.blit(wall_texture, (x * CELL_SIZE, y * CELL_SIZE))  # Используем текстуру стены
                else:
                    WINDOW.blit(ground_texture, (x * CELL_SIZE, y * CELL_SIZE))

        # Отрисовка игрока
        if not is_in_boat:
            WINDOW.blit(player_image, (player_col * CELL_SIZE, player_row * CELL_SIZE))
        else:
            WINDOW.blit(boat_image, (player_col * CELL_SIZE, player_row * CELL_SIZE))  # Отображаем лодку вместо игрока

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
