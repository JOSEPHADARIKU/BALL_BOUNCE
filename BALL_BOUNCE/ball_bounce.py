import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

import pygame, random

# 🔒 locked (DO NOT TOUCH)
def _joseph_tag():
    _ = [
        "Hello from Joseph! welcome to my game ❤️",
        "https://github.com/JOSEPHADARIKU"
    ]
    for line in _:
        print(line)

_joseph_tag()

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BALL BOUNCE")
FONT = pygame.font.SysFont('Arial', 24)
clock = pygame.time.Clock()

BALL_FOLDER = "assets/balls"
BG_FOLDER = "assets/backgrounds"
ball_options = [f for f in os.listdir(BALL_FOLDER) if f.endswith(".png")]
bg_options = [f for f in os.listdir(BG_FOLDER) if f.endswith((".jpg", ".png"))]
selected_ball = None
selected_bg = None

# Load thumbnails
def load_preview(path, size):
    img = pygame.image.load(path)
    return pygame.transform.scale(img, size)

ball_previews = [(b, load_preview(os.path.join(BALL_FOLDER, b), (100, 100))) for b in ball_options]
bg_previews = [(b, load_preview(os.path.join(BG_FOLDER, b), (200, 120))) for b in bg_options]

def selection_menu():
    global selected_ball, selected_bg
    running = True
    while running:
        screen.fill((25, 25, 25))

        y1, y2 = 60, 250
        x_margin = 50

        title = FONT.render("Pick a Ball and Background", True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 10))

        # Draw ball previews
        ball_rects = []
        for i, (name, img) in enumerate(ball_previews):
            x = x_margin + i * 140
            rect = screen.blit(img, (x, y1))
            ball_rects.append((name, rect))
            if selected_ball == name:
                pygame.draw.rect(screen, (0, 255, 0), rect, 3)

        # Draw bg previews
        bg_rects = []
        for i, (name, img) in enumerate(bg_previews):
            x = x_margin + i * 240
            rect = screen.blit(img, (x, y2))
            bg_rects.append((name, rect))
            if selected_bg == name:
                pygame.draw.rect(screen, (0, 255, 0), rect, 3)

        # Draw start button
        if selected_ball and selected_bg:
            start_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT - 70, 200, 50)
            pygame.draw.rect(screen, (0, 200, 0), start_rect)
            label = FONT.render("START GAME", True, (255, 255, 255))
            screen.blit(label, (start_rect.x + 30, start_rect.y + 10))
        else:
            start_rect = None

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for name, rect in ball_rects:
                    if rect.collidepoint(pos):
                        selected_ball = name
                for name, rect in bg_rects:
                    if rect.collidepoint(pos):
                        selected_bg = name
                if start_rect and start_rect.collidepoint(pos):
                    running = False

        clock.tick(60)

selection_menu()

# === Actual Game ===
class Ball:
    ball_image = pygame.image.load(os.path.join(BALL_FOLDER, selected_ball))
    gravity = 0.1

    def __init__(self):
        self.velocityX = random.choice([-3, 3])
        self.velocityY = random.choice([-3, 3])
        self.X = random.randint(0, 768)
        self.Y = random.randint(0, 350)
        self.radius = 32
        self.id = random.randint(1000, 9999)

    def render(self):
        screen.blit(Ball.ball_image, (self.X, self.Y))

    def move(self):
        self.velocityY += Ball.gravity
        self.X += self.velocityX
        self.Y += self.velocityY
        if self.X < 0 or self.X > 768:
            self.velocityX *= -1
        if self.Y < 0 and self.velocityY < 0:
            self.velocityY *= -1
            self.Y = 0
        if self.Y > 568 and self.velocityY > 0:
            self.velocityY *= -1
            self.Y = 568

    def is_touching(self, other):
        dx = self.X - other.X
        dy = self.Y - other.Y
        dist_sq = dx * dx + dy * dy
        return dist_sq < (self.radius * 2) ** 2

background = pygame.image.load(os.path.join(BG_FOLDER, selected_bg))
Ball_List = [Ball(), Ball()]
collision_log = set()
running = True

while running:
    clock.tick(60)
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for b in Ball_List:
        b.move()
        b.render()

    new_balls = []
    for i in range(len(Ball_List)):
        for j in range(i + 1, len(Ball_List)):
            b1 = Ball_List[i]
            b2 = Ball_List[j]
            pair_key = tuple(sorted((b1.id, b2.id)))
            if b1.is_touching(b2) and pair_key not in collision_log:
                collision_log.add(pair_key)
                new_balls.append(Ball())

    Ball_List.extend(new_balls)
    pygame.display.update()
