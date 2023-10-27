import pygame
import pytmx
from resources.map_data.scene import Scene
from resources.character.character import Character

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # camera offset
        self.offset = pygame.math.Vector2(0, 0)
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2

        # zoom
        self.zoom_scale = 3
        self.internal_surface_size = (1280, 720)
        self.internal_surface = pygame.Surface(self.internal_surface_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surface.get_rect(center = (self.half_width, self.half_height))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surface_size)

    def center_target_camera(self, target):
        self.offset.x = target.player_x - self.half_width + 15
        self.offset.y = target.player_y - self.half_height + 20

    def custom_draw(self, mask_image):
        # setup the game camera
        self.internal_surface.fill('#8fde5d')
        self.center_target_camera(char)

        for layer_name, layer in scene.load_map().items():
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    self.internal_surface.blit(image, ((x * scene.tmx_data.tilewidth,
                                                      y * scene.tmx_data.tileheight) - self.offset))
                    
        # check that the action is a valid key in the animation dictionary
        self.internal_surface.blit(char.animation()[action][frame], ((char.player_x, char.player_y) - self.offset))

        self.internal_surface.blit(mask_image, (0, 0))

        #scales the game surface
        scaled_surface = pygame.transform.scale(
            self.internal_surface, self.internal_surface_size_vector * self.zoom_scale)
        scaled_rect = scaled_surface.get_rect(center = (self.half_width, self.half_height))
        self.display_surface.blit(scaled_surface, scaled_rect)

action = 'idle'	
camera_group = CameraGroup()
# scene setup
scene = Scene(camera_group)
# loads the map for posterior drawing
scene.load_map()
# character setup
char = Character(360, 38, camera_group)
direction = 2
# checks if some key is pressed
key_is_pressed = False
last_key_pressed = None

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                action = 'walk'
                key_is_pressed = True
                scene.animation_cooldown = 100
                direction = 3
                last_key_pressed = 'w'
            elif event.key == pygame.K_a:
                action = 'walk'
                key_is_pressed = True
                scene.animation_cooldown = 100
                direction = 1
                last_key_pressed = 'a'         
            elif event.key == pygame.K_s:
                action = 'walk'
                key_is_pressed = True
                scene.animation_cooldown = 100
                direction = 2
                last_key_pressed = 's'             
            elif event.key == pygame.K_d:
                action = 'walk'
                key_is_pressed = True
                scene.animation_cooldown = 100
                direction = 0
                last_key_pressed = 'd'
            elif event.key == pygame.K_LSHIFT and key_is_pressed:
                action = 'running'
                scene.animation_cooldown = 100
                char.vel = 6
                

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                action = 'idle'
                key_is_pressed = False
                scene.animation_cooldown = 300
                direction = 3
            elif event.key == pygame.K_a:
                action = 'idle'
                key_is_pressed = False
                scene.animation_cooldown = 300
                direction = 1
            elif event.key == pygame.K_s:
                action = 'idle'
                key_is_pressed = False
                scene.animation_cooldown = 300
                direction = 2
            elif event.key == pygame.K_d:
                action = 'idle'
                key_is_pressed = False
                scene.animation_cooldown = 300
                direction = 0
            elif event.key == pygame.K_LSHIFT:
                action = 'walk'
                scene.animation_cooldown = 100
                char.vel = 3

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("#8fde5d")

    # update the direction of character animation
    char.def_animation_list(direction)

    # update animation
    frame = scene.handle_animations(char, action)

    # handle player masks for collision
    char_rect = char.character_animations[action].get_rect()
    char_mask = pygame.mask.from_surface(char.character_animations[action])
    mask_image = char_mask.to_surface()

    # ensures that the frame index is not greater than the number of frames in the animation
    frame %= len(char.animation()[action])

    # handle character movement
    if key_is_pressed:
        if last_key_pressed == 'w':
            char.move_up()
        elif last_key_pressed == 'a':
            char.move_left()
        elif last_key_pressed == 's':
            char.move_down()
        elif last_key_pressed == 'd':
            char.move_right()

    # RENDER YOUR GAME HERE
    camera_group.custom_draw(mask_image)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
