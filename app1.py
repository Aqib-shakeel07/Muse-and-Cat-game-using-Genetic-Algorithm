import pygame
import sys
import random
import pandas as pd
import matplotlib.pyplot as plt

# Initialize Pygame
pygame.init()

# Screen and grid settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
GRID_SIZE = 10
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
ORANGE = (250, 156, 28)
YELLOW = (255, 255, 0)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cat and Mouse Split-Screen Game")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 36)

# Load sounds
pygame.mixer.music.load("tracks/background_music_2.mp3")
game_music = "tracks/background_music_1.mp3"
enemy_defeat_sound = pygame.mixer.Sound("tracks/mouse_hit5.mp3")
win_sound = pygame.mixer.Sound("tracks/win_sound.mp3")
lose_sound = pygame.mixer.Sound("tracks/lose_sound.mp3")

LOSE_DELAY = 500  # 0.5 seconds

# Play main menu music
pygame.mixer.music.play(-1)

# Initialize logging DataFrame
log_data = pd.DataFrame(columns=['Generation', 'AI_Kills', 'Player_Kills', 'Average_AI_Health'])

# Helper function to append non-empty rows to DataFrame
def append_log_data(dataframe, new_data):
    new_data_df = pd.DataFrame(new_data)
    if not new_data_df.dropna(how='all').empty:
        return pd.concat([dataframe, new_data_df], ignore_index=True)
    return dataframe

