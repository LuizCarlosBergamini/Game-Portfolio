import pygame
from resources.camera.camera import CameraGroup


class UI():
    def __init__(self):
        self.pixel_font = pygame.font.Font('resources/font/Minecraft.ttf', 24)

        self.question_box = pygame.image.load('UI/chatbox.png').convert_alpha()
        self.question_box_rect = self.question_box.get_rect()
        camera = CameraGroup()
        self.ui_surface = pygame.Surface(
            (1280 * camera.zoom_scale, 720 * camera.zoom_scale), pygame.SRCALPHA)
        self.ui_surface_rect = self.ui_surface.get_rect(
            center=(camera.half_width, camera.half_height))

    def draw_question_box(self):
        # self.ui_surface.fill((255, 0, 0, 128))  # Fill with transparent red
        question_box_pos = (1790, 633)
        self.ui_surface.blit(self.question_box, (question_box_pos))
        # draw font
        text = self.pixel_font.render('?', True, (255, 255, 255))
        text_rect = text.get_rect(center=(question_box_pos[0] + (
            self.question_box_rect.width / 2), question_box_pos[1] + (self.question_box_rect.height / 2)))
        self.ui_surface.blit(
            text, text_rect)
