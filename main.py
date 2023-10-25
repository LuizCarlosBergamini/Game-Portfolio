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

    def custom_draw(self):
        for layer_name, layer in scene.load_map().items():
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    self.display_surface.blit(image, (x * scene.tmx_data.tilewidth,
                                                      y * scene.tmx_data.tileheight))
        
        # check that the action is a valid key in the animation dictionary
        screen.blit(char.animation()[action][frame], (char.player_x, char.player_y))

action = 'idle'	
camera_group = CameraGroup()
# scene setup
scene = Scene(camera_group)
# loads the map for posterior drawing
scene.load_map()
# character setup
char = Character(0, 0, camera_group)
char.def_animation_list(2)
# checks if some key is pressed
key_is_pressed = False

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
                char.def_animation_list(3)                
            elif event.key == pygame.K_a:
                action = 'walk'
                key_is_pressed = True
                scene.animation_cooldown = 100
                char.def_animation_list(1)                
            elif event.key == pygame.K_s:
                action = 'walk'
                key_is_pressed = True
                scene.animation_cooldown = 100
                char.def_animation_list(2)                
            elif event.key == pygame.K_d:
                action = 'walk'
                key_is_pressed = True
                scene.animation_cooldown = 100
                char.def_animation_list(0)
                

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                action = 'idle'
                key_is_pressed = False
                scene.animation_cooldown = 300
                char.def_animation_list(3)
            elif event.key == pygame.K_a:
                action = 'idle'
                key_is_pressed = False
                scene.animation_cooldown = 300
                char.def_animation_list(1)
            elif event.key == pygame.K_s:
                action = 'idle'
                key_is_pressed = False
                scene.animation_cooldown = 300
                char.def_animation_list(2)
            elif event.key == pygame.K_d:
                action = 'idle'
                key_is_pressed = False
                scene.animation_cooldown = 300
                char.def_animation_list(0)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # update animation
    frame = scene.handle_animations(char, action)

    # ensures that the frame index is not greater than the number of frames in the animation
    frame %= len(char.animation()[action])

    # RENDER YOUR GAME HERE
    camera_group.custom_draw()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
