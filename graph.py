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

# blits out the graph of the stock price
class Viewport():
    def __init__(self):
        ''' where the graph blits out on the screen specifically '''
        self.width, self.height = scrx/2,scry/2
        self.pos=((scrx-self.width)/2-150,scrx*0.1)
        self.surface = pygame.Surface((self.width, self.height))
        

        ''' max viewable y-values '''
        self.max_view_height = 10**4
        self.view_height = 2100

        ''' max viewable x-values '''
        self.max_view_length = 251
        self.view_length = 11


        ''' default zoom settings'''
        self.zoom = self.height/self.view_height
        self.interval = 0
        self.total_points = 0
        self.translation = 0
        self.follow = True
        self.y_vals = np.array([0 for i in range(self.max_view_length)])
        self.filter_y_vals = self.y_vals.copy()
        self.x_vals = np.linspace(0, int(self.width), len(self.y_vals))
        self.processed_vals = 0


    ''' follows the the current day point of the graph'''
    def convert_point(self, point):
        if not self.follow:
            mode = self.translation
        else:
            mode = self.y_vals[-1]
        return self.height/2 - ((point-mode) * self.zoom)
    

    ''' '''
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
        
    
        for i in range(0, len(self.x_vals), len(self.x_vals)//10):

            mark = text_viewui.render(f'{self.total_points-i}', False, colors['ui'])
            pos = self.x_vals[-i-1]-mark.size[0]/2+25,10

            x_marker_surface.blit(mark, pos)
        
        surface.blit(x_marker_surface, (self.pos[0]-25,self.pos[1]+self.height))
    
    def update(self, num=None):
        self.surface.fill(colors['bg'])
        self.total_points +=1
        # the specific code that adds a new y value in the data set

        # from market
        self.y_vals = np.append(self.y_vals, num)
      
        # maxes out the number of points to draw 
        # if len(self.y_vals) >= self.max_amt:
        #     self.y_vals = self.y_vals[:-(self.max_amt+1):-1][::-1]
        if len(self.y_vals) >= self.max_view_length:
            self.y_vals = self.y_vals[:-(self.max_view_length+1):-1][::-1]        


    def draw(self, color):

        self.filter_y_vals = self.y_vals[:-(self.view_length+1):-1][::-1]
        self.x_vals = np.linspace(0, int(self.width), len(self.filter_y_vals))

        pygame.draw.line(self.surface, colors['ui'], (0, self.convert_point(0)), (self.width, self.convert_point(0)))

        self.processed_vals = self.convert_point(self.filter_y_vals)
        
        points = np.column_stack((self.x_vals, self.processed_vals))
        
        pygame.draw.lines(self.surface, color, False, points, width=3)

    
    def scale_y(self, zom):
        self.surface.fill(colors['bg'])        
        self.view_height += (zom * self.max_view_height/100)
        self.zoom = self.height/self.view_height

    def scale_x(self, zom):
        self.surface.fill(colors['bg'])
        self.view_length += zom


    def translate(self, val):
        self.surface.fill(colors['bg'])
        self.translation += val * (self.view_height)/10
