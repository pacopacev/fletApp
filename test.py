import pygame
import random
import time

# Initialize pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 200
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Music Visualizer")

# Define the colors
bg_color = (0, 0, 0)
bar_color = (255, 0, 0)

# Define the bar positions
bar_width = 50
bar_spacing = 10
bar_count = 5
bar_positions = [(x * (bar_width + bar_spacing)) + (bar_width / 2) - (bar_width / 2) for x in range(bar_count)]

# Create the bars
bars = [pygame.Rect(x, 0, bar_width, 0) for x in bar_positions]

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(bg_color)

    # Update the bar positions randomly
    for i in range(bar_count):
        bar_height = random.randint(0, screen_height)
        bars[i].y = screen_height - bar_height
        bars[i].height = bar_height

    # Draw the bars
    for i in range(bar_count):
        pygame.draw.rect(screen, bar_color, bars[i])

    # Update the display
    pygame.display.flip()

    # Delay to control the animation speed
    time.sleep(0.1)

# Quit the game
pygame.quit()