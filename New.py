import pygame
import random

# Initialize pygame
pygame.init()
# Game Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 100
PIPE_GAP = 150
GRAVITY = 0.5
FLAP_STRENGTH = -7

# Setup game display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load Images
background_image = pygame.image.load('background.png')  # Load background image
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale to fit screen
bird_image = pygame.image.load('bird.png')  # Load bird image
bird_image = pygame.transform.scale(bird_image, (40, 30))  # Resize bird image to fit
pipe_image = pygame.image.load('pipe.png')  # Load pipe image
pipe_image = pygame.transform.scale(pipe_image, (60, 500))  # Resize pipe image to fit
pipe_image_rotate = pygame.transform.rotate(pipe_image, 180)
ground_image = pygame.image.load('ground.png')  # Optional ground image if you want
ground_image = pygame.transform.scale(ground_image, (SCREEN_WIDTH, GROUND_HEIGHT))

# Font for displaying score
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()

# Bird Class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def draw(self):
        screen.blit(bird_image, (self.x, self.y))

# Pipe Class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - GROUND_HEIGHT)
        self.passed = False

    def update(self):
        self.x -= 3

    def draw(self):
        # Draw the upper and lower pipes
        screen.blit(pipe_image_rotate, (self.x, self.height - pipe_image.get_height()))
        screen.blit(pipe_image, (self.x, self.height + PIPE_GAP))

# Check collision between bird and pipes
def check_collision(bird, pipes):
    for pipe in pipes:
        if (bird.x + bird_image.get_width() > pipe.x and bird.x < pipe.x + pipe_image.get_width()):
            if bird.y < pipe.height or bird.y + bird_image.get_height() > pipe.height + PIPE_GAP:
                return True
    if bird.y + bird_image.get_height() >= SCREEN_HEIGHT - GROUND_HEIGHT:
        return True
    return False

# Display the start screen
def start_screen():
    while True:
        screen.fill((135, 206, 235))  # Background color (light blue)
        screen.blit(background_image, (0, 0))
        title_text = font.render("Flappy Bird", True, (255, 255, 255))
        instructions_text = font.render("Press SPACE to start", True, (255, 255, 255))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(instructions_text, (SCREEN_WIDTH // 2 - instructions_text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True
# Display the end screen
def end_screen(score):
    while True:
        screen.fill((135, 206, 235))  # Background color (light blue)
        screen.blit(background_image, (0, 0))
        
        # Game over text
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
        
        # Score display
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
        
        # Replay instruction
        replay_text = font.render("Press SPACE to play again", True, (255, 255, 255))
        screen.blit(replay_text, (SCREEN_WIDTH // 2 - replay_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True

# Main Game Loop
def game_loop():
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + 100)]
    score = 0

    running = True
    while running:
        screen.fill((135, 206, 235))  # Background color (light blue)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None  # Người chơi thoát
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.flap()

        # Bird update
        bird.update()

        # Pipes update
        if len(pipes) == 0 or pipes[-1].x < SCREEN_WIDTH - 200:
            pipes.append(Pipe(SCREEN_WIDTH))
        for pipe in pipes:
            pipe.update()

        # Remove pipes off-screen
        pipes = [pipe for pipe in pipes if pipe.x > -pipe_image.get_width()]

        # Check for collisions
        if check_collision(bird, pipes):
            return score  # Trả về điểm số nếu game kết thúc

        # Check for score increment
        for pipe in pipes:
            if not pipe.passed and pipe.x + pipe_image.get_width() < bird.x:
                pipe.passed = True
                score += 1  # Tăng điểm khi chim vượt qua cột

        # Draw bird and pipes
        bird.draw()
        for pipe in pipes:
            pipe.draw()

        # Draw ground
        screen.blit(ground_image, (0, SCREEN_HEIGHT - GROUND_HEIGHT))

        # Display the score
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        # Update display and tick clock
        pygame.display.update() 
        clock.tick(30)

# Run the game
while True:
    if not start_screen():  # Bắt đầu từ màn hình bắt đầu
        break
    score = game_loop()  # Trò chơi chính, trả về điểm số
    if score is None:  # Nếu người chơi thoát, kết thúc vòng lặp
        break
    if not end_screen(score):  # Màn hình kết thúc
        break

pygame.quit()
