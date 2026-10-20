
import pygame
import random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 420, 760
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multi Hot Virtual Slots")
clock = pygame.time.Clock()

# Colors
BG = (4, 45, 34)
DARK = (3, 25, 22)
GREEN = (10, 110, 67)
GOLD = (255, 195, 45)
WHITE = (255, 255, 255)
RED = (220, 45, 60)
PALE = (180, 255, 210)

font = pygame.font.Font(None, 27)
small = pygame.font.Font(None, 21)
large = pygame.font.Font(None, 39)
title_font = pygame.font.Font(None, 37)

# Symbol labels and colors
SYMBOLS = [
    ("OR", (255, 135, 20)),
    ("LM", (245, 220, 35)),
    ("WM", (235, 65, 75)),
    ("PL", (100, 35, 130)),
    ("CH", (230, 35, 60)),
    ("GR", (100, 65, 190)),
    ("BL", (240, 175, 30)),
    ("7", (230, 40, 50)),
    ("WILD", (20, 190, 100)),
]

PAYOUTS = {
    "OR": 2, "LM": 2, "WM": 3,
    "PL": 3, "CH": 4, "GR": 3,
    "BL": 5, "7": 10, "WILD": 15,
}

ROWS, COLS = 3, 5
CELL_W, CELL_H = 72, 95
GRID_X, GRID_Y = 22, 190

balance = 1000
bet = 10
message = "Tap SPIN to play!"
last_win = 0

def text_center(text, font_obj, color, x, y):
    image = font_obj.render(str(text), True, color)
    rect = image.get_rect(center=(x, y))
    screen.blit(image, rect)

def make_reels():
    return [
        [random.choice(SYMBOLS)[0] for _ in range(ROWS)]
        for _ in range(COLS)
    ]

reels = make_reels()

def draw_symbol(symbol, rect):
    # Colored symbol tile
    pygame.draw.rect(screen, (1, 55, 43), rect, border_radius=9)
    pygame.draw.rect(screen, GOLD, rect, 2, border_radius=9)

    color = dict(SYMBOLS).get(symbol, WHITE)

    # Draw a simple colorful fruit-like emblem
    cx, cy = rect.center
    radius = 22 if symbol != "WILD" else 25
    pygame.draw.circle(screen, color, (cx, cy - 7), radius)
    pygame.draw.circle(screen, WHITE, (cx - 7, cy - 14), 5)

    text_center(
        symbol, small if symbol != "WILD" else font,
        WHITE, cx, cy + 27
    )

def draw_button(rect, label, color):
    pygame.draw.rect(screen, GOLD, rect, border_radius=15)
    inner = rect.inflate(-4, -4)
    pygame.draw.rect(screen, color, inner, border_radius=13)
    text_center(label, font, WHITE, rect.centerx, rect.centery)

def draw_game():
    screen.fill(BG)

    # Decorative background
    for i in range(18):
        x = (i * 83 + 19) % WIDTH
        y = (i * 117 + 35) % HEIGHT
        pygame.draw.circle(screen, (5, 64, 46), (x, y), 18)

    text_center("MULTI HOT 5", title_font, GOLD, WIDTH // 2, 48)
    text_center("VIRTUAL WILD SLOTS", font, PALE, WIDTH // 2, 82)

    # Balance and bet panels
    pygame.draw.rect(
        screen, GOLD, (20, 112, 185, 48), border_radius=10
    )
    pygame.draw.rect(
        screen, DARK, (23, 115, 179, 42), border_radius=8
    )
    text_center("COINS", small, PALE, 112, 125)
    text_center(balance, font, GOLD, 112, 145)

    pygame.draw.rect(
        screen, GOLD, (215, 112, 185, 48), border_radius=10
    )
    pygame.draw.rect(
        screen, DARK, (218, 115, 179, 42), border_radius=8
    )
    text_center("BET", small, PALE, 307, 125)
    text_center(bet, font, GOLD, 307, 145)

    # Reel grid
    pygame.draw.rect(
        screen, GOLD,
        (GRID_X - 5, GRID_Y - 5,
         COLS * CELL_W + 10, ROWS * CELL_H + 10),
        border_radius=10
    )
    pygame.draw.rect(
        screen, DARK,
        (GRID_X, GRID_Y,
         COLS * CELL_W, ROWS * CELL_H),
        border_radius=8
    )

    for col in range(COLS):
        for row in range(ROWS):
            rect = pygame.Rect(
                GRID_X + col * CELL_W + 3,
                GRID_Y + row * CELL_H + 3,
                CELL_W - 6, CELL_H - 6
            )
            draw_symbol(reels[col][row], rect)

    # Message area
    pygame.draw.rect(
        screen, DARK, (18, 490, WIDTH - 36, 58),
        border_radius=10
    )
    text_center(
        message, small, GOLD, WIDTH // 2, 508
    )
    text_center(
        "Last win: " + str(last_win) + " coins",
        small, WHITE, WIDTH // 2, 531
    )

    # Bet controls
    draw_button(pygame.Rect(35, 570, 95, 48), "- BET", RED)
    draw_button(pygame.Rect(290, 570, 95, 48), "+ BET", GREEN)

    # Spin button
    draw_button(
        pygame.Rect(105, 635, 210, 70),
        "SPIN", (5, 125, 70)
    )

    text_center(
        "For entertainment only - virtual coins",
        small, PALE, WIDTH // 2, 735
    )

    pygame.display.flip()

def calculate_winnings():
    # Three or more matching symbols from the left,
    # with WILD acting as a substitute.
    winnings = 0

    for row in range(ROWS):
        line = [reels[col][row] for col in range(COLS)]

        target = next(
            (symbol for symbol in line if symbol != "WILD"),
            "WILD"
        )

        count = 0
        for symbol in line:
            if symbol == target or symbol == "WILD":
                count += 1
            else:
                break

        if count >= 3:
            multiplier = PAYOUTS[target]
            winnings += bet * multiplier * count

    return winnings

def spin():
    global reels, balance, last_win, message

    if balance < bet:
        message = "Not enough virtual coins!"
        last_win = 0
        return

    balance -= bet
    reels = make_reels()

    last_win = calculate_winnings()
    balance += last_win

    if last_win > 0:
        message = "WIN! +" + str(last_win) + " coins"
    else:
        message = "No win. Try another spin!"

# Main game loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if 635 <= y <= 705 and 105 <= x <= 315:
                spin()

            elif 570 <= y <= 618:
                if 35 <= x <= 130:
                    bet = max(1, bet - 5)
                elif 290 <= x <= 385:
                    bet = min(100, bet + 5)

    draw_game()
    clock.tick(30)

pygame.quit()
