import pygame
import sys

# Инициализация Pygame
pygame.init()

# Установка размера окна
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 16
FPS = 60


ground_texture = pygame.image.load('ground_texture.png')

def main():

    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Передвижение игрока с камерой')

    # Size grid
    grid_width = 100
    grid_height = 100
    grid_pixel_width = grid_width * CELL_SIZE
    grid_pixel_height = grid_height * CELL_SIZE


    player = pygame.Rect(0, 0, CELL_SIZE, CELL_SIZE)
    player_color = (255, 0, 0)

    clock = pygame.time.Clock()
    while True:
        WINDOW.fill((0, 0, 0))

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= 3
        if keys[pygame.K_RIGHT]:
            player.x += 3
        if keys[pygame.K_UP]:
            player.y -= 3
        if keys[pygame.K_DOWN]:
            player.y += 3

        player.x = max(0, min(player.x, grid_pixel_width - CELL_SIZE))
        player.y = max(0, min(player.y, grid_pixel_height - CELL_SIZE))

        camera_width = WINDOW_WIDTH // CELL_SIZE
        camera_height = WINDOW_HEIGHT // CELL_SIZE

        camera_x = max(0, min(player.x - (camera_width // 2) * CELL_SIZE, grid_pixel_width - camera_width * CELL_SIZE))
        camera_y = max(0, min(player.y - (camera_height // 2) * CELL_SIZE, grid_pixel_height - camera_height * CELL_SIZE))

        for y in range(camera_y // CELL_SIZE, (camera_y + WINDOW_HEIGHT) // CELL_SIZE + 1):
            for x in range(camera_x // CELL_SIZE, (camera_x + WINDOW_WIDTH) // CELL_SIZE + 1):
                ground_rect = pygame.Rect(x * CELL_SIZE - camera_x, y * CELL_SIZE - camera_y, CELL_SIZE, CELL_SIZE)
                WINDOW.blit(ground_texture, ground_rect)

        player_relative_to_camera = pygame.Rect(player.x - camera_x, player.y - camera_y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(WINDOW, player_color, player_relative_to_camera)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
