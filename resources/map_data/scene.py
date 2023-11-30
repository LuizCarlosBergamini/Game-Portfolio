import pygame
import pytmx


class Scene(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.group = group
        self.layers = {}
        self.forest_layers = []
        self.tmx_data = pytmx.util_pygame.load_pygame(
            "util/Portfolio Game Map.tmx")

        # Player variables
        self.player_animation_cooldown = 300
        self.player_frame = 0
        self.last_update_player = pygame.time.get_ticks()

        # NPC variables
        self.npc_animation_cooldown = 300
        self.npc_frame = 0
        self.last_update_npc = pygame.time.get_ticks()

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

    def load_forest(self):
        self.forest_layers.append(self.tmx_data.get_layer_by_name(
            'foreground trees'))
        self.forest_layers.append(self.tmx_data.get_layer_by_name(
            'foreground objects'))

        return self.forest_layers

    def handle_player_animations(self, sprite, animation_type):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_player >= self.player_animation_cooldown:
            self.player_frame += 1
            self.last_update_player = current_time
            if self.player_frame >= sprite.animation_steps[animation_type]:
                self.player_frame = 0

        return self.player_frame

    def handle_npc_animations(self, sprite, animation_type):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_npc >= self.npc_animation_cooldown:
            self.npc_frame += 1
            self.last_update_npc = current_time
            # Debug line
            # print(
            #     f"npc_frame: {self.npc_frame}, animation_steps: {sprite.animation_steps[animation_type]}")
            if self.npc_frame >= sprite.animation_steps[animation_type]:
                self.npc_frame = 0

        return self.npc_frame
