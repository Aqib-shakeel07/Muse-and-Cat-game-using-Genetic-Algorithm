import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Screen and grid settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 40  # Each grid cell is 40x40
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Enemy path (list of (x, y) positions in grid coordinates)
ENEMY_PATH = [
    (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5),
    (7, 6), (7, 7), (6, 7), (5, 7), (4, 7), (3, 7), (2, 7), (1, 7), (0, 7),
    (0, 6)  # Loop back to (0, 5)
]

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defense Game")
clock = pygame.time.Clock()

# Initialize the mixer for music and sound
pygame.mixer.init()

# Load sounds
try:
    background_music = pygame.mixer.music.load("GeneticAlgorithm/tracks/background_music_1.mp3")  # Replace with your music file
    pygame.mixer.music.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
    place_tower_sound = pygame.mixer.Sound("GeneticAlgorithm/tracks/place_tower.mp3")  # Replace with your sound effect file
    enemy_hit_sound = pygame.mixer.Sound("GeneticAlgorithm/tracks/enemy_hit2.mp3")  # Replace with your sound effect file
    pygame.mixer.music.play(-1)  # Loop the background music infinitely
except FileNotFoundError:
    print("Error: Music or sound files not found. Ensure the files are in the same directory as this script.")
    background_music = None

# Draw the grid
def draw_grid():
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))

# Enemy class
class Enemy:
    def __init__(self, path):
        self.path = path  # List of waypoints (grid positions)
        self.path_index = 0  # Current waypoint index
        self.x, self.y = self.path[self.path_index]  # Starting position
        self.x *= GRID_SIZE
        self.y *= GRID_SIZE
        self.speed = 2  # Speed of movement (pixels per frame)
        self.health = 100  # Enemy health

    def move(self):
        if self.path_index < len(self.path) - 1:
            next_x, next_y = self.path[self.path_index + 1]
            next_x *= GRID_SIZE
            next_y *= GRID_SIZE

            # Move in the x direction
            if self.x < next_x:
                self.x += self.speed
            elif self.x > next_x:
                self.x -= self.speed

            # Move in the y direction
            if self.y < next_y:
                self.y += self.speed
            elif self.y > next_y:
                self.y -= self.speed

            # Check if the enemy has reached the next waypoint
            if abs(self.x - next_x) < self.speed and abs(self.y - next_y) < self.speed:
                self.path_index += 1

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, GRID_SIZE, GRID_SIZE))
        # Draw health bar
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 5, GRID_SIZE * (self.health / 100), 5))

    def take_damage(self, damage):
        self.health -= damage
        if enemy_hit_sound:
            enemy_hit_sound.play()  # Play sound when enemy is hit

# Tower class
class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = GRID_SIZE * 3  # Attack range
        self.damage = 20  # Damage per attack
        self.cooldown = 30  # Frames between attacks
        self.timer = 0  # Timer to track cooldown

    def attack(self, enemies):
        if self.timer == 0:  # Only attack if cooldown is 0
            for enemy in enemies:
                # Calculate distance to the enemy
                distance = ((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2) ** 0.5
                if distance <= self.range:
                    enemy.take_damage(self.damage)
                    self.timer = self.cooldown
                    break

        # Reduce cooldown timer
        if self.timer > 0:
            self.timer -= 1

    def draw(self):
        pygame.draw.circle(screen, BLUE, (self.x, self.y), GRID_SIZE // 2)

# Main menu
def main_menu():
    while True:
        screen.fill(WHITE)
        font = pygame.font.Font(None, 74)
        title = font.render("Tower Defense Game", True, BLACK)
        start_button = font.render("Start", True, GREEN)
        quit_button = font.render("Quit", True, RED)

        # Draw menu
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        screen.blit(start_button, (SCREEN_WIDTH // 2 - start_button.get_width() // 2, 250))
        screen.blit(quit_button, (SCREEN_WIDTH // 2 - quit_button.get_width() // 2, 350))

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 250 <= mouse_y <= 250 + start_button.get_height():
                    return  # Start the game
                elif 350 <= mouse_y <= 350 + quit_button.get_height():
                    pygame.quit()
                    sys.exit()

# Main game loop
def main():
    towers = []
    enemies = [Enemy(ENEMY_PATH)]  # Add one enemy for now

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Place towers
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x = (mouse_x // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
                grid_y = (mouse_y // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
                towers.append(Tower(grid_x, grid_y))
                if place_tower_sound:
                    place_tower_sound.play()  # Play tower placement sound

        # Update game objects
        for enemy in enemies:
            enemy.move()
            if enemy.health <= 0:
                enemies.remove(enemy)  # Remove dead enemy

        for tower in towers:
            tower.attack(enemies)

        # Draw everything
        screen.fill(WHITE)
        draw_grid()

        for tower in towers:
            tower.draw()

        for enemy in enemies:
            enemy.draw()

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main_menu()  # Show the main menu first
    main()       # Start the game after the menu
