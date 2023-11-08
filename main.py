import random
import time

import pygame

# pygame setup
pygame.init()

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Snake Game')
running = True
x = 300
y = 300
pos_x = 20
pos_y = 0
clock = pygame.time.Clock()
food_x = 100
food_y = 100
window_width = 600
window_height = 600
col1 = (204, 255, 255)
col2 = (204, 229, 255)
body_x = x
body_y = y

game_over_font = pygame.font.Font(None, 50)
game_over_text = game_over_font.render("Game Over", True, (0, 0, 0))
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (window_width // 2, window_height // 2)

score_font = pygame.font.Font(None, 36)
score = 0

color_body = (255, 150, 255)
color_snake = (255, 51, 255)
head_snake = pygame.Rect(x, y, 20, 20)
body = [head_snake]


def draw_grid():
    block_size = 20
    count_i = 0
    count_j = 0
    for i in range(0, window_width, block_size):
        count_i += 1
        for j in range(0, window_height, block_size):
            count_j += 1
            rec1 = pygame.Rect(i, j, 20, 20)
            pygame.draw.rect(screen, col1, rec1)
            if count_i % 2 == 0 and count_j % 2 == 1:
                rec2 = pygame.Rect(i, j, 20, 20)
                pygame.draw.rect(screen, col2, rec2)
            elif count_j % 2 == 0 and count_i % 2 == 1:
                rec2 = pygame.Rect(i, j, 20, 20)
                pygame.draw.rect(screen, col2, rec2)


def draw_snake_food():
    col_food = (0, 128, 128)
    food_rec = pygame.Rect(food_x, food_y, 20, 20)
    pygame.draw.rect(screen, col_food, food_rec)
    return food_rec


def place_random_food():
    global food_x, food_y
    food_x = random.randrange(0, 600, 20)
    food_y = random.randrange(0, 600, 20)


def draw_body(big_body):
    for snake_body in big_body:
        pygame.draw.rect(screen, color_body, snake_body)


def show_score():
    pygame.time.delay(1)
    screen.blit(game_over_text, game_over_rect)
    score_text = score_font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()
    pygame.display.update()


def update_body_first_iteration(big_body, body1_x, body1_y):
    # WORK AROUND first iteration
    big_body.append(pygame.Rect(body1_x, body1_y, 20, 20))


def update_body(big_body, body_x, body_y):
    if len(big_body) == 1:
        update_body_first_iteration(big_body, body_x, body_y)
    new_body = big_body.copy()
    new_body.reverse()
    for i in range(0, len(new_body) - 1):  # SHIFT
        new_body[i].y = new_body[i + 1].y
        new_body[i].x = new_body[i + 1].x
    new_body.pop(-1)  # pop the head body element
    new_body.reverse()
    return new_body

while running:
    event = pygame.event.poll()
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    food_pos = draw_snake_food()

    body_x = x
    body_y = y
    x += pos_x
    y += pos_y

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            pos_x = 20
            pos_y = 0
        if event.key == pygame.K_LEFT:
            pos_x = -20
            pos_y = 0
        if event.key == pygame.K_DOWN:
            pos_x = 0
            pos_y = 20
        if event.key == pygame.K_UP:
            pos_x = 0
            pos_y = -20
    if head_snake.colliderect(food_pos):  # FOOD eaten
        place_random_food()
        score = score + 10
        # Coordinates of last rect of the body to be appended
        body_rec = pygame.Rect(body_x, body_y, 20, 20)
        body.append(pygame.draw.rect(screen, color_body, body_rec))

    # Update snake
    head_snake.x = x
    head_snake.y = y

    # Update Body
    updated_body = update_body(body, body_x, body_y)


    def body_touch():
        for i in range(1, len(updated_body)):
            if head_snake.colliderect(updated_body[i]):
                print("hi")
                return True
        return False


    def game_over():
        # head and body as arguments to check
        check_1 = x >= 581 or x <= -1 or y <= -1 or y >= 581
        check_2 = body_touch()
        return check_1 or check_2

    if game_over():
        show_score()
        running = False

    # DRAW logic
    pygame.display.flip()
    draw_grid()
    draw_snake_food()
    # draw head AFTER the body because it overlaps it
    draw_body(updated_body)
    pygame.draw.rect(screen, color_snake, head_snake)

    clock.tick(10)
