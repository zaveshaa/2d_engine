import pygame
import sys

# Инициализация Pygame
pygame.init()

# Установка размера окна и размера ячейки
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 640
CELL_SIZE = 16
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Загрузка текстур
wall_texture = pygame.image.load('wall.png')
ground_texture = pygame.image.load('grass.png')
water_texture = pygame.image.load('water.png')  
sand_texture = pygame.image.load('sand.png')  
player_texture = pygame.Surface((CELL_SIZE, CELL_SIZE))
player_texture.fill(RED)  

# Функция для отрисовки сетки
def draw_grid(surface, width, height, cell_size):
    for x in range(0, width, cell_size):
        pygame.draw.line(surface, BLACK, (x, 0), (x, height))
    for y in range(0, height, cell_size):
        pygame.draw.line(surface, BLACK, (0, y), (width, y))

# Функция для сохранения карты
def save_map(game_map):
    with open('map.txt', 'w') as file:
        for row in game_map:
            file.write(''.join(row) + '\n')

# Функция для отрисовки кнопки сохранения
def draw_save_button(surface):
    pygame.draw.rect(surface, RED, (0, 0, CELL_SIZE * 3, CELL_SIZE))
    font = pygame.font.Font(None, 36)
    text = font.render("Save", True, WHITE)
    text_rect = text.get_rect(center=((CELL_SIZE * 3) // 2, CELL_SIZE // 2))
    surface.blit(text, text_rect)

# Добавляем новое состояние клеток "песок" в игровую карту
def add_sand(game_map, row, col):
    if 0 < row < len(game_map) - 1 and 0 < col < len(game_map[0]) - 1:
        if (game_map[row-1][col] == 'B' or
            game_map[row+1][col] == 'B' or
            game_map[row][col-1] == 'B' or
            game_map[row][col+1] == 'B'):
            game_map[row][col] = 'S'

# Основная функция
def main():
    # Создаем окно
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Map Editor')

    clock = pygame.time.Clock()

    # Инициализация карты
    map_width = WINDOW_WIDTH // CELL_SIZE
    map_height = (WINDOW_HEIGHT - CELL_SIZE) // CELL_SIZE
    game_map = [['.' for _ in range(map_width)] for _ in range(map_height)]

    # Размещаем игрока на карте
    player_col = map_width // 2
    player_row = map_height // 2
    game_map[player_row][player_col] = 'P'

    # Выбранный тип плитки
    selected_tile = 'G'

    # Флаг рисования
    is_drawing = False

    while True:
        WINDOW.fill(WHITE)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_tile = '.'  # Земля
                elif event.key == pygame.K_2:
                    selected_tile = 'W'  # Стена
                elif event.key == pygame.K_3:
                    selected_tile = 'B'  # Вода
                elif event.key == pygame.K_4:
                    selected_tile = 'S'  # Песок
                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    save_map(game_map)
                    print("Карта сохранена!")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if y < CELL_SIZE and x < CELL_SIZE * 3:
                    save_map(game_map)
                    print("Карта сохранена!")
                else:
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE
                    if row < map_height:
                        if event.button == 1:  
                            is_drawing = True
                            game_map[row][col] = selected_tile
                        elif event.button == 3:  
                            is_drawing = True
                            game_map[row][col] = '.'
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in (1, 3): 
                    is_drawing = False
            elif event.type == pygame.MOUSEMOTION and is_drawing:
                x, y = pygame.mouse.get_pos()
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                if row < map_height:
                    if selected_tile == 'P':
                        if game_map[row][col] in ('.', 'S'):
                            game_map[row][col] = selected_tile
                    else:
                        game_map[row][col] = selected_tile
                    if selected_tile == 'S':
                        add_sand(game_map, row, col)

        # Рисуем сетку
        draw_grid(WINDOW, WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE)

        # Отображаем карту
        for y in range(map_height):
            for x in range(map_width):
                if game_map[y][x] == 'W':
                    WINDOW.blit(wall_texture, (x * CELL_SIZE, y * CELL_SIZE))
                elif game_map[y][x] == 'P':
                    WINDOW.blit(player_texture, (x * CELL_SIZE, y * CELL_SIZE))
                elif game_map[y][x] == 'B':
                    WINDOW.blit(water_texture, (x * CELL_SIZE, y * CELL_SIZE))
                elif game_map[y][x] == 'S':
                    WINDOW.blit(sand_texture, (x * CELL_SIZE, y * CELL_SIZE))
                else:
                    WINDOW.blit(ground_texture, (x * CELL_SIZE, y * CELL_SIZE))

        # Отображаем кнопку сохранения
        draw_save_button(WINDOW)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
