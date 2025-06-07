import pygame
import sys
import math

# Initialize
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tractor Race with Crowd & Finish Line")

# Colors
GREEN = (34, 139, 34)
GREY = (105, 105, 105)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
CROWD_COLORS = [(255, 0, 0), (0, 0, 255), (255, 255, 0), (0, 255, 0), (255, 105, 180)]

# Clock
clock = pygame.time.Clock()

# Load tractor (optional)
try:
    tractor_img = pygame.image.load("tractor.png")
    tractor_img = pygame.transform.scale(tractor_img, (60, 60))
except:
    print("tractor.png not found. Using red box.")
    tractor_img = None

# Tractor details
tractor_w, tractor_h = 60, 60
tractor_x = 700 - tractor_w
tractor_y = 500 - tractor_h
tractor_speed = 2
current_segment = 0

# Animation frame
frame_count = 0

# === Drawing Functions ===

def draw_track():
    screen.fill(GREEN)
    pygame.draw.rect(screen, GREY, (100, 100, 600, 400))        # road
    pygame.draw.rect(screen, GREEN, (200, 200, 400, 200))       # inner field
    pygame.draw.rect(screen, WHITE, (100, 100, 600, 400), 5)    # outer border
    pygame.draw.rect(screen, WHITE, (200, 200, 400, 200), 5)    # inner border

def draw_tractor(x, y):
    if tractor_img:
        screen.blit(tractor_img, (x, y))
    else:
        pygame.draw.rect(screen, RED, (x, y, tractor_w, tractor_h))

# def draw_finish_line():
#     tile_size = 10
#     rows = 40  # height of track / tile_size (track height=400, 400/10=40)
#     cols = 6   # width of finish line = 6 tiles * 10 = 60 px wide

#     # Finish line vertical strip position:
#     # Place it at the bottom edge of track, at tractor start x (around 700-60)
#     start_x = 700 - cols * tile_size   # finish line start x
#     start_y = 100  # top of track

#     for row in range(rows):
#         for col in range(cols):
#             color = BLACK if (row + col) % 2 == 0 else WHITE
#             pygame.draw.rect(screen, color,
#                              (start_x + col * tile_size, start_y + row * tile_size, tile_size, tile_size))

def draw_crowd_moving(frame):
    amplitude = 3  # pixels up/down
    frequency = 0.2

    for i in range(40):  # left and right columns
        x_left = 70
        x_right = 730
        y_base = 100 + i * 10
        offset = int(amplitude * math.sin(frequency * (frame + i)))

        color = CROWD_COLORS[i % len(CROWD_COLORS)]
        # Left
        pygame.draw.rect(screen, color, (x_left, y_base + offset, 10, 10))
        # Right
        pygame.draw.rect(screen, color, (x_right, y_base + offset, 10, 10))

    for i in range(60):  # top and bottom rows
        x_base = 100 + i * 10
        offset = int(amplitude * math.sin(frequency * (frame + i)))

        color = CROWD_COLORS[i % len(CROWD_COLORS)]
        # Top row
        pygame.draw.rect(screen, color, (x_base, 70 + offset, 10, 10))
        # Bottom row
        pygame.draw.rect(screen, color, (x_base, 530 + offset, 10, 10))

# === Main Loop ===

def main():
    global tractor_x, tractor_y, current_segment, frame_count
    running = True

    while running:
        clock.tick(60)
        frame_count += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Auto movement
        if current_segment == 0:  # right
            tractor_x += tractor_speed
            if tractor_x >= 700 - tractor_w:
                current_segment = 1
        elif current_segment == 1:  # up
            tractor_y -= tractor_speed
            if tractor_y <= 100:
                current_segment = 2
        elif current_segment == 2:  # left
            tractor_x -= tractor_speed
            if tractor_x <= 100:
                current_segment = 3
        elif current_segment == 3:  # down
            tractor_y += tractor_speed
            if tractor_y >= 500 - tractor_h:
                current_segment = 0

        # Drawing sequence
        draw_track()
        draw_crowd_moving(frame_count)
        draw_tractor(tractor_x, tractor_y)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
