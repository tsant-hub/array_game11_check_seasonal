'''
Graph Engine
Description: Handles the graphing of the viewport. Points to be graphed are taken from the market engine.

Needs polishing and optimization
'''

import pygame
import numpy as np
import random
from defaults import *
from utils import *
from trade import *

class Viewport():
    def __init__(self):
        self.width, self.height = scrx/2,scry/2
        self.pos=((scrx-self.width)/2-150,scrx*0.1)
        self.surface = pygame.Surface((self.width, self.height))
        
        self.max_view_height = 10**4
        self.view_height = 2100

        self.max_view_length = 250
        self.view_length = 15
        
        
        '''
        remaining to do for today
        -   modify max view length to be max 252; adjust the viewport naming for that also
        -   make the buy/sell system
        '''

        self.zoom = self.height/self.view_height
        self.interval = 0
        self.total_points = 0
        self.translation = 0
        self.follow = True
        self.y_vals = np.array([0 for i in range(self.max_view_length)])
        self.filter_y_vals = self.y_vals.copy()
        self.x_vals = np.linspace(0, int(self.width), len(self.y_vals))
        self.processed_vals = 0

    def convert_point(self, point):
        if not self.follow:
            mode = self.translation
        else:
            mode = self.y_vals[-1]
        return self.height/2 - ((point-mode) * self.zoom)
    
    def render(self, surface):
        surface.blit(self.surface, self.pos)

        # render the y marker points
        y_marker_surface = pygame.Surface((100,scry/2+40))
        y_marker_surface.fill(colors['bg'])
        zoom = (self.view_height-100)/1000
        if zoom <= 0:
            divs = int(self.max_view_height/400)
            spread = 0.55
        elif zoom == 1:
            divs = int(self.max_view_height/100)
            spread = 1
        elif zoom == 2:
            divs = int(self.max_view_height/40)
            spread = 1
        elif 3 <= zoom <= 4:
            divs = int(self.max_view_height/20)
            spread = 2
        elif zoom >= 5:
            divs = int(self.max_view_height/10)
            spread = 2

        # code makes it so that y translation lets you see more of the top and bottom of the screen if you scroll up down endlessly
        '''
        Issue: dont make strad increase exponentially because it makes the program lag af
        '''
        if self.follow:
            zzz = len(str(abs(int(self.y_vals[-1]))))
            strad = 10**zzz if zzz > 2 else 1000
            yran = int(spread*(self.max_view_height)+strad)
        else:
            zzz = len(str(abs(int(self.translation))))
            strad = 10**zzz if zzz > 2 else 1000
            yran = int(spread*(self.max_view_height)+strad)

        for i in range(-yran, yran, divs):
            mark = text_viewui.render(f'{i}', False, colors['ui'])
            y_marker_surface.blit(mark, (75-mark.size[0],self.convert_point(i)-mark.size[1]/2+20))
        surface.blit(y_marker_surface, (self.surface.width+self.pos[0], self.pos[1]-20))

        # render the x marker points
        ''' optimize this josef '''
        
        x_marker_surface = pygame.Surface((scrx/2+50, 50))
        x_marker_surface.fill(colors['bg'])
        
        # tried to implement one that works like the y scaling but i keep on messing it up
        # for i in range(-int(self.view_length/2), int(self.view_length/2)):
        #     mark = text_viewui.render(f'{self.total_points-i}', False, colors['ui'])
        #       
        #                             vvv modifies which position to place each number
        #     x_marker_surface.blit(mark,(self.x_vals[-i-1+int(self.view_length/2)]-mark.size[0]/2+25,10))
        # surface.blit(x_marker_surface, (self.pos[0]-25,self.pos[1]+self.height))

    
        for i in range(len(self.x_vals)):
            # add a big view / small view approach maybe?            
            if (self.view_length > 100) and (i%15!=0) and (i!=len(self.x_vals)-1):
                continue
            elif (self.view_length > 50) and (i%10!=0) and (i!=len(self.x_vals)-1):
                continue
            elif (self.view_length > 15) and (i%5!=0) and (i!=len(self.x_vals)-1):
                continue
            
            
            mark = text_viewui.render(f'{self.total_points-i}', False, colors['ui'])
            pos = self.x_vals[-i-1]-mark.size[0]/2+25,10

            x_marker_surface.blit(mark, pos)
        
        surface.blit(x_marker_surface, (self.pos[0]-25,self.pos[1]+self.height))
    
    def update(self, num=None):
        self.surface.fill(colors['bg'])
        self.total_points +=1
        # the specific code that adds a new y value in the data set

        # random
        # self.y_vals = np.append(self.y_vals, random.randrange(-self.max_view_height, int(self.max_view_height/10), int(self.max_view_height/1000)))
        # self.y_vals = np.append(self.y_vals, self.max_view_height if (random.randint(0,1) == 0) else -self.max_view_height)

        # from market
        self.y_vals = np.append(self.y_vals, num)
      
        # maxes out the number of points to draw 
        # if len(self.y_vals) >= self.max_amt:
        #     self.y_vals = self.y_vals[:-(self.max_amt+1):-1][::-1]
        if len(self.y_vals) >= self.max_view_length:
            self.y_vals = self.y_vals[:-(self.max_view_length+1):-1][::-1]        


    def draw(self, color):
        ''' 
        y_vals must be of ndarray format
        '''
        self.filter_y_vals = self.y_vals[:-(self.view_length+1):-1][::-1]
        self.x_vals = np.linspace(0, int(self.width), len(self.filter_y_vals))

        pygame.draw.line(self.surface, colors['ui'], (0, self.convert_point(self.height/2)), (self.width, self.convert_point(self.height/2)))

        self.processed_vals = self.convert_point(self.filter_y_vals)
        
        points = np.column_stack((self.x_vals, self.processed_vals))
        
        pygame.draw.lines(self.surface, color, False, points, width=3)

        # print(self.y_vals)
    
    def scale_y(self, zom):

        # Occam's Razor 😮

        # self.surface.fill(colors['bg'])        
        # if (self.view_height >= 0) and (self.view_height <= self.max_view_height):
        #     self.view_height += (zom * self.max_view_height/100)
        #     self.zoom = self.height/self.view_height
        #     print(1)
        # elif self.view_height < 0 :
        #     self.view_height = self.max_view_height/100
        #     print(2)
        # elif self.view_height > self.max_view_height:
        #     self.view_height = self.max_view_height - self.max_view_height/100
        #     print(3)
        self.surface.fill(colors['bg'])        
        self.view_height += (zom * self.max_view_height/100)
        self.zoom = self.height/self.view_height

    def scale_x(self, zom):
        self.surface.fill(colors['bg'])
        self.view_length += zom

        # Incorporated lapaw error catching conditionals into keybind conditionals instead

        # if 5 < self.view_length < self.max_view_length:
        #     self.view_length += zom
        # elif self.view_length == 5 and zom > 0:
        #     self.view_length += zom
        # elif self.view_length == 51 and zom < 0:
        #     self.view_length -= 1

    def translate(self, val):
        self.surface.fill(colors['bg'])
        self.translation += val * (self.view_height)/10