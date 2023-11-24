import pygame as pg
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/sky.jpg', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.digit_size = 90
        self.win_image = self.get_texture('resources/textures/win.png', RES)

    def draw_mini_map(self):
        mini_map_size = 200
        mini_map = pg.Surface((mini_map_size, mini_map_size))
        mini_map.set_alpha(200)
        mini_map.fill((0, 0, 0))

        # Dibujar las paredes del minimapa
        for y, row in enumerate(self.game.map.mini_map):
            for x, tile_value in enumerate(row):
                if tile_value:
                    pg.draw.rect(mini_map, 'darkgray', (x * 10, y * 10, 10, 10))

        # Dibujar la posición del jugador
        player_x, player_y = self.game.player.map_pos
        pg.draw.rect(mini_map, 'red', (player_x * 10, player_y * 10, 10, 10))

        # Dibujar el minimapa en la esquina superior izquierda
        self.screen.blit(mini_map, (10, 10))

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_mini_map()
        
    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/3.png'),
            3: self.get_texture('resources/textures/wall1.jpg'),
            4: self.get_texture('resources/textures/wall2.jpg'),
            5: self.get_texture('resources/textures/wall3.jpg'),
        }
