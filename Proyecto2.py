import pygame
import sys
import math

# Configuración del juego
width, height = 1400, 800
player_pos = [2.5, 2.5]  # Posición inicial del jugador
player_angle = 0  # Ángulo de visión inicial del jugador
FOV = math.pi / 3  # Campo de visión del jugador

# Lee el mapa desde un archivo de texto
def load_map(file_path):
    with open(file_path, 'r') as file:
        game_map = [line.strip() for line in file]
    return game_map

map_file_path = './assets/mapa.txt'
game_map = load_map(map_file_path)

# Configuración de Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

def show_welcome_screen():
    font_small = pygame.font.Font(None, 45)

    # Carga el logo de DOOM
    doom_logo = pygame.image.load("./assets/logo.jpg") 

    logo_rect = doom_logo.get_rect(center=(width // 2, height // 2 - 50))

    start_text = font_small.render("Single Player", True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(width // 2, height // 2 + 150))  # Ajusta la posición vertical

    quit_text = font_small.render("Quit Game", True, (255, 255, 255))
    quit_rect = quit_text.get_rect(center=(width // 2, height // 2 + 200))  # Ajusta la posición vertical

    screen.fill((0, 0, 0))
    screen.blit(doom_logo, logo_rect)
    screen.blit(start_text, start_rect)
    screen.blit(quit_text, quit_rect)
    pygame.display.flip()

    option_selected = 0  # 0 para iniciar, 1 para salir

    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    option_selected = (option_selected - 1) % 2
                elif event.key == pygame.K_DOWN:
                    option_selected = (option_selected + 1) % 2
                elif event.key == pygame.K_RETURN:
                    waiting_for_key = False

        # Resalta la opción seleccionada
        start_text = font_small.render("Single Player", True, (255, 255, 255))
        quit_text = font_small.render("Quit Game", True, (255, 255, 255))
        if option_selected == 0:
            start_text = font_small.render("Single Player", True, (255, 0, 0))
        else:
            quit_text = font_small.render("Quit Game", True, (255, 0, 0))

        screen.fill((0, 0, 0))
        screen.blit(doom_logo, logo_rect)
        screen.blit(start_text, start_rect)
        screen.blit(quit_text, quit_rect)
        pygame.display.flip()

    return option_selected == 0  # Devuelve True si la opción seleccionada es iniciar el juego

def cast_ray(ray_angle, player_pos, player_angle):
    ray_angle += player_angle
    ray_x, ray_y = player_pos

    while True:
        map_x, map_y = int(ray_x), int(ray_y)

        if game_map[map_y][map_x] == "+":
            hit_distance = math.sqrt((ray_x - player_pos[0])**2 + (ray_y - player_pos[1])**2)
            hit_angle = ray_angle - player_angle
            hit_angle %= 2 * math.pi
            return hit_distance, hit_angle

        ray_x += math.cos(ray_angle)
        ray_y += math.sin(ray_angle)

def draw_walls(player_pos, player_angle):
    screen.fill((0, 0, 0))

    for x in range(width):
        ray_angle = (player_angle - FOV/2) + (x / width) * FOV
        distance, angle = cast_ray(ray_angle, player_pos, player_angle)

        # Corrección de distancias para evitar distorsiones
        distance *= math.cos(angle)

        # Calcula la altura de la pared
        wall_height = height / distance

        # Calcula la posición vertical de la parte superior e inferior de la pared
        wall_top = (height - wall_height) / 2
        wall_bottom = wall_top + wall_height

        # Dibuja la pared en la pantalla
        pygame.draw.line(screen, (255, 255, 255), (x, wall_top), (x, wall_bottom))

    pygame.display.flip()

# Pantalla de bienvenida
startGame = show_welcome_screen()

# Bucle principal
if startGame:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_angle -= 0.05
        if keys[pygame.K_RIGHT]:
            player_angle += 0.05
        if keys[pygame.K_UP]:
            player_pos[0] += 0.1 * math.cos(player_angle)
            player_pos[1] += 0.1 * math.sin(player_angle)
        if keys[pygame.K_DOWN]:
            player_pos[0] -= 0.1 * math.cos(player_angle)
            player_pos[1] -= 0.1 * math.sin(player_angle)

        draw_walls(player_pos, player_angle)
        clock.tick(30)
