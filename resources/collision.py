import pygame

class CollisionHandler:
    def __init__(self, camera, char):
        self.camera = camera
        self.char = char
        self.char_pos = (char.player_x, char.player_y) - camera.offset
        self.player_rect = pygame.Rect(self.char_pos[0] + 100, self.char_pos[1], 32, 32)
    
    def check_collision(self, rect1, rect2):
        """
        Check if two rectangular objects collide.
        rect1 and rect2 should be pygame.Rect objects.
        Returns True if they collide, False otherwise.
        """
        return rect1.colliderect(rect2)
