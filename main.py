import pathlib
import pygame
import math
from random import randint


pygame.init()

WIDTH = 900
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial Black', 50)
end_font = pygame.font.SysFont('Arial White', 90)

end_x = 240
end_y = 250

# ---------------------------------------
# Colors
# ---------------------------------------

BLUE = (0, 0, 250)
GREY = (200, 200, 200)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
ORANGE = (200, 100, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# ---------------------------------------
# picture properties
# ---------------------------------------

CWD = pathlib.Path(__file__).parent
background_file_name = pygame.image.load(CWD / 'images/background.jpg')
background = pygame.transform.scale(background_file_name, (WIDTH, HEIGHT))


# ---------------------------------------
# game properties
# ---------------------------------------

ball_color = BLUE

# Ball variables
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_r = 40
speed_x = speed_y = randint(2, 4)

# player variables
mouse_x = 0
mouse_y = 0
mouse_r = 40

# Redeclare the two balls from template 1

# Declare variables wall_y, wall_x, wall_h to draw a horizontal wall. Declare wall_speed to move it.
# - wall_y must be negative to start at the top of the screen,
# - wall_x must be random value between 10 and 700
# - wall_h and wall_speed should be positive values


#   --------------------           ------------------  wall_y
#   |  LEFT WALL       |    GAP    |  RIGHT WALL    |
#   --------------------           ------------------  wall_y+wall_h
#   0              wall_x        wall_x+3*mouse_r     WIDTH
wall_w = randint(100, 600)
wall_y = -50
wall_h = 20  # COULD DO RANDOM LATE
wall_speed = 2

# Declare a gap in the wall = 3 * mouse_r
GAP = 3 * mouse_r
pass_wall = False
pass_gap = False

timer = 0
lives = 9
score = 0
ball_visible = True
collision = False


def redraw():
    # filling the screen
    screen.blit(background, (0, 0))

    # Draw the left part of the wall
    pygame.draw.rect(screen, BLUE, (0, wall_y, wall_w, wall_h))

    # Draw the right part of the wall
    pygame.draw.rect(screen, BLUE, (wall_w + GAP, wall_y, WIDTH - (wall_w + GAP), wall_h))

    # circles
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_r)
    pygame.draw.circle(screen, ball_color, (mouse_x, mouse_y), mouse_r)

    # lives
    text1 = font.render(f'Lives: {lives}', 1, RED)
    screen.blit(text1, (10, 10))

    # score
    text2 = font.render(f'Score: {score}', 1, RED)
    screen.blit(text2, (WIDTH - 200, 10))
    pygame.display.update()


def game_over():
    screen.fill(BLACK)
    end = end_font.render('GAME OVER =( ', 1, RED)
    screen.blit(end, (end_x, end_y))
    pygame.display.update()


# -------------------------------------------------------
# Main loop
# -------------------------------------------------------

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # ball
    ball_x += speed_x
    ball_y += speed_y

    # bouncing ball
    if ball_x < 0 + ball_r or ball_x > WIDTH - ball_r:
        speed_x *= -1
    if ball_y < 0 + ball_r or ball_y > HEIGHT - ball_r:
        speed_y *= -1

    # mouse:
    if ball_visible:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect(mouse_x - mouse_r, mouse_y - mouse_r, mouse_r * 2, mouse_r * 2)
    gapRect = pygame.Rect(wall_w, wall_y, GAP, wall_h)
    if pygame.Rect.colliderect(mouse_rect, gapRect) and not pass_gap:
        score += 1
        pass_gap = True

    left_rect = pygame.Rect(0, wall_y, wall_w, wall_h)
    right_rect = pygame.Rect(wall_w + GAP, wall_y, WIDTH - (wall_w + GAP), wall_h)

    if (
        pygame.Rect.colliderect(mouse_rect, left_rect) or pygame.Rect.colliderect(mouse_rect, right_rect)
    ) and not pass_wall:
        score -= 1
        lives -= 1
        pass_wall = True

    # walls
    wall_y += wall_speed
    wall_speed += wall_speed * 0.02

    if wall_y > HEIGHT:
        wall_y = -50
        wall_w = randint(10, WIDTH - 200)
        wall_speed = 2
        timer = 0
        pass_gap = False

    if wall_y > HEIGHT and not ball_visible:
        ball_r = randint(30, 60)
        ball_color = (randint(0, 255), randint(0, 255), randint(0, 255))
        ball_visible = True

    if (
        (mouse_x - mouse_r < wall_w or wall_w + GAP < mouse_x + mouse_r)
        and wall_y + wall_h > mouse_y - mouse_r
        and wall_y < mouse_y + mouse_r
    ):
        ball_visible = False
        mouse_y += wall_speed

        # Generate a new mouse ball with different color and size
        new_mouse_x = randint(mouse_r, WIDTH - mouse_r)
        new_mouse_y = randint(mouse_r, HEIGHT // 2)  # Regenerate above half of the screen
        new_mouse_r = randint(20, 50)

    # Regenerate the ball above the screen
    if mouse_y > HEIGHT:
        mouse_x, mouse_y, mouse_r, ball_color = new_mouse_x, new_mouse_y, new_mouse_r, ball_color
        ball_visible = True
        ball_color = (randint(0, 255), randint(0, 255), randint(0, 255))  # New color for the mouse ball

    distance = math.dist((ball_x, ball_y), (mouse_x, mouse_y))
    if distance < ball_r + mouse_r and not collision:
        lives -= 1
        collision = True
    if distance > ball_r + mouse_r:
        collision = False

    if lives <= 0:
        run = False

    redraw()
    clock.tick(60)

game_over()
pygame.time.delay(2000)
pygame.quit()
