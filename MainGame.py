

import pygame
import sys
import random
import math
import os
from pygame.locals import*
pygame.init()

#Creates the window, surface, caption and colors
screen = pygame.display.set_mode((800, 500))
clock = pygame.time.Clock()
pygame.display.set_caption('DeadShooter')
font = pygame.font.Font(None, 24)
front = (100, 100, 200)
bg = (0, 0, 0)


#Loading the main files, such as images, sounds
shot_sound = pygame.mixer.Sound("shot.wav")
mainCharImage = pygame.image.load("mainChar.png")
mainEnemyImage = pygame.image.load("mainEnemy.png")
gameover = pygame.image.load("gameover.png")
gameover_r = gameover.get_rect()
gameover_r = gameover_r.move([800/2-gameover_r.width/2, 500/2-gameover_r.height/2])
EnemyDeadImage = pygame.image.load("mainEnemy_dead.png")
mainCharImage_destroyed = pygame.image.load("mainChar_dead.png")

#Uses the built in sprite class
class Sprite:
    pass

shot_image = pygame.image.load("bullet_1.png")

#Variables
mainChar = Sprite()
mainChar.x = 0
mainChar.y = 0
mainChar.redness = 0
shots = []
Enemies = []
Health = 3
mainChar.image = mainCharImage
score = 0
frames_until_next_enemy = random.randrange(20, 100)

#Main functions of the game

def display_sprite(sprite):
    screen.blit(sprite.image, (sprite.x, sprite.y))

#Function for bullets, one of the main modules of the game
def Shoot():
    shot = Sprite()
    shot.x = mainChar.x + 50
    shot.y = mainChar.y + 40
    shot.image = shot_image
    shot.used = False
    shots.append(shot)
#Function that uses the built in random function to spawn enemies
def NewEnemy():
    Enemy = Sprite()
    Enemy.x = screen.get_width()
    Enemy.y = random.randrange(100, screen.get_height() - 100)
    Enemy.image = mainEnemyImage
    Enemy.hit = False
    Enemy.redness = 255
    Enemies.append(Enemy)

def get_sprite_rectangle(sprite):
    return sprite.image.get_rect().move(sprite.x, sprite.y)

#Gameover text. Instructions
Restart_text = font.render ('PRESS ENTER TO PLAY AGAIN', 1, front)
Restart_text_pos = Restart_text.get_rect()
Restart_text_pos.right = screen.get_width() - 270
Restart_text_pos.top = 320

