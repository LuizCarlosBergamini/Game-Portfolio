import pygame
import pytmx
from resources.map_data.scene import Scene


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.scene = Scene(self)
        self.action = 'idle'

        # camera offset
        self.offset = pygame.math.Vector2(0, 0)
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2

        # zoom
        self.zoom_scale = 3
        self.internal_surface_size = (1280, 720)
        self.internal_surface = pygame.Surface(
            self.internal_surface_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surface.get_rect(
            center=(self.half_width, self.half_height))
        self.internal_surface_size_vector = pygame.math.Vector2(
            self.internal_surface_size)

    def center_target_camera(self, target):
        self.offset.x = target.player_x - self.half_width + 15
        self.offset.y = target.player_y - self.half_height + 20

    def custom_draw(self, mask_image, frame, char):
        print(self.offset)
        # setup the game camera
        self.internal_surface.fill('#8fde5d')
        self.center_target_camera(char)

        for layer_name, layer in self.scene.load_map().items():
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    self.internal_surface.blit(image, ((x * self.scene.tmx_data.tilewidth,
                                                        y * self.scene.tmx_data.tileheight) - self.offset))

        # check that the action is a valid key in the animation dictionary
        self.internal_surface.blit(char.animation()[self.action][frame], ((
            char.player_x, char.player_y) - self.offset))

        self.internal_surface.blit(mask_image, (0, 0))

        # scales the game surface
        scaled_surface = pygame.transform.scale(
            self.internal_surface, self.internal_surface_size_vector * self.zoom_scale)
        scaled_rect = scaled_surface.get_rect(
            center=(self.half_width, self.half_height))
        self.display_surface.blit(scaled_surface, scaled_rect)
