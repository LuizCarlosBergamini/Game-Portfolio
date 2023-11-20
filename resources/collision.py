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

    import pygame

    def collision_map_layer(self):
        collision_layer = self.tmx_data.get_layer_by_name('collision')
        self.collision_rects = []
        for x, y, images in collision_layer.tiles():
            map_x = x * (self.camera.scene.tmx_data.tilewidth *
                         self.camera.zoom_scale) - self.camera.offset.x
            map_y = y * (self.camera.scene.tmx_data.tileheight *
                         self.camera.zoom_scale) - self.camera.offset.y
            # Scale the image to be 2 times bigger
            scaled_image = pygame.transform.scale(
                images, (images.get_width() * self.camera.zoom_scale, images.get_height() * self.camera.zoom_scale))
            self.collision_rects.append(
                scaled_image.get_rect(topleft=(
                    map_x - 1920,
                    map_y - 1080)))

        return self.collision_rects

    def check_collision(self, shift_pressed, direction):
        for rect in self.collision_map_layer():
            if self.player_rect.colliderect(rect):
                # print('colide')
                match direction:
                    case 0:
                        if shift_pressed:
                            self.char.player_x -= 6
                        else:
                            self.char.player_x -= 3
                        return
                    case 1:
                        if shift_pressed:
                            self.char.player_x += 6
                        else:
                            self.char.player_x += 3
                        return
                    case 2:
                        if shift_pressed:
                            self.char.player_y -= 6
                        else:
                            self.char.player_y -= 3
                        return
                    case 3:
                        if shift_pressed:
                            self.char.player_y += 6
                        else:
                            self.char.player_y += 3
                        return

        return False
