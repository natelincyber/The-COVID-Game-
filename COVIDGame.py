from pygame import mixer
import pygame
import random
import sys
import os



pygame.init()

WIDTH = 800
HEIGHT = 600

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.display.set_caption("The COVID Game!")

mixer.music.load("background_music.mp3")
mixer.music.play(-1)

ENEMY = pygame.image.load("germ.png")
ENEMY = pygame.transform.scale(ENEMY, (75, 75))
PLAYER = pygame.image.load("boy.png")
PLAYER = pygame.transform.scale(PLAYER, (75, 75))
BACKGROUND = pygame.image.load("covidbackground.png")
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
ORANGE = (245, 135, 0)

BRIGHT_RED = (255, 0, 0)
BRIGHT_GREEN = (0, 255, 0)
BRIGHT_ORANGE = (255, 145, 0)





player_size = 48
player_pos = [WIDTH / 2, HEIGHT - 2 * player_size]

enemy_size = 48
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
enemy_list = [enemy_pos]

SPEED = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

score = 0

clock = pygame.time.Clock()

myFont = pygame.font.SysFont("monospace", 35)

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def set_level(score, SPEED):
    SPEED = score / 5  + 5
    return SPEED


def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, WIDTH - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])


def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        screen.blit(ENEMY, (enemy_pos[0], enemy_pos[1]))



def update_enemy_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(idx)
            score += 1
    return score


def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False


def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True
    return False

def button(msg, x, y, w, h, inactive_color, active_color, action=None, text_size=None):
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action != None:
            click_sound = mixer.Sound("sound_click.wav")
            click_sound.play()
            if action == "play":
                main(game_over, score, SPEED, player_pos)
            elif action == "quit":
                sys.exit()

    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))
    
    small_text = pygame.font.SysFont('monospace', text_size)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ( (x + (w/2), (y + (h/2))))
    screen.blit(text_surf, text_rect)


def start_menu():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(WHITE)
        large_text = pygame.font.SysFont('arial', 80)
        text_surf, text_rect = text_objects("The COVID Game!", large_text)
        text_rect.center = ((WIDTH/2), (HEIGHT/2))
        screen.blit(BACKGROUND,(0,0))
        screen.blit(text_surf, text_rect)

        button("Start!", 150, 450, 100, 50, GREEN, BRIGHT_GREEN, "play", 20)
        button("Exit", 550, 450, 100, 50, RED, BRIGHT_RED, "quit", 20)
  
        pygame.display.update()
        clock.tick(15)


def death_screen(score):
    end = True
    while end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        large_text = pygame.font.SysFont('bitstreamverasans', 40)
        text_surf, text_rect = text_objects('''You Caught the Virus!''',  large_text)
        text_sur, text_rec = text_objects('''Remember to wear a mask and stay safe''', large_text)
        text_rect.center = ((WIDTH/2), (HEIGHT/2 - 50))
        text_rec.center = ((WIDTH/2), (HEIGHT/2 + 20))
        screen.blit(BACKGROUND,(0,0))
        screen.blit(text_surf, text_rect)
        screen.blit(text_sur, text_rec)

        button("Restart", 150, 400, 100, 50, GREEN, BRIGHT_GREEN, "play", 20)
        button("Exit", 550, 400, 100, 50, RED, BRIGHT_RED, "quit", 20)
        button(("Score:" + str(score)), 250, 125, 300, 75, ORANGE, BRIGHT_ORANGE, None, 50)

        pygame.display.update()
        clock.tick(15)

def main(game_over, score, SPEED, player_pos):
    player_size = 45
    player_pos = [WIDTH / 2, HEIGHT - 2 * player_size]

    enemy_size = 45
    enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
    enemy_list = [enemy_pos]
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:

                x = player_pos[0]
                y = player_pos[1]

                if event.key == pygame.K_LEFT:
                    x -= 37
                elif event.key == pygame.K_RIGHT:
                    x += 37

# handle the boundary movement.
                if x >= 740:
                    x = 735
                if x < 0:
                    x = 5
                player_pos = [x, y]

        screen.blit(BACKGROUND,(0,0))

        drop_enemies(enemy_list)
        score = update_enemy_positions(enemy_list, score)
        SPEED = set_level(score, SPEED)

        text = "Score:" + str(score)
        label = myFont.render(text, 1, YELLOW)
        screen.blit(label, (WIDTH - 200, HEIGHT - 40))

        if collision_check(enemy_list, player_pos):
            death_sound = mixer.Sound("deathsound.wav")
            death_sound.play()
            game_over = True 
            break

        draw_enemies(enemy_list)

        screen.blit(PLAYER, (player_pos[0], player_pos[1]))

        clock.tick(30)

        pygame.display.update()

    death_screen(score)

start_menu()
