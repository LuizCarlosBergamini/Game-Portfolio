import pygame
from resources.spritesheet import Spritesheet


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.player_x = x
        self.player_y = y
        self.vel = 1
        self.sheet = Spritesheet()
        self.animation_list = {}
        self.animation_steps = {'idle': 2, 'walk': 6, 'running': 4}
        self.direction_list = {'idle': [0, 2, 4, 6], 'walk': [
            0, 6, 12, 18], 'running': [0, 4, 8, 12]}
        self.step_counter = 0
        self.character_animations = {
            'walk': pygame.image.load(
                'resources\character\walking_spredsheet.png').convert_alpha(),
            'idle': pygame.image.load(
                'resources/character/idle_spredsheet front.png').convert_alpha(),
            'running': pygame.image.load(
                'resources/character/running_spredsheet.png').convert_alpha(),
        }

    def sprite(self, animation_type):
        character_sprite = {}
        character_sprite[animation_type] = self.character_animations[animation_type]
        return character_sprite

    def def_animation_list(self, facing_direction):
        for key, value in self.animation_steps.items():
            temp_img_list = []
            for i in range(value):
                temp_img_list.append(self.sheet.get_image(
                    self.sprite(f"{key}")[key],
                    self.step_counter, 32, 32, 1, 'azure4', self.direction_list[key][facing_direction]))
                self.step_counter += 1
            self.step_counter = 0
            self.animation_list[key] = temp_img_list

    def animation(self):
        return self.animation_list

    def move_left(self):
        self.player_x -= self.vel

    def move_right(self):
        self.player_x += self.vel

    def move_up(self):
        self.player_y -= self.vel

    def move_down(self):
        self.player_y += self.vel
