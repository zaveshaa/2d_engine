import pygame
import sys

# Initialize Pygame
pygame.init()

# Set window size and cell size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 640
CELL_SIZE = 32
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Textures
wall_texture = pygame.image.load('wall.png')
ground_texture = pygame.image.load('grass.png')
player_texture = pygame.Surface((CELL_SIZE, CELL_SIZE))
player_texture.fill(RED)  # Red color for the player

# Function to draw grid
def draw_grid(surface, width, height, cell_size):
    for x in range(0, width, cell_size):
        pygame.draw.line(surface, BLACK, (x, 0), (x, height))
    for y in range(0, height, cell_size):
        pygame.draw.line(surface, BLACK, (0, y), (width, y))

# Function to save map
def save_map(game_map):
    with open('map.txt', 'w') as file:
        for row in game_map:
            file.write(''.join(row) + '\n')

# Function to draw save button
def draw_save_button(surface):
    pygame.draw.rect(surface, RED, (0, 0, CELL_SIZE * 3, CELL_SIZE))
    font = pygame.font.Font(None, 36)
    text = font.render("Save", True, WHITE)
    text_rect = text.get_rect(center=((CELL_SIZE * 3) // 2, CELL_SIZE // 2))
    surface.blit(text, text_rect)

# Main function
def main():
    # Create window
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Map Editor')

    clock = pygame.time.Clock()

    # Initialize map
    map_width = WINDOW_WIDTH // CELL_SIZE
    map_height = (WINDOW_HEIGHT - CELL_SIZE) // CELL_SIZE
    game_map = [['.' for _ in range(map_width)] for _ in range(map_height)]

    # Place player on the map
    player_col = map_width // 2
    player_row = map_height // 2
    game_map[player_row][player_col] = 'P'

    # Selected tile type
    selected_tile = 'G'

    # Drawing flag
    is_drawing = False

    while True:
        WINDOW.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_tile = '.'  # Ground
                elif event.key == pygame.K_2:
                    selected_tile = 'W'  # Wall
                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    save_map(game_map)
                    print("Map saved!")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if y < CELL_SIZE and x < CELL_SIZE * 3:
                    save_map(game_map)
                    print("Map saved!")
                else:
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE
                    if row < map_height:
                        if event.button == 1:  # Left mouse button
                            is_drawing = True
                            game_map[row][col] = selected_tile
                        elif event.button == 3:  # Right mouse button
                            is_drawing = True
                            game_map[row][col] = '.'

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in (1, 3):  # Left or right mouse button
                    is_drawing = False

            elif event.type == pygame.MOUSEMOTION and is_drawing:
                x, y = pygame.mouse.get_pos()
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                if row < map_height:
                    if selected_tile == 'P':
                        # Prevent overwriting the player
                        if game_map[row][col] != 'P':
                            game_map[row][col] = selected_tile
                    else:
                        game_map[row][col] = selected_tile

        # Draw grid
        draw_grid(WINDOW, WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE)

        # Render map
        for y in range(map_height):
            for x in range(map_width):
                if game_map[y][x] == 'W':
                    WINDOW.blit(wall_texture, (x * CELL_SIZE, y * CELL_SIZE))
                elif game_map[y][x] == 'P':
                    WINDOW.blit(player_texture, (x * CELL_SIZE, y * CELL_SIZE))
                else:
                    WINDOW.blit(ground_texture, (x * CELL_SIZE, y * CELL_SIZE))

        # Render icons
        draw_save_button(WINDOW)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
