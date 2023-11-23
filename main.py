import pygame as pg
import sys
from map import *
from player import *
from raycasting import *
from object_renderer import *

def show_welcome_screen(screen, width, height):
    font_small = pg.font.Font(None, 45)

    # Carga el logo de DOOM
    doom_logo = pg.image.load("./resources/logo.jpg") 

    logo_rect = doom_logo.get_rect(center=(width // 2, height // 2 - 50))

    start_text = font_small.render("Single Player", True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(width // 2, height // 2 + 150))  # Ajusta la posición vertical

    quit_text = font_small.render("Quit Game", True, (255, 255, 255))
    quit_rect = quit_text.get_rect(center=(width // 2, height // 2 + 200))  # Ajusta la posición vertical

    screen.fill((0, 0, 0))
    screen.blit(doom_logo, logo_rect)
    screen.blit(start_text, start_rect)
    screen.blit(quit_text, quit_rect)
    pg.display.flip()  # Actualiza la pantalla

    option_selected = 0  # 0 para iniciar, 1 para salir

    waiting_for_key = True
    while waiting_for_key:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    option_selected = (option_selected - 1) % 2
                elif event.key == pg.K_DOWN:
                    option_selected = (option_selected + 1) % 2
                elif event.key == pg.K_RETURN:
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
        pg.display.flip()

    return option_selected == 0  # Devuelve True si la opción seleccionada es iniciar el juego

class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'resources/sound/'
        self.theme = pg.mixer.music.load(self.path + 'theme.mp3')
        pg.mixer.music.set_volume(0.3)

class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.sound = Sound(self)
        pg.mixer.music.play(-1)

    def update(self):
        self.player.update()
        self.raycasting.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.object_renderer.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True

    def run(self):
        if show_welcome_screen(self.screen, WIDTH, HEIGHT):  # Llama a la pantalla de bienvenida
            self.new_game()
            while True:
                self.check_events()
                self.update()
                self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()
