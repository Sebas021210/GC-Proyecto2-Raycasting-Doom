import pygame
import sys

def show_welcome_screen(screen, width, height):
    font_small = pygame.font.Font(None, 45)

    # Carga el logo de DOOM
    doom_logo = pygame.image.load("./resources/logo.jpg") 

    logo_rect = doom_logo.get_rect(center=(width // 2, height // 2 - 50))

    start_text = font_small.render("Single Player", True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(width // 2, height // 2 + 150))  # Ajusta la posición vertical

    quit_text = font_small.render("Quit Game", True, (255, 255, 255))
    quit_rect = quit_text.get_rect(center=(width // 2, height // 2 + 200))  # Ajusta la posición vertical

    screen.fill((0, 0, 0))
    screen.blit(doom_logo, logo_rect)
    screen.blit(start_text, start_rect)
    screen.blit(quit_text, quit_rect)
    pygame.display.flip()  # Actualiza la pantalla

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
