import pygame
import pytmx


class Scene(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.group = group
        self.layers = {}
        self.tmx_data = pytmx.util_pygame.load_pygame(
            "util/Portfolio Game Map.tmx")
        self.animation_cooldown = 300
        self.frame = 0
        self.last_update = pygame.time.get_ticks()

        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2

        self.offset = pygame.math.Vector2(0, 0)

        # zoom
        self.zoom_scale = 3.5
        self.surface_size = (1280, 720)
        self.surface = pygame.Surface(
            self.surface_size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect(
            center=(self.half_width, self.half_height))
        self.surface_size_vector = pygame.math.Vector2(
            self.surface_size)
        
    def center_target_camera(self, target):
        self.offset.x = target.player_x - self.half_width + 15
        self.offset.y = target.player_y - self.half_height + 20

    def load_map(self):
        for layer in self.tmx_data.visible_layers:
            self.layers[layer.name] = self.tmx_data.get_layer_by_name(
                layer.name)

        return self.layers


    def handle_animations(self, sprite, animation_type):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = current_time
            if self.frame >= sprite.animation_steps[animation_type]:
                self.frame = 0

        return self.frame