#Main game loop
while True:
    #Press ESCAPE to quit the program ANTI CRASH
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Shoot()
                shot_sound.play()
    mainChar.image = mainCharImage
    PressedKey = pygame.key.get_pressed() #sets a variable for pressed keys

    #Sets the arrow keys to make the main character move
    if PressedKey[pygame.K_UP]:
        mainChar.y = mainChar.y - 5

    if PressedKey[pygame.K_DOWN]:
        mainChar.y = mainChar.y + 5

    if PressedKey[pygame.K_LEFT]:
        mainChar.x = mainChar.x - 5

    if PressedKey[pygame.K_RIGHT]:
        mainChar.x = mainChar.x + 5

    for shot in shots:
        shot.x = shot.x + 25

        shots = [shot for shot in shots if shot.x < screen.get_width() and not shot.used]

        # Stops the main character from going off the screen
    if mainChar.y < 0:
        mainChar.y = 0

    if mainChar.y > screen.get_height() - mainCharImage.get_height():
        mainChar.y = screen.get_height() - mainCharImage.get_height()

    if mainChar.x < 0:
        mainChar.x = 0

    if mainChar.x > screen.get_width() - mainCharImage.get_width():
        mainChar.x = screen.get_width() - mainCharImage.get_width()


    #Sets a time limit for new enemies to spawn
    frames_until_next_enemy = frames_until_next_enemy - 1
    if frames_until_next_enemy <= 0:
        frames_until_next_enemy = random.randrange(10, 40)
        NewEnemy()

    #Creates a 'redness' effect to show that the main character has collided with an enemy, takes off 1 life
    for Enemy in Enemies:
        Enemy.x = Enemy.x - random.randrange(5, 13)
        if Enemy.hit:
            Enemy.redness = max(0, Enemy.redness - 10)

    Enemies = [Enemy for Enemy in Enemies if Enemy.x > - mainEnemyImage.get_width() and not (Enemy.hit and Enemy.redness == 0)]
    mainChar.redness = max(0, mainChar.redness - 10)
    mainChar.redness = max(0, mainChar.redness - 2)
    mainChar_rect = get_sprite_rectangle(mainChar)

    for Enemy in Enemies:
        if Enemy.hit:
            continue
        Enemy_rect = get_sprite_rectangle(Enemy)
        if Enemy_rect.colliderect(mainChar_rect) and Health > 0:
            Enemy.hit = True
            Enemy.x = Enemy.x - 6
            Enemy.y = Enemy.y - 6
            Health = Health - 1
            if Health == 0:
                mainChar.x = mainChar.x - 50
                mainChar.redness = 255

            else:
                mainChar.redness = 255
            continue
        #Checks to see if the bullet and the enemy have collided
        for shot in shots:
            if Enemy_rect.colliderect(get_sprite_rectangle(shot)):
                Enemy.hit = True
                Enemy.x = Enemy.x - 6
                Enemy.y = Enemy.y - 6
                shot.used = True
                score = score + 10
                continue
    screen.fill(bg)
    #Condition that stops the player from having negative lives, makes you restart the game once at 0 lives
    if Health == 0:
        temporary = pygame.Surface(mainCharImage_destroyed.get_size(), pygame.SRCALPHA, 32)
        temporary.fill( (255, 255, 255, mainChar.redness) )
        temporary.blit(mainCharImage_destroyed, (0,0), mainCharImage_destroyed.get_rect(), pygame.BLEND_RGBA_MULT)
        mainChar.image = temporary
        font = pygame.font.Font(None, 25)
        screen.blit(Restart_text, Restart_text_pos)
        screen.blit(gameover, gameover_r)
        if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if PressedKey[K_RETURN]:
            score=0
            Enemies = []
            mainChar.x = 0
            mainChar.y = 0
            mainChar.redness = 0
            mainChar.redness = 0
            Health = 3
    if mainChar.redness > 0:
        temporary = pygame.Surface(mainChar.image.get_size(), pygame.SRCALPHA, 32)
        temporary.fill( (255, 255 - mainChar.redness, 255 - mainChar.redness, 255) )
        temporary.blit(mainChar.image, (0,0), mainChar.image.get_rect(), pygame.BLEND_RGBA_MULT)
        mainChar.image = temporary

    display_sprite(mainChar)
    for shot in shots:
        display_sprite(shot)

    for Enemy in Enemies:
        if Enemy.hit:
            temporary = pygame.Surface( EnemyDeadImage.get_size(), pygame.SRCALPHA, 32)
            temporary.fill( (255, 255, 255, Enemy.redness) )
            temporary.blit(EnemyDeadImage, (0,0), EnemyDeadImage.get_rect(), pygame.BLEND_RGBA_MULT)
            Enemy.image = temporary
        display_sprite(Enemy)

    #Writes out the score and high score and etc on the top of the screen, also uses .bilt and flip to screen everything that happened behind the scenes.
    score_text = font.render("SCORE: " + str(score), 1, front)
    score_text_pos = score_text.get_rect()
    score_text_pos.right = screen.get_width() - 10
    score_text_pos.top = 10
    Health_text = font.render("Health: " + str(Health), 1, front)
    screen.blit(Health_text, (10, 10))
    screen.blit(score_text, score_text_pos)
    info = open("highscore.csv","r")
    highscore = int(info.readline())
    highscore_text = font.render ('HIGHSCORE: ' + str(highscore), 1, front)
    highscore_text_pos = highscore_text.get_rect()
    highscore_text_pos.right = screen.get_width() - 10
    highscore_text_pos.top = 50
    screen.blit(highscore_text, highscore_text_pos)
    if score-1>highscore:
        info = open("highscore.csv","w")
        info.write(str(score))
    pygame.display.flip()

    clock.tick(50)

