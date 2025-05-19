import pygame
import asyncio
import platform
import time
from datetime import datetime
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stopwatch & Clock")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DEEP_BLUE = (10, 25, 47)
CYAN = (0, 255, 255)
DARK_CYAN = (0, 139, 139)
HOVER_CYAN = (0, 191, 255)
SHADOW = (30, 30, 30, 100)

# Fonts
font_large = pygame.font.SysFont("dejavusans", 60, bold=True)
font_medium = pygame.font.SysFont("dejavusans", 40, bold=True)
font_small = pygame.font.SysFont("dejavusans", 28, bold=True)

# Stopwatch variables
stopwatch_running = False
start_time = 0
elapsed_time = 0

# Button class with gradient and shadow
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.font = font_small

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        color = self.hover_color if is_hovered else self.color
        # Draw shadow
        shadow_rect = pygame.Rect(self.rect.x + 5, self.rect.y + 5, self.rect.width, self.rect.height)
        pygame.draw.rect(screen, SHADOW, shadow_rect, border_radius=15)
        # Draw gradient button
        for i in range(self.rect.height):
            gradient_color = (
                color[0],
                color[1],
                color[2] - i * 2 if color[2] > i * 2 else color[2]
            )
            pygame.draw.rect(screen, gradient_color, (self.rect.x, self.rect.y + i, self.rect.width, 1))
        # Draw border
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=15)
        # Draw text
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# Buttons
start_button = Button("Start", 50, 300, 120, 60, DARK_CYAN, HOVER_CYAN)
stop_button = Button("Stop", 240, 300, 120, 60, DARK_CYAN, HOVER_CYAN)
reset_button = Button("Reset", 430, 300, 120, 60, DARK_CYAN, HOVER_CYAN)

def setup():
    screen.fill(DEEP_BLUE)

def draw_gradient_background():
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(DEEP_BLUE[0] * (1 - ratio) + CYAN[0] * ratio)
        g = int(DEEP_BLUE[1] * (1 - ratio) + CYAN[1] * ratio)
        b = int(DEEP_BLUE[2] * (1 - ratio) + CYAN[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

def format_time(ms):
    hours = ms // 3600000
    ms %= 3600000
    minutes = ms // 60000
    ms %= 60000
    seconds = ms // 1000
    milliseconds = ms % 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

def update_loop():
    global stopwatch_running, start_time, elapsed_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return

        if start_button.is_clicked(event) and not stopwatch_running:
            stopwatch_running = True
            start_time = time.time() * 1000 - elapsed_time

        if stop_button.is_clicked(event) and stopwatch_running:
            stopwatch_running = False
            elapsed_time = time.time() * 1000 - start_time

        if reset_button.is_clicked(event):
            stopwatch_running = False
            elapsed_time = 0
            start_time = 0

    # Draw gradient background
    draw_gradient_background()

    # Draw card for stopwatch and clock
    card_rect = pygame.Rect(50, 50, 500, 200)
    pygame.draw.rect(screen, SHADOW, (card_rect.x + 5, card_rect.y + 5, card_rect.width, card_rect.height), border_radius=20)
    pygame.draw.rect(screen, DEEP_BLUE, card_rect, border_radius=20)
    pygame.draw.rect(screen, CYAN, card_rect, 2, border_radius=20)

    # Draw title
    title_text = font_medium.render("Stopwatch & Clock", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 80))
    screen.blit(title_text, title_rect)

    # Draw stopwatch with pulse effect
    if stopwatch_running:
        elapsed_time = time.time() * 1000 - start_time
    pulse = 1.0 + 0.05 * math.sin(time.time() * 3)
    stopwatch_text = font_large.render(format_time(int(elapsed_time)), True, WHITE)
    stopwatch_rect = stopwatch_text.get_rect(center=(WIDTH // 2, 140))
    # Draw glow
    glow_surf = font_large.render(format_time(int(elapsed_time)), True, CYAN)
    glow_rect = glow_surf.get_rect(center=(WIDTH // 2, 140))
    screen.blit(glow_surf, glow_rect)
    screen.blit(stopwatch_text, stopwatch_rect)

    # Draw clock with pulse
    current_time = datetime.now().strftime("%H:%M:%S")
    clock_text = font_medium.render(f"Time: {current_time}", True, WHITE)
    clock_rect = clock_text.get_rect(center=(WIDTH // 2, 200))
    glow_clock = font_medium.render(f"Time: {current_time}", True, CYAN)
    glow_clock_rect = glow_clock.get_rect(center=(WIDTH // 2, 200))
    screen.blit(glow_clock, glow_clock_rect)
    screen.blit(clock_text, clock_rect)

    # Draw buttons
    start_button.draw(screen)
    stop_button.draw(screen)
    reset_button.draw(screen)

    pygame.display.flip()

async def main():
    setup()
    while True:
        update_loop()
        await asyncio.sleep(1.0 / 60)  # 60 FPS

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())