import pygame
import pytmx
from resources.map_data.scene import Scene
from functools import cache


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        # display setup
        self.display_surface = pygame.display.get_surface()
        self.scene = Scene(self)
        self.action = 'idle'

        # camera offset
        self.offset = pygame.math.Vector2(0, 0)
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2

        # zoom
        self.zoom_scale = 4
        self.surface_size = (1280, 720)
        self.map_surface = pygame.Surface(
            self.surface_size, pygame.SRCALPHA)

        # foreground
        self.foreground_surface = pygame.Surface(
            self.surface_size, pygame.SRCALPHA)
        self.foreground_surface.set_colorkey((0, 0, 0))

        # market surface
        self.market_surface = pygame.Surface(
            self.surface_size, pygame.SRCALPHA)

        # player surface
        self.player_surface = pygame.Surface(
            self.surface_size, pygame.SRCALPHA)
        self.player_surface.set_colorkey((0, 0, 0))

        # npc surface
        self.npc_surface = pygame.Surface(
            self.surface_size, pygame.SRCALPHA)
        self.npc_surface.set_colorkey((0, 0, 0))

        self.rect = self.player_surface.get_rect(
            center=(self.half_width, self.half_height))
        self.surface_size_vector = pygame.math.Vector2(
            self.surface_size)

        self.scaled_player_surface = pygame.Surface(
            self.surface_size_vector * self.zoom_scale)
        self.scaled_player_surface.set_colorkey((0, 0, 0))

    def center_target_camera(self, target):
        self.offset.x = target.player_x - self.half_width + 15
        self.offset.y = target.player_y - self.half_height + 20

    def scale_map(self, map):
        # draw map
        for layer_name, layer in map.items():
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    self.map_surface.blit(image, ((x * self.scene.tmx_data.tilewidth,
                                                   y * self.scene.tmx_data.tileheight)))

        scaled_surface = pygame.transform.scale(
            self.map_surface, self.surface_size_vector * self.zoom_scale)
        scaled_rect = scaled_surface.get_rect(
            center=(self.half_width, self.half_height))

        return scaled_surface, scaled_rect

    def forest_objects(self, forest):
        # draw foreground objects
        for layer in forest:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    self.foreground_surface.blit(image, ((x * self.scene.tmx_data.tilewidth,
                                                          y * self.scene.tmx_data.tileheight)))

        scaled_surface = pygame.transform.scale(
            self.foreground_surface, self.surface_size_vector * self.zoom_scale)
        scaled_rect = scaled_surface.get_rect(
            center=(self.half_width, self.half_height))

        return scaled_surface, scaled_rect

    def scale_market(self, vegetalMarket):
        # Vegetables Market
        for x, y, image in vegetalMarket.get_tile_image().tiles():
            self.market_surface.blit(image, ((x * vegetalMarket.tmx_data.tilewidth,
                                              y * vegetalMarket.tmx_data.tileheight)))

        scaled_surface = pygame.transform.scale(
            self.market_surface, self.surface_size_vector * self.zoom_scale)
        scaled_rect = scaled_surface.get_rect(
            center=(self.half_width, self.half_height))

        return scaled_surface, scaled_rect

    def custom_draw(self, screen, frame, char, fps):

        # print(
        #     f"char.player_x: {char.player_x}, char.player_y: {char.player_y}")
        self.player_surface.fill((0, 0, 0, 0))

        # prints the player in the self.player_surface
        self.player_surface.blit(
            char.animation()[self.action][frame], (char.player_x, char.player_y) - self.offset)

        # ----- foreground objects block -----

        # ----- foreground objects block -----

        # show fps
        screen.blit(fps, (char.player_x - 10,
                    char.player_y - 50) - self.offset)

        pygame.transform.scale(
            self.player_surface, self.surface_size_vector * self.zoom_scale, self.scaled_player_surface)
        scaled_rect = self.scaled_player_surface.get_rect(
            center=(self.half_width, self.half_height))
        screen.blit(self.scaled_player_surface,
                    (scaled_rect.x, scaled_rect.y))
