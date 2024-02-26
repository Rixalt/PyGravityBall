import pygame
import random

pygame.init()

# Розміри вікна
width = 800
height = 600

# Кольори
black = (0, 0, 0)
white = (255, 255, 255)
blue = (255, 0, 0)
yellow = (255, 255, 0)

# Створення вікна
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gravity Ball")

clock = pygame.time.Clock()

# Початкові координати м'яча
ball_x = width // 2
ball_y = height - 50
ball_radius = 20

# Швидкість руху м'яча
ball_speed_x = 3
ball_speed_y = 0

# Перемикачі руху м'яча
moving_up = False
moving_down = False

# Перешкоди
obstacles = []
obstacle_width = 70
obstacle_height = 5
obstacle_speed = 3

# Інтервал для додавання нової перешкоди (у кадрах)
add_obstacle_interval = 120
frames_since_last_obstacle = 0

# Монетка
coin_width = 20
coin_height = 20
coin_x = random.randint(0, width - coin_width)
coin_y = random.randint(0, height - coin_height)
score = 0

def show_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

        screen.fill(black)
        font = pygame.font.Font(None, 36)
        start_text = font.render(
            "Натисніть Enter, щоб розпочати гру", True, white)
        screen.blit(start_text, (width // 2 -
                    start_text.get_width() // 2, height // 2))
        pygame.display.flip()
        clock.tick(60)


def show_game_over_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

        screen.fill(black)
        font = pygame.font.Font(None, 36)
        game_over_text = font.render("Гра закінчена", True, white)
        restart_text = font.render(
            "Натисніть Enter, щоб розпочати нову гру", True, white)
        screen.blit(game_over_text, (width // 2 -
                    game_over_text.get_width() // 2, height // 2 - 50))
        screen.blit(restart_text, (width // 2 -
                    restart_text.get_width() // 2, height // 2))
        pygame.display.flip()
        clock.tick(60)

# Додавання горизонтальної перешкоди
def add_horizontal_obstacle():
    obstacle_y = random.randint(0, height - obstacle_height)
    # Випадковий напрямок руху перешкоди
    obstacle_dx = obstacle_speed * random.choice([-1, 1])
    # Випадковий бік, з якого з'явиться перешкода
    obstacle_side = random.choice(["left", "right"])

    if obstacle_side == "left":
        obstacle_x = -obstacle_width
    else:
        obstacle_x = width

    obstacles.append((obstacle_x, obstacle_y, obstacle_width,
                      obstacle_height, obstacle_dx))

show_menu()

running = True
game_over = False 

while running:
    while game_over:
        show_game_over_screen()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_over = False
                    ball_x = width // 2
                    ball_y = height - 50
                    ball_speed_x = 3
                    ball_speed_y = 0
                    moving_up = False
                    moving_down = False
                    obstacles = []
                    coin_x = random.randint(0, width - coin_width)
                    coin_y = random.randint(0, height - coin_height)
                    score = 0
                    frames_since_last_obstacle = 0
                    add_horizontal_obstacle()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = False 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                moving_up = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                moving_up = False

    # Рух м'яча
    if moving_up:
        ball_speed_y = -3
    else:
        ball_speed_y = 3

    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Відштовхування від країв вікна
    if ball_x >= width - ball_radius or ball_x <= ball_radius:
        ball_speed_x *= -1
    if ball_y >= height - ball_radius:
        ball_speed_y *= -1
        ball_y = height - ball_radius
    if ball_y <= ball_radius:
        ball_speed_y *= -1
        ball_y = ball_radius

    # Очищення екрану
    screen.fill(black)

    player_rect = pygame.Rect(
        ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)

    # Відображення м'яча
    pygame.draw.circle(screen, white, (ball_x, ball_y), ball_radius)
    pygame.draw.circle(screen, blue, (ball_x, ball_y), ball_radius - 2)

    # Відображення перешкод
    for obstacle in obstacles:
        obstacle_x, obstacle_y, obstacle_param1, obstacle_param2, obstacle_dx = obstacle

        pygame.draw.rect(screen, white, (obstacle_x, obstacle_y,
                                         obstacle_param1, obstacle_param2))

        # Рух перешкоди
        obstacle_x += obstacle_dx

        # Перевірка, чи перешкода виходить за межі екрану
        if (obstacle_x > width and obstacle_dx > 0) or (obstacle_x < -obstacle_param1 and obstacle_dx < 0):
            obstacles.remove(obstacle)
            add_horizontal_obstacle()
        else:
            obstacles[obstacles.index(obstacle)] = (
                obstacle_x, obstacle_y, obstacle_param1, obstacle_param2, obstacle_dx)

        # Перевірка торкання з гравцем
        obstacle_rect = pygame.Rect(
            obstacle_x, obstacle_y, obstacle_param1, obstacle_param2)
        if player_rect.colliderect(obstacle_rect):
            print("Гра закінчена")
            running = False

    # Відображення монетки
    pygame.draw.ellipse(
        screen, white, (coin_x, coin_y, coin_width, coin_height))
    pygame.draw.ellipse(screen, yellow, (coin_x + 2,
                                         coin_y + 2, coin_width - 4, coin_height - 4))

    # Перевірка торкання гравця з монеткою
    if player_rect.colliderect(pygame.Rect(coin_x, coin_y, coin_width, coin_height)):
        score += 1
        coin_x = random.randint(0, width - coin_width)
        coin_y = random.randint(0, height - coin_height)

    # Відображення рахунку
    font = pygame.font.Font(None, 36)
    text = font.render("Рахунок: " + str(score), True, white)
    screen.blit(text, (10, 10))

    # Додавання нової перешкоди
    frames_since_last_obstacle += 1
    if frames_since_last_obstacle >= add_obstacle_interval and len(obstacles) < 5:
        add_horizontal_obstacle()
        frames_since_last_obstacle = 0

    # Оновлення екрану
    pygame.display.flip()

    # Обмеження кількості кадрів на секунду
    clock.tick(60)

show_game_over_screen()

pygame.quit()
