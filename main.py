import pygame
import pytmx
from resources.map_data.scene import Scene
from resources.character.character import Character, NPC
from resources.camera.camera import CameraGroup
from resources.collision import CollisionHandler
from resources.map_data.buildings import VegetablesMarket
import pygame_gui
from pygame_gui.core import ObjectID
from UI.UI import UI

# pygame setup
pygame.init()
surface_size = (1280, 720)
screen = pygame.display.set_mode(surface_size)
clock = pygame.time.Clock()
running = True


camera_group = CameraGroup()
# scene setup
scene = Scene(camera_group)
# loads the map for posterior drawing
scene.load_map()
# character setup
char = Character(-435, -872, camera_group)
direction = 2
# checks if some key is pressed
key_is_pressed = False
last_key_pressed = None
shift_pressed = False
# setup collision handler
collision_handler = CollisionHandler(camera_group, char)
# NPC setup
npc = NPC(camera_group)
# buildings setup
vegetalMarket = VegetablesMarket(camera_group)
# create a font variable
font = pygame.font.Font('freesansbold.ttf', 16)

collision_handler.collision_map_layer()

collision_handler.collision_rects[0].x += 16
collision_handler.collision_rects[0].y += 16

ui = UI()

scaled_map, scaled_rect = camera_group.scale_map(collision_handler)
scaled_market, scaled_market_rect = camera_group.scale_market(vegetalMarket)


while running:
    time_delta = clock.tick(60)/1000.0
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
                char.vel = 6
                shift_pressed = True

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
                char.vel = 3
                shift_pressed = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == UIButton:
                print('Test button pressed')

    # draw the fps on the screen
    fps = clock.get_fps()
    fps_text = font.render(f"FPS: {fps:.2f}", True, (255, 255, 255))

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("#8fde5d")

    # update the collision box position
    collision_handler.update_player_collision_box()

    # update the direction of character animation
    char.def_animation_list(direction)

    # update animation for player
    frame = scene.handle_player_animations(char, camera_group.action)

    # ensures that the frame index is not greater than the number of frames in the animation
    frame %= len(char.animation()[camera_group.action])

    # update animation for npc
    frame_npc = scene.handle_npc_animations(npc, 'idle')
    print(f"frame_npc: {frame_npc}")

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
    # checks for collision
    # collision_handler.check_collision(shift_pressed, direction)

    # prints the UI
    ui.draw_question_box()

    # RENDER YOUR GAME HERE
    screen.blit(scaled_map, (scaled_rect.x, scaled_rect.y) -
                camera_group.offset)

    # prints the markets
    screen.blit(scaled_market, (scaled_market_rect.x,
                scaled_market_rect.y) - camera_group.offset)

    camera_group.custom_draw(screen, frame, char, fps_text, npc, frame_npc)

    screen.blit(ui.ui_surface, (ui.ui_surface_rect.x,
                ui.ui_surface_rect.y) - camera_group.offset)

    # flip() the display to put your work on screen
    pygame.display.update()

pygame.quit()
