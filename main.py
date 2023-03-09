import pygame
import os
import random
pygame.init()  # now use display and fonts

WIDTH, HEIGHT = 600, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame test")
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255, 0, 0)
FRAMES_BETWEEN_SPAWN = 60
VEL = 10
FPS = 60
SIZE = (40, 40)
HALF_SIZE = (20, 20)
SPEED_INIT = 3
NB_PER_LAYER_INIT = 3
PROBABILITY_APPLE = 0.1
MONSTER_IMAGE = pygame.image.load(os.path.join("Assets", "zombie.png"))
MONSTER = pygame.transform.scale(MONSTER_IMAGE, SIZE)
PLAYER = pygame.image.load(os.path.join("Assets", "player.png"))
PLAYER = pygame.transform.scale(PLAYER, SIZE)
HEART = pygame.image.load(os.path.join("Assets", "heart.png"))
HEART = pygame.transform.scale(HEART, SIZE)
APPLE = pygame.image.load(os.path.join("Assets", "apple.png"))
APPLE = pygame.transform.scale(APPLE, SIZE)
font = pygame.font.Font('freesansbold.ttf', 32)

INVINCIBILITY = 60


def draw_window(player, monster_list, apple_list, collision, hp, speed, number_per_layer):
    WIN.fill(WHITE)
    if collision:
        WIN.fill(RED)
    for monster in monster_list:
        WIN.blit(MONSTER, (monster.x, monster.y))
    for apple in apple_list:
        WIN.blit(APPLE, (apple.x, apple.y))

    pygame.draw.rect(WIN, (0,0,0), pygame.Rect(0, 0, WIDTH, 40))

    font = pygame.font.SysFont('Comic Sans MS', 30)

    TEXT = font.render(
        f'Speed {speed-SPEED_INIT+1} Difficulty {number_per_layer-NB_PER_LAYER_INIT+1}', True, WHITE, BLACK)
    textRect = TEXT.get_rect()
    textRect.center = (3*WIDTH // 4, 20)
    WIN.blit(TEXT, textRect)
  
   
    for n in range(hp):
        WIN.blit(HEART, (n*40, 0))
    WIN.blit(PLAYER, (player.x, player.y))
    pygame.display.update()


def move_player(keys_pressed, player):
    if keys_pressed[pygame.K_q] and player.x - VEL > 0:  # LEFT
        player.x -= VEL
    if keys_pressed[pygame.K_d] and player.x + VEL + player.width < WIDTH:  # RIGHT
        player.x += VEL
    if keys_pressed[pygame.K_z] and player.y - VEL > 0:  # UP
        player.y -= VEL
    if keys_pressed[pygame.K_s] and player.y + VEL + player.height < HEIGHT:  # DOWN
        player.y += VEL


def check_collisions(player, monster_list):
    collision = False
    for monster in monster_list:
        if abs(player.x - monster.x) < 40 and abs(player.y - monster.y) < 40:
            collision = True
    return collision


def check_collisions_apples(player, apple_list, hp):
    collision = False
    to_remove_i = None
    for i, apple in enumerate(apple_list):
        if abs(player.x - apple.x) < 40 and abs(player.y - apple.y) < 40:
            to_remove_i = i
            hp += 1
            apple_list.pop(to_remove_i)  # care pop within loop
            print(hp)
            break
    return apple_list, hp


def spawn_monsters(monster_list, number):
    for n in range(number):
        collision = True
        while collision:
            collision = False
            x = random.randint(0, WIDTH-40)
            monster = pygame.Rect(x, -40, 40, 40)
            collision = check_collisions(monster, monster_list)
        monster_list.append(monster)
    return monster_list


def spawn_apple(monster_list, apple_list):
    prob = random.random()
    if prob < PROBABILITY_APPLE:
        collision = True
        while collision:
            collision = False
            x = random.randint(0, WIDTH-40)
            apple = pygame.Rect(x, -40, 40, 40)
            collision = check_collisions(apple, monster_list)
        apple_list.append(apple)


def move_monsters(monster_list, speed):
    for monster in monster_list:
        monster.y += speed


def move_apples(apple_list, speed):
    for apple in apple_list:
        apple.y += speed


def main():
    clock = pygame.time.Clock()
    run = True
    COMPTEUR = 1

    player = pygame.Rect(300, 800, 40, 40)
    speed = SPEED_INIT
    frames_between_spawn = FRAMES_BETWEEN_SPAWN
    monster_list = []
    apple_list = []
    hp = 3
    number_per_layer = NB_PER_LAYER_INIT

    invincibility = 0
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys_pressed = pygame.key.get_pressed()
        if COMPTEUR % frames_between_spawn == 0:
            spawn_monsters(monster_list, number_per_layer)
            spawn_apple(monster_list, apple_list)
        if COMPTEUR % 360 == 0:
            speed += 1
        if COMPTEUR % 1024 == 0:
            frames_between_spawn //= 1.5
        if COMPTEUR % 2048 == 0: 
            number_per_layer += 1
        COMPTEUR += 1
        move_monsters(monster_list, speed)
        move_apples(apple_list, speed)
        move_player(keys_pressed, player)
        collision = check_collisions(player, monster_list)
        apple_list, hp = check_collisions_apples(player, apple_list, hp)
        if collision and invincibility == 0:
            hp -= 1
            invincibility = INVINCIBILITY
        if invincibility > 0:
            invincibility -= 1
        draw_window(player, monster_list, apple_list,
                    collision, hp, speed, number_per_layer)
        if hp == 0:
            run = False
    pygame.quit()


if __name__ == "__main__":
    main()
