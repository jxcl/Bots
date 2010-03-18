'''
Created on Dec 17, 2009

@author: Alex
'''

import pygame
import random
import botflags
import math
import constants


flag = botflags.botflags()
class robot():
    '''
    The "bot" class represents any single swarm bot.
    '''


    def __init__(self, pos = [-1,0], dest = -1):
        '''
        Constructor
        '''
        
        self.position = [0,0]
        
        if pos[0] != -1:
            self.position = pos
        else:
            self.position[0] = random.randint(0,constants.HEIGHT)
            self.position[1] = random.randint(0,constants.WIDTH)
        
        self.heading = [0,0]
        self.state = flag.BLACK
        self.captures = 0
        self.speed = constants.BOT_SPEED
        
        if dest == -1:
            self.new_dest()
        else:
            self.destination = dest
            
    def get_rect(self):
        '''Returns the rectangle of the bot.'''
        
        rectangle = pygame.Rect(self.position[0],self.position[1],5,5)
        
        return rectangle
    
    def update(self):
        if self.at_dest():
            self.new_dest()
        else:
            
            self.position[0] += self.heading[0]
            self.position[1] += self.heading[1]
    
    def at_dest(self):
        '''Returns true if the bot within 2 pixels of its destination.'''
        if abs(self.destination[0]-self.position[0] < 3) and abs(self.destination[1] - self.position[1]) < 3:
            return True
        else:
            return False
    
    def adjust_hdg(self):
        '''Sets the appopriate heading of the bot.
        
        It doesn't use trigonometry to set the speed, so
        speed is not constant. However, it works well enough.
        '''
        
        delta_x = self.destination[0] - self.position[0]
        delta_y = self.destination[1] - self.position[1]
        
        div = (abs(delta_x) + abs(delta_y)) * 1.0
        if div >= 1:
            self.heading[0] = (delta_x / div) * self.speed
            self.heading[1] = (delta_y / div) * self.speed
        elif div < 1:
            self.heading[0] = delta_x * self.speed
            self.heading[1] = delta_y * self.speed
        
    def new_dest(self):
        x = random.randint(1, constants.HEIGHT)
        y = random.randint(1, constants.WIDTH)
        
        self.destination = [x, y]
        
        self.adjust_hdg()
        
    def set_state(self, state):
        self.state = state
        if self.state == flag.RED:
            self.captures = 5
            self.speed = 0
            self.adjust_hdg()
        elif self.state == flag.GREEN:
            self.captures = 3
            self.speed = constants.BOT_SPEED
            
            self.new_dest()
        
    
    def proximity(self, bot_list):
        '''Detects close bots.'''
        prox_list = []
        for bot in bot_list:
            dist_x = abs(bot.position[0] - self.position[0])
            dist_y = abs(bot.position[1] - self.position[1])
            
            distance_to_bot = dist_x**2 + dist_y**2
            
            if distance_to_bot < constants.CAPTURE_RADIUS_SQUARE:
                if self.position != bot.position:
                    prox_list.append(bot)
        
        return prox_list
    def attempt_capture(self, bot):
        
        if self.captures > 0:
            roll = random.randint(0,5)
            
            if roll == 0:
                bot.set_state(self.state)
                self.captures -= 1
    def color_mod(self):
        if self.state == flag.RED:
            return (125 + self.captures * 26, 0, 0)
        elif self.state == flag.GREEN:
            return (0, 125 + self.captures * 43, 0)
        else:
            return (255, 255, 255)
    
    def tick(self, bot_list):
        '''performs all operations in a single frame.'''
        self.update()
        if self.state != flag.BLACK:
            close_bots = self.proximity(bot_list)
            for bot in close_bots:
                if bot.state != self.state:
                    self.attempt_capture(bot)
    def offscreen(self):
        '''For debugging purposes.'''
        if abs(self.position[0]-constants.HEIGHT) > constants.HEIGHT or abs(self.position[1]-constants.WIDTH) > constants.WIDTH:
            return True
        else:
            return False