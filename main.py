import pygame
import pytmx
from resources.map_data.scene import Scene
from resources.character.character import Character
from resources.camera.camera import CameraGroup

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


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
                camera_group.action = 'walk'
                key_is_pressed = True
                scene.animation_cooldown = 100
                direction = 3
                last_key_pressed = 'w'
            elif event.key == pygame.K_a:
                camera_group.action = 'walk'
                key_is_pressed = True
                scene.animation_cooldown = 100
                direction = 1
                last_key_pressed = 'a'
            elif event.key == pygame.K_s:
                camera_group.action = 'walk'
                key_is_pressed = True
                scene.animation_cooldown = 100
                direction = 2
                last_key_pressed = 's'
            elif event.key == pygame.K_d:
                camera_group.action = 'walk'
                key_is_pressed = True
                scene.animation_cooldown = 100
                direction = 0
                last_key_pressed = 'd'
            elif event.key == pygame.K_LSHIFT and key_is_pressed:
                camera_group.action = 'running'
                scene.animation_cooldown = 100
                char.vel = 2

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                camera_group.action = 'idle'
                key_is_pressed = False
                scene.animation_cooldown = 300
                direction = 3
            elif event.key == pygame.K_a:
                camera_group.action = 'idle'
                key_is_pressed = False
                scene.animation_cooldown = 300
                direction = 1
            elif event.key == pygame.K_s:
                camera_group.action = 'idle'
                key_is_pressed = False
                scene.animation_cooldown = 300
                direction = 2
            elif event.key == pygame.K_d:
                camera_group.action = 'idle'
                key_is_pressed = False
                scene.animation_cooldown = 300
                direction = 0
            elif event.key == pygame.K_LSHIFT:
                camera_group.action = 'walk'
                scene.animation_cooldown = 100
                char.vel = 1

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("#8fde5d")

    # update the direction of character animation
    char.def_animation_list(direction)

    # update animation
    frame = scene.handle_animations(char, camera_group.action)

    # handle player masks for collision
    char_rect = char.character_animations[camera_group.action].get_rect()
    char_mask = pygame.mask.from_surface(
        char.character_animations[camera_group.action])
    mask_image = char_mask.to_surface()

    # ensures that the frame index is not greater than the number of frames in the animation
    frame %= len(char.animation()[camera_group.action])

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
    camera_group.custom_draw(mask_image, frame, char)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
