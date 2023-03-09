import pygame
import os
import random
WIDTH, HEIGHT = 600, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame test")
WHITE = (255,255,255)
RED = (255,0,0)
VEL = 5
FPS = 60
NUMBER_PER_LAYER=3
SIZE = (40,40)
HALF_SIZE = (20,20)
monster_list = []
SPEED = 3
MONSTER_IMAGE = pygame.image.load(os.path.join("Assets", "zombie.png"))
MONSTER = pygame.transform.scale(MONSTER_IMAGE, SIZE)
PLAYER = pygame.image.load(os.path.join("Assets", "player.png"))
PLAYER = pygame.transform.scale(PLAYER, SIZE)
HEART = pygame.image.load(os.path.join("Assets", "heart.png"))
HEART = pygame.transform.scale(HEART, SIZE)
INVINCIBILITY = 60

def draw_window(player, monster_list,collision,hp):
    WIN.fill(WHITE)
    if collision : 
        WIN.fill(RED)
    for monster in monster_list : 
        WIN.blit(MONSTER,(monster.x, monster.y))
    for n in range(hp) : 
        WIN.blit(HEART,(n*40,0))
    WIN.blit(PLAYER, (player.x, player.y))
    pygame.display.update()

def move_player(keys_pressed,player) : 
    if keys_pressed[pygame.K_q] and player.x - VEL > 0:  # LEFT
        player.x -= VEL
    if keys_pressed[pygame.K_d] and player.x + VEL + player.width < WIDTH:  # RIGHT
        player.x += VEL
    if keys_pressed[pygame.K_z] and player.y - VEL > 0:  # UP
        player.y -= VEL
    if keys_pressed[pygame.K_s] and player.y + VEL + player.height < HEIGHT :  # DOWN
        player.y += VEL

def check_collisions(player,monster_list) : 
    collision = False
    for monster in monster_list : 
        if abs (player.x - monster.x) < 40 and abs(player.y- monster.y) <40 : 
            collision = True
    return collision


def spawn_monsters(monster_list,number) : 
    for n in range(number) : 
        collision = True
        while collision : 
            collision = False
            x = random.randint(0,WIDTH-40)
            monster = pygame.Rect(x, 0, 40, 40)
            collision = check_collisions(monster,monster_list)
        monster_list.append(monster)
    return monster_list

def move_monsters(monster_list) : 
    for monster in monster_list : 
        monster.y+=SPEED
def main(): 
    clock = pygame.time.Clock()
    run = True
    COMPTEUR = 0
    hp = 3
    invincibility = 0
    player = pygame.Rect(300, 800, 40, 40)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys_pressed = pygame.key.get_pressed()
        if COMPTEUR % 60 == 0 : 
            spawn_monsters(monster_list,NUMBER_PER_LAYER)
        COMPTEUR +=1
        move_monsters(monster_list) 
        move_player(keys_pressed,player)
        collision = check_collisions(player,monster_list)
        if collision and invincibility == 0 :
            hp -= 1
            invincibility = INVINCIBILITY 
        if invincibility > 0 : 
            invincibility -=1
        draw_window(player, monster_list, collision,hp)
        if hp == 0 :
            run = False
    pygame.quit()

if __name__ == "__main__":
    main()