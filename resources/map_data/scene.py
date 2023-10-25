import pygame
import pytmx


class Scene(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.layers = {}
        self.tmx_data = pytmx.util_pygame.load_pygame(
            "util/Portfolio Game Map.tmx")
        self.animation_cooldown = 300
        self.frame = 0
        self.last_update = pygame.time.get_ticks()

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
