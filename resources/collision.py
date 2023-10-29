import pygame


class CollisionHandler:
    def __init__(self, camera, char):
        self.camera = camera
        self.char = char
        self.player_rect = pygame.Rect(
            char.player_x, char.player_y, 11, 8)
        self.tmx_data = self.camera.scene.tmx_data
        self.collision_rects = []

    def update_player_collision_box(self):
        self.player_rect.x = self.char.player_x - self.camera.offset.x + 10
        self.player_rect.y = self.char.player_y - self.camera.offset.y + 16

    def collision_map_layer(self):
        collision_layer = self.tmx_data.get_layer_by_name('collision')
        self.collision_rects = []
        for x, y, images in collision_layer.tiles():
            self.collision_rects.append(images.get_rect(topleft=(
                (x * self.camera.scene.tmx_data.tilewidth, y * self.camera.scene.tmx_data.tileheight) - self.camera.offset)))

        return self.collision_rects

    def check_collision(self, shift_pressed, direction):
        print(shift_pressed)
        colliding = False
        collision_tolerance = 10
        for rect in self.collision_map_layer():
            if self.player_rect.colliderect(rect):
                match direction:
                    case 0:
                        if shift_pressed:
                            self.char.player_x -= 4
                        else:
                            self.char.player_x -= 2
                        return
                    case 1:
                        if shift_pressed:
                            self.char.player_x += 4
                        else:
                            self.char.player_x += 2
                        return
                    case 2:
                        if shift_pressed:
                            self.char.player_y -= 4
                        else:
                            self.char.player_y -= 2
                        return
                    case 3:
                        if shift_pressed:
                            self.char.player_y += 4
                        else:
                            self.char.player_y += 2
                        return

                # collision with the left side of the rect
                # if abs(rect.left - self.player_rect.right) < collision_tolerance and not shift_pressed and not colliding:
                #     self.char.player_x -= 2
                #     return
                # elif abs(rect.left - self.player_rect.right) < collision_tolerance and shift_pressed and not colliding:
                #     self.char.player_x -= 4
                #     return
                # # collision with the right side of the rect
                # elif abs(rect.right - self.player_rect.left) < collision_tolerance and not shift_pressed:
                #     self.char.player_x += 2
                #     return
                # elif abs(rect.right - self.player_rect.left) < collision_tolerance and shift_pressed:
                #     self.char.player_x += 4
                #     return
                # # collision with the top of the rect
                # elif abs(rect.top - self.player_rect.bottom) < collision_tolerance and not shift_pressed:
                #     self.char.player_y -= 2
                #     return
                # elif abs(rect.top - self.player_rect.bottom) < collision_tolerance and shift_pressed:
                #     self.char.player_y -= 4
                #     return
                # # collision with the bottom of the rect
                # elif abs(rect.bottom - self.player_rect.top) < collision_tolerance and not shift_pressed:
                #     self.char.player_y += 2
                #     return
                # elif abs(rect.bottom - self.player_rect.top) < collision_tolerance and shift_pressed:
                #     self.char.player_y += 4
                #     return

        return False
