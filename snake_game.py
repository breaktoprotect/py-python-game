import pygame
import sys
import numpy
import random

# Pygame setup
pygame.init()
CLK_INTERVAL = 50 # 1/10th of a second
 
# Interface setup
WIN_HEIGHT = 500
WIN_WIDTH = 500
window = pygame.display.set_mode((WIN_HEIGHT, WIN_WIDTH))
VELOCITY = 10 # How much to move per unit

# Initial snake setup
SEGMENT_WIDTH = 10
snake_segments = [(250,250),(250,260),(250,270),(250,280),(250,290)]
facing = 0 # 0 is up, 1 is right, 2 is down, 3 is left

# Main Clocked Loop
started = False
apple_position = (random.randint(0,WIN_HEIGHT/10)*10,random.randint(0,WIN_HEIGHT/10)*10)

while True:
    # Event: Quit program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(1)

    # Event: Movements
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] and facing != 2:
        facing = 0
    if keys[pygame.K_RIGHT] and facing != 3:
        facing = 1
    if keys[pygame.K_DOWN] and facing != 0:
        facing = 2
    if keys[pygame.K_LEFT] and facing != 1:
        facing = 3

    #* Draw & Display
    window.fill((0,0,0)) # Clear screen to color black again
    # Snake
    for segment in snake_segments:
        pygame.draw.rect(window, (25,205,75), (segment[0], segment[1], SEGMENT_WIDTH, SEGMENT_WIDTH))
    # Apple
    pygame.draw.rect(window, (205,25,25), (apple_position[0], apple_position[1], SEGMENT_WIDTH, SEGMENT_WIDTH))
    pygame.display.update()

    #* Advance the Snake
    snake_head = (0,0)
    # Modify head position
    if facing == 0: 
        snake_head = numpy.subtract(snake_segments[0], (0, SEGMENT_WIDTH))
    if facing == 1:
        snake_head = numpy.add(snake_segments[0], (SEGMENT_WIDTH, 0))
    if facing == 2:
        snake_head = numpy.add(snake_segments[0], (0, SEGMENT_WIDTH))
    if facing == 3:
        snake_head = numpy.subtract(snake_segments[0], (SEGMENT_WIDTH, 0))
    
    #* Moving the snake
    # Keep all segments but last - illusion of moving
    leftovers = snake_segments[:len(snake_segments)-1]
    snake_segments = [] #reset
    snake_segments.append(tuple(snake_head))
    for segment in leftovers:
        snake_segments.append(segment)

    #* Collision detection
    # Borders
    if snake_segments[0][0] == WIN_HEIGHT or snake_segments[0][1] == WIN_WIDTH + SEGMENT_WIDTH or \
        snake_segments[0][0] == -SEGMENT_WIDTH or snake_segments[0][1] == -SEGMENT_WIDTH:
        print("[!] Snake crashed to the wall! Exiting...")
        sys.exit(1)

    # Itself
    if numpy.any(tuple(snake_segments[0]) in snake_segments[1:]):
        print("[!] Snake crashed itself! Exiting...")
        sys.exit(1)

    # Apple
    if snake_segments[0] == apple_position:
        print("[+] NOM!")

        #* Growing the snake
        additional_segment = snake_segments[len(snake_segments)-1:]

        if facing == 0: 
            additional_segment = numpy.add(additional_segment, (0, SEGMENT_WIDTH))
        if facing == 1:
            additional_segment = numpy.subtract(additional_segment, (SEGMENT_WIDTH, 0))
        if facing == 2:
            additional_segment = numpy.subtract(additional_segment, (0, SEGMENT_WIDTH))
        if facing == 3:
            additional_segment = numpy.add(additional_segment, (SEGMENT_WIDTH, 0))

        snake_segments.append(tuple(additional_segment[0]))

        #* Respawn Apple at random location
        apple_position = (random.randint(0,WIN_HEIGHT/10)*10,random.randint(0,WIN_HEIGHT/10)*10)

    # Game Speed
    pygame.time.delay(CLK_INTERVAL)