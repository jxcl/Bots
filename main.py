import pygame
import pygame.gfxdraw
import random
import robot
import botflags
import constants


from pygame.locals import *
from pygame.color import THECOLORS

pygame.init()
flag = botflags.botflags()

screen= pygame.display.set_mode(constants.SIZE)
pygame.display.set_caption("Bots")

screen.fill(THECOLORS['black'])

clock = pygame.time.Clock()

bot_list = []


def populate():
    for x in range(constants.NUM_BOTS):
        bot = robot.robot()
        bot_list.append(bot)
    
    bot_list[0].set_state(flag.GREEN)
    bot_list[1].set_state(flag.RED)

populate()

done = False
while not done:
    dt = clock.tick(constants.FPS)
    screen.fill(THECOLORS['black'])
    
    for bot in bot_list:
        rect = bot.get_rect()
        pygame.gfxdraw.box(screen, rect, bot.color_mod())
        
        bot.tick(bot_list)
        
    pygame.display.update()
    
    events = pygame.event.get( )
    for e in events:
        if( e.type == QUIT ):
            done = True
            break
        elif (e.type == KEYDOWN):
            if( e.key == K_ESCAPE ):
                done = True
                break
            if( e.key == K_f ):
                pygame.display.toggle_fullscreen()
            if( e.key == K_SPACE):
                bot_list = []
                populate()