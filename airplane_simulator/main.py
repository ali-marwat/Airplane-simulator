import pygame
import random
from airplane import Airplane
from weather import Weather

# Initialize pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("2D Airplane Simulator")

# Load assets
background_img = pygame.image.load("assets/background_img.png")
background_img = pygame.transform.scale(background_img, (800, 600))
airplane_img = pygame.image.load("assets/plane_img.png")
airplane_img = pygame.transform.scale(airplane_img, (100, 50))
explosion_img = pygame.image.load("assets/explosion.png")
explosion_img = pygame.transform.scale(explosion_img, (100, 100))

# Obstacle images
bird_img = pygame.image.load("assets/bird.png")
bird_img = pygame.transform.scale(bird_img, (50, 50))
building_img = pygame.image.load("assets/building.png")

# Set font for messages
font = pygame.font.Font(None, 74)  # Welcome and crash message font
small_font = pygame.font.Font(None, 36)  # Smaller font for instructions

# Create objects
airplane = Airplane(100, 300)  # Fixed horizontal position
weather = Weather(wind_speed=1)

# Obstacle list
obstacles = []

# Function to create obstacles
def create_obstacle():
    obstacle_type = random.choice(["bird", "building"])
    if obstacle_type == "bird":
        return {
            "type": "bird",
            "x": 800,  # Start just outside the right edge
            "y": random.randint(0, 550),  # Birds can appear anywhere on the screen
            "img": bird_img,
            "speed": random.randint(5, 10)  # Random speed for birds
        }
    elif obstacle_type == "building":
        random_height = random.randint(200, 500)  # Increased height range for buildings
        return {
            "type": "building",
            "x": 800,  # Start at the right edge
            "y": 600 - random_height,  # Position based on height
            "img": pygame.transform.scale(building_img, (100, random_height)),
            "speed": 4  # Speed for buildings
        }

# Function to detect collision
def detect_collision(obj1, airplane):
    obj1_rect = pygame.Rect(obj1["x"], obj1["y"], obj1["img"].get_width(), obj1["img"].get_height())
    airplane_rect = pygame.Rect(airplane.x, airplane.y, airplane_img.get_width(), airplane_img.get_height())
    return obj1_rect.colliderect(airplane_rect)

# Display welcome message
def show_welcome_screen():
    screen.fill((135, 206, 235))  # Sky blue background
    title_text = font.render("Welcome!", True, (255, 255, 255))  # White text
    instruction_text = small_font.render("Press any key to start", True, (255, 255, 255))
    screen.blit(title_text, (250, 200))
    screen.blit(instruction_text, (270, 300))
    pygame.display.flip()

    # Wait for user to press a key
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:  # Start game on key press
                waiting = False

# Main game loop
running = True
clock = pygame.time.Clock()
game_over = False

# Background scrolling variables
bg_x = 0

# Show welcome screen before starting the game
show_welcome_screen()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Scroll the background
        bg_x -= 2  # Move left by 2 pixels per frame
        if bg_x <= -800:  # Reset background when it moves off-screen
            bg_x = 0

        # Update game state
        keys = pygame.key.get_pressed()
        airplane.update(keys)
        weather.apply_effect(airplane)

        # Spawn obstacles occasionally
        if random.randint(1, 60) == 1:  # Approx. 1 obstacle per second
            obstacles.append(create_obstacle())

        # Move obstacles
        for obstacle in obstacles:
            obstacle["x"] -= obstacle["speed"]  # Move left

            # Check for collision
            if detect_collision(obstacle, airplane):
                game_over = True  # Stop the game on collision
                break

        # Remove off-screen obstacles
        obstacles = [ob for ob in obstacles if ob["x"] > -100]

    # Draw everything
    screen.blit(background_img, (bg_x, 0))
    screen.blit(background_img, (bg_x + 800, 0))  # Adjacent background for seamless scrolling
    for obstacle in obstacles:
        screen.blit(obstacle["img"], (obstacle["x"], obstacle["y"]))
    if not game_over:
        screen.blit(airplane_img, (airplane.x, airplane.y))
    else:
        # Display explosion on collision
        screen.blit(explosion_img, (airplane.x, airplane.y))
        # Display "You Crashed!" message
        text = font.render("You Crashed!", True, (255, 0, 0))  # Red text
        screen.blit(text, (250, 250))  # Centered position

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

pygame.quit()