import pygame
from resources.spritesheet import Spritesheet


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.player_x = x
        self.player_y = y
        self.vel = 5
        self.sheet = Spritesheet()
        self.animation_list = {}
        self.animation_steps = {'idle': 2, 'walk': 24}
        self.direction_list = {'idle': [0, 2, 4, 6], 'walk': [0, 6, 12, 18]}
        self.step_counter = 0
        self.character_animations = {
            'walk': pygame.image.load(
                'resources\character\walking_spredsheet.png').convert_alpha(),
            'idle': pygame.image.load(
                'resources/character/idle_spredsheet front.png').convert_alpha(),
        }

    def sprite(self, animation_type):
        character_sprite = {}
        character_sprite[animation_type] = self.character_animations[animation_type]
        print(character_sprite)
        return character_sprite

    def def_animation_list(self, animation_type, facing_direction):
        for key, value in self.animation_steps.items():
            temp_img_list = []
            for i in range(value):
                temp_img_list.append(self.sheet.get_image(
                    self.sprite(f"{key}")[animation_type],
                    self.step_counter, 32, 32, 10, 'azure4', self.direction_list[animation_type][facing_direction]))
                self.step_counter += 1
            self.step_counter = 0
            self.animation_list[animation_type] = temp_img_list

    def animation(self):
        return self.animation_list

    def move_left(self):
        self.x -= self.vel

    def move_right(self):
        self.x += self.vel

    def move_up(self):
        self.y -= self.vel

    def move_down(self):
        self.y += self.vel
