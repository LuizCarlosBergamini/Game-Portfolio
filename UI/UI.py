import pygame
from resources.camera.camera import CameraGroup


class UI():
    def __init__(self, Character):
        self.player = Character
        self.pixel_font = pygame.font.Font('resources/font/Minecraft.ttf', 24)
        self.question_box = pygame.image.load('UI/chatbox.png').convert_alpha()
        self.question_box_rect = self.question_box.get_rect()
        camera = CameraGroup()
        self.ui_surface = pygame.Surface(
            (1280 * camera.zoom_scale, 720 * camera.zoom_scale), pygame.SRCALPHA)
        self.ui_surface_rect = self.ui_surface.get_rect(
            center=(camera.half_width, camera.half_height))

    def add_outline_to_image(image: pygame.Surface, thickness: int, color: tuple, color_key: tuple = (255, 0, 255)) -> pygame.Surface:
        mask = pygame.mask.from_surface(image)
        mask_surf = mask.to_surface(setcolor=color, unsetcolor=color_key)
        mask_surf.set_colorkey(color_key)

        new_img = pygame.Surface(
            (image.get_width() + thickness * 2, image.get_height() + thickness * 2))
        new_img.fill(color_key)
        new_img.set_colorkey(color_key)

        for x in range(-thickness, thickness+1):
            for y in range(-thickness, thickness+1):
                new_img.blit(mask_surf, (x + thickness, y + thickness))
        new_img.blit(image, (thickness, thickness))

        return new_img

    def draw_question_box(self):
        self.ui_surface.fill((0, 0, 0, 0))  # Fill with transparent black
        # self.ui_surface.fill((255, 0, 0, 128))  # Fill with transparent red
        question_box_pos = (1790, 633)
        # draw font
        text = self.pixel_font.render('?', True, (255, 255, 255))
        text_rect = text.get_rect(center=(question_box_pos[0] + (
            self.question_box_rect.width / 2), question_box_pos[1] + (self.question_box_rect.height / 2)))

        if self.player.player_x >= -165 and self.player.player_x <= -81 and self.player.player_y >= -330 and self.player.player_y <= -287:
            self.question_box = pygame.transform.scale(self.question_box, (self.question_box_rect.width * 1.5,
                                                       self.question_box_rect.height * 1.5))

            question_box_pos = (1790 - 12, 633 - 12)

            text = pygame.transform.scale(text, (text_rect.width * 1.5,
                                          text_rect.height * 1.5))

            # instructions text (press E)
            instructions_text = self.pixel_font.render(
                'press E', False, (255, 255, 255)).convert()
            instructions_text_outline = UI.add_outline_to_image(
                instructions_text, 2, (0, 0, 0))
            instructions_text_rect = instructions_text_outline.get_rect(center=(question_box_pos[0] + (
                self.question_box_rect.width / 2) + 15, question_box_pos[1] + (self.question_box_rect.height / 2) - 40))

            self.ui_surface.blit(instructions_text_outline,
                                 instructions_text_rect)

        else:
            self.question_box = pygame.transform.scale(self.question_box, (self.question_box_rect.width,
                                                       self.question_box_rect.height))

            question_box_pos = (1790, 633)

            text = pygame.transform.scale(text, (text_rect.width,
                                          text_rect.height))

        print(self.question_box_rect.width, self.question_box_rect.height)

        self.ui_surface.blit(self.question_box, (question_box_pos))

        self.ui_surface.blit(
            text, text_rect)