def draw_grid(offset=0):
    """Draws the grid lines on the screen."""
    for x in range(offset, SCREEN_WIDTH // 2 + offset, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (offset, y), (SCREEN_WIDTH // 2 + offset, y))

def draw_wall():
    """Draws the dividing wall between the two halves of the screen."""
    pygame.draw.rect(screen, YELLOW, (SCREEN_WIDTH // 2 - 2, 0, 4, SCREEN_HEIGHT))

class Mouse:
    def __init__(self, offset=0, use_image=False):
        self.x = random.randint(0, SCREEN_WIDTH // GRID_SIZE // 2 - 1) * GRID_SIZE + offset
        self.y = random.randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE
        self.speed = 2
        self.health = 100
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.offset = offset
        self.use_image = use_image
        if self.use_image:
            self.image = pygame.image.load("images/mouse_image.png")  # Load your mouse image here
            self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))

    def move(self):
        """Moves the mouse randomly within the grid."""
        if self.direction == "UP":
            self.y -= self.speed
        elif self.direction == "DOWN":
            self.y += self.speed
        elif self.direction == "LEFT":
            self.x -= self.speed
        elif self.direction == "RIGHT":
            self.x += self.speed

        # Randomly change direction
        if random.randint(0, 50) == 0:
            self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

        # Keep mouse within grid bounds
        if self.x < self.offset:
            self.x = self.offset
            self.direction = "RIGHT"
        elif self.x >= self.offset + (SCREEN_WIDTH // 2) - GRID_SIZE:
            self.x = self.offset + (SCREEN_WIDTH // 2) - GRID_SIZE
            self.direction = "LEFT"

        if self.y < 0:
            self.y = 0
            self.direction = "DOWN"
        elif self.y >= SCREEN_HEIGHT - GRID_SIZE:
            self.y = SCREEN_HEIGHT - GRID_SIZE
            self.direction = "UP"

    def draw(self):
        """Draws the mouse and its health bar."""
        if self.use_image:
            screen.blit(self.image, (self.x, self.y))  # Draw the mouse image
        else:
            pygame.draw.rect(screen, GRAY, (self.x, self.y, GRID_SIZE, GRID_SIZE))  # Draw the gray box

        # Draw health bar
        pygame.draw.rect(screen, RED, (self.x, self.y - 5, GRID_SIZE * (self.health / 100), 5))

    def take_damage(self, damage):
        """Reduces the mouse's health."""
        self.health -= damage


class Mousetrap:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = GRID_SIZE * 3  # Effective range of the trap
        self.damage = 5  # Incremental damage per attack
        self.cooldown = 40  # Time (in frames) between attacks
        self.timer = 0  # Timer to handle cooldowns

    def attack(self, mice):
        """Attacks mice within range incrementally."""
        if self.timer == 0:  # If trap is ready to attack
            for mouse in mice:
                # Calculate Euclidean distance to the mouse
                distance = ((self.x - mouse.x) ** 2 + (self.y - mouse.y) ** 2) ** 0.5
                if distance <= self.range:  # If mouse is in range
                    mouse.take_damage(self.damage)  # Apply incremental damage
                    pygame.mixer.Sound.play(enemy_defeat_sound)  # Play attack sound
                    self.timer = self.cooldown  # Reset cooldown timer
                    break  # Stop attacking other mice this frame

        # Decrease timer if not ready yet
        if self.timer > 0:
            self.timer -= 1

    def draw(self, offset=0):
        """Draws the mousetrap."""
        pygame.draw.circle(screen, ORANGE, (self.x + offset, self.y), GRID_SIZE // 2)


class GeneticAlgorithm:
    def __init__(self, population_size, mutation_rate):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = []

    def initialize_population(self):
        """Creates the initial population of mousetrap placements."""
        for _ in range(self.population_size):
            mousetraps = [
                (random.randint(0, SCREEN_WIDTH // GRID_SIZE // 2 - 1) * GRID_SIZE + SCREEN_WIDTH // 2 + GRID_SIZE // 2,
                 random.randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE + GRID_SIZE // 2)
                for _ in range(random.randint(5, 10))
            ]
            self.population.append(mousetraps)


def win(winner, n):
    pygame.mixer.music.stop()
    if winner == "AI":
        pygame.time.delay(LOSE_DELAY)
        pygame.mixer.Sound.play(lose_sound)
    else:
        pygame.time.delay(LOSE_DELAY)
        pygame.mixer.Sound.play(win_sound)

    font_large = pygame.font.Font(None, 72)
    font_small = pygame.font.Font(None, 36)

    while True:
        screen.fill(BLACK)
        win_text = font_large.render(f"{winner} Wins!", True, WHITE)
        kills_text = font_small.render(f"Total Kills: {n}", True, WHITE)
        restart_text = font_small.render("Press ENTER to Restart or ESC to Quit", True, WHITE)

        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(kills_text, (SCREEN_WIDTH // 2 - kills_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()
                if event.key == pygame.K_ESCAPE:
                    main_menu()


def visualize_performance():
    """Visualizes the logged performance data."""
    global log_data
    plt.figure(figsize=(10, 6))
    plt.plot(log_data['Generation'], log_data['AI_Kills'], label='AI Kills', color='red')
    plt.plot(log_data['Generation'], log_data['Player_Kills'], label='Player Kills', color='blue')
    plt.plot(log_data['Generation'], log_data['Average_AI_Health'], label='Avg AI Health', color='green')
    plt.xlabel('Generation')
    plt.ylabel('Metrics')
    plt.title('AI Performance Metrics')
    plt.legend()
    plt.grid()
    plt.show()


def main():
    pygame.mixer.music.load(game_music)
    pygame.mixer.music.play(-1)
    mousetraps_player = []
    n = 5
    mice = [Mouse(use_image=True) for _ in range(n)]  # Player's mice
    mice_ai = [Mouse(offset=SCREEN_WIDTH // 2, use_image=True) for _ in range(n)]  # AI's mice

    ga = GeneticAlgorithm(population_size=n, mutation_rate=0.1)
    ga.initialize_population()
    mousetraps_ai = ga.population[0]

    player_kills = 0
    ai_kills = 0
    generation = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                visualize_performance()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x < SCREEN_WIDTH // 2:
                    grid_x = (mouse_x // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
                    grid_y = (mouse_y // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
                    mousetraps_player.append(Mousetrap(grid_x, grid_y))

        for mouse in mice[:]:
            mouse.move()
            if mouse.health <= 0:
                mice.remove(mouse)
                player_kills += 1
                if player_kills == n:
                    win("Player", n)

        for mouse in mice_ai[:]:
            mouse.move()
            if mouse.health <= 0:
                mice_ai.remove(mouse)
                ai_kills += 1
                if ai_kills == n:
                    win("AI", n)

        avg_health = sum(mouse.health for mouse in mice_ai) / len(mice_ai) if mice_ai else 0
        global log_data
        log_data = append_log_data(log_data, {
            'Generation': [generation],
            'AI_Kills': [ai_kills],
            'Player_Kills': [player_kills],
            'Average_AI_Health': [avg_health]
        })

        generation += 1

        screen.fill(BLACK)
        draw_wall()

        for mousetrap in mousetraps_player:
            mousetrap.draw()
            mousetrap.attack(mice)

        for mousetrap_pos in mousetraps_ai:
            mousetrap = Mousetrap(mousetrap_pos[0], mousetrap_pos[1])
            mousetrap.draw(offset=SCREEN_WIDTH // 2)
            mousetrap.attack(mice_ai)

        for enemy in mice:
            enemy.draw()
        for enemy in mice_ai:
            enemy.draw()

        player_score_text = small_font.render(f"Player's Score: {player_kills}", True, WHITE)
        ai_score_text = small_font.render(f"AI's Score: {ai_kills}", True, WHITE)
        screen.blit(player_score_text, (10, 10))
        screen.blit(ai_score_text, (SCREEN_WIDTH // 2 + 10, 10))

        pygame.display.flip()
        clock.tick(FPS)


def main_menu():
    while True:
        screen.fill(BLACK)
        title_text = font.render("Cat And Mouse Game", True, WHITE)
        start_text = small_font.render("Press ENTER to Start", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()

        pygame.display.flip()


main_menu()
