import pygame
import sys
import math
import random

# Initialize
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zig-Zag Truck Race with Crowd and Start/Finish")

# Colors
GREEN = (34, 139, 34)
GREY = (105, 105, 105)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
START_FINISH_COLOR = (255, 215, 0)  # Gold
CROWD_COLORS = [(255, 0, 0), (0, 0, 255), (255, 255, 0), (0, 255, 0), (255, 105, 180)]
TRUCK_COLORS = [(200, 0, 0), (0, 100, 255), (0, 200, 100), (255, 165, 0), (180, 0, 180)]  # 5 truck colors

# Clock
clock = pygame.time.Clock()

# Truck size
truck_w, truck_h = 60, 40

# Track width (wider for multiple trucks side-by-side)
TRACK_WIDTH = 100

# Define closed zig-zag track points
track_points = [
    (100, 500),
    (200, 400),
    (300, 500),
    (400, 400),
    (500, 500),
    (600, 400),
    (700, 500),
    (700, 300),
    (600, 200),
    (500, 300),
    (400, 200),
    (300, 300),
    (200, 200),
    (100, 300),
    (100, 500)  # closing the loop
]

# Precompute segments for movement
segments = []
for i in range(len(track_points) - 1):
    start = track_points[i]
    end = track_points[i + 1]
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.hypot(dx, dy)
    segments.append({
        'start': start,
        'end': end,
        'dx': dx,
        'dy': dy,
        'length': length
    })

total_length = sum(seg['length'] for seg in segments)

class Truck:
    def __init__(self, color, start_distance, speed, lane_offset):
        self.color = color
        self.distance = start_distance
        self.speed = speed
        self.lane_offset = lane_offset  # lateral offset for side-by-side lanes

    def move(self):
        self.distance = (self.distance + self.speed) % total_length

    def get_position(self):
        dist = self.distance
        for seg in segments:
            if dist <= seg['length']:
                ratio = dist / seg['length']
                x = seg['start'][0] + seg['dx'] * ratio
                y = seg['start'][1] + seg['dy'] * ratio
                # Perpendicular vector to segment for lateral offset
                length = seg['length']
                if length != 0:
                    perp_x = -seg['dy'] / length
                    perp_y = seg['dx'] / length
                else:
                    perp_x, perp_y = 0, 0
                # Apply lateral offset scaled to half track width (± max)
                x += perp_x * self.lane_offset
                y += perp_y * self.lane_offset
                return x, y
            dist -= seg['length']
        return segments[-1]['end']

def draw_3d_truck(x, y, color):
    body_rect = pygame.Rect(x, y + 10, truck_w, 30)
    pygame.draw.rect(screen, color, body_rect)

    cabin_points = [(x + 40, y + 10), (x + 55, y), (x + 55, y + 20), (x + 40, y + 30)]
    pygame.draw.polygon(screen, (max(color[0]-50,0), max(color[1]-50,0), max(color[2]-50,0)), cabin_points)

    pygame.draw.circle(screen, BLACK, (int(x + 15), int(y + 45)), 12)
    pygame.draw.circle(screen, BLACK, (int(x + 45), int(y + 45)), 12)
    pygame.draw.circle(screen, WHITE, (int(x + 15), int(y + 45)), 6)
    pygame.draw.circle(screen, WHITE, (int(x + 45), int(y + 45)), 6)

def draw_track():
    screen.fill(GREEN)
    for i in range(len(track_points) - 1):
        pygame.draw.line(screen, GREY, track_points[i], track_points[i+1], TRACK_WIDTH)

    pygame.draw.lines(screen, WHITE, False, track_points, 5)

    # Draw Start/Finish line near the first segment start point
    start_line_x = track_points[0][0]
    start_line_y = track_points[0][1]
    pygame.draw.line(screen, START_FINISH_COLOR, 
                     (start_line_x - TRACK_WIDTH//2, start_line_y - 40), 
                     (start_line_x - TRACK_WIDTH//2, start_line_y + 40), 6)

def draw_crowd(frame):
    amplitude = 3
    frequency = 0.2
    # Left and right vertical sides crowd
    for i in range(40):
        y_base = 100 + i * 10
        offset = int(amplitude * math.sin(frequency * (frame + i)))
        pygame.draw.rect(screen, CROWD_COLORS[i % len(CROWD_COLORS)], (50, y_base + offset, 10, 10))
        pygame.draw.rect(screen, CROWD_COLORS[i % len(CROWD_COLORS)], (740, y_base + offset, 10, 10))
    # Top and bottom horizontal sides crowd
    for i in range(60):
        x_base = 100 + i * 10
        offset = int(amplitude * math.sin(frequency * (frame + i)))
        pygame.draw.rect(screen, CROWD_COLORS[i % len(CROWD_COLORS)], (x_base, 50 + offset, 10, 10))
        pygame.draw.rect(screen, CROWD_COLORS[i % len(CROWD_COLORS)], (x_base, 540 + offset, 10, 10))

def main():
    num_trucks = 5
    trucks = []

    # lateral offsets for trucks - spaced side-by-side on track within TRACK_WIDTH
    max_offset = TRACK_WIDTH//2 - 20  # max lateral offset left/right for trucks
    # distribute 5 trucks evenly side-by-side
    lateral_positions = [-max_offset, -max_offset//2, 0, max_offset//2, max_offset]

    # Initialize trucks with different speeds and starting distances staggered to avoid overlap
    start_offset = 15  # spacing between trucks on track distance
    for i in range(num_trucks):
        speed = random.uniform(1.5, 3.5)
        start_dist = (total_length - i * start_offset) % total_length
        lane_offset = lateral_positions[i % len(lateral_positions)]
        trucks.append(Truck(TRUCK_COLORS[i], start_dist, speed, lane_offset))

    frame_count = 0
    running = True

    while running:
        clock.tick(60)
        frame_count += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for truck in trucks:
            truck.move()

        draw_track()
        draw_crowd(frame_count)

        for truck in trucks:
            x, y = truck.get_position()
            draw_3d_truck(x - truck_w//2, y - truck_h//2, truck.color)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
