'''
Math 154 Final Project
Group Mayad

BLACK CAPITAL, INC.
A social commentary

Main Module
Description: The main process of the game. Handles player input and pygame backend.

NOTES
To do:
[ ] implement the market system
    [/] moving graph
    [ ] add viewport utilities
        [/] zoom and shi
        [ ] make it so that when you zoom in gadamo ang markers
    [/] graph that moves according to principles of the stock market
        [/] the long-term and short-term factorsk
[/] implement player input
    [/] buy and sell mechanic
    [ ] make the buy sell mechanic affect the stock market
[ ] implement events into the game
    [ ] implement a text engine in the game
[ ] basic gameloop
    [/] return the seed from the random module so that pwede mareproduce ang states
    [/] player is able to bet on the stock market
    [ ] events can happen + implementation of potential sources of infos
    [ ] add the possibility to pause the game
[ ] add a title screen
'''
import pygame, random, os, sys
import numpy as np 
import sympy as sp
from defaults import *
from utils import *
from graph import *
from trade import *
from market import *
from event import *

pygame.init()

window = pygame.display.set_mode((scrx, scry))
pygame.clock = pygame.time.Clock()
pygame.display.set_caption('BLACK MARKET')

# for testing purposes
SEED = np.random.randint(0,1000000)
np.random.seed(SEED)
# np.random.seed(266007)
print(f'GAME SEED: {SEED}')

viewport = Viewport()
trade = Trade(money)
market = Market(1000)
<<<<<<< HEAD
newsbox = NewsBox((60,viewport.pos[1]+viewport.height+45),(630,150))

phenomena = Event(trade, market, newsbox)

=======
newsbox = NewsBox((60,viewport.pos[1]+viewport.height+45),(630,145))
>>>>>>> 61e33c8e3955fbe40658c44c79757d0367635ade
def game():
    debug_state = False         # ctrl + d
    boundaries_state = False    # ctrl + b
    
    # add a pause function

    occurence = ['','', 100, False, '']   
    while True:
        window.fill(colors['bg'])
        market.update()
        trade.update(viewport.y_vals[-1])
<<<<<<< HEAD
        newsbox.update(occurence)

=======
        newsbox.update()
>>>>>>> 61e33c8e3955fbe40658c44c79757d0367635ade
        
        trade.render(window)
        viewport.draw(colors['main'])
        viewport.render(window)
        newsbox.render(window)

<<<<<<< HEAD
=======
        
                       
>>>>>>> 61e33c8e3955fbe40658c44c79757d0367635ade

        # logo drawing on top right
        # pygame.draw.rect(window, 'red4', pygame.Rect((700, scry/20+15),((scrx-screen_margin)-700,305-(scry/20+15))))
        # window.blit(text_main.render('LOGO',False,colors['bg']),(((scrx-screen_margin+700)/2,(305)/2)))
        
        # time bar
        pygame.draw.rect(window, colors['ui'], pygame.Rect((viewport.pos[0], scry/20),((viewport.interval - pygame.time.get_ticks())/(2*interval/1000),10)))
    
        # events here happen every update
        if (viewport.interval - pygame.time.get_ticks()) <= 0:
            # update the viewport
            viewport.interval = pygame.time.get_ticks() + interval
            viewport.update(market.gen_points())
            
            
            
            phenomena.day+=1
            occurence = phenomena.select()

            updateCSV()
            

        ''' text printing '''
        com_name = text_main.render('DEATH CAPITAL, INC.',False, colors['main'])
        window.blit(com_name, (viewport.pos[0],viewport.pos[1]-50))

        ''' debug tools '''
        show_boundaries(boundaries_state, window, viewport)
        debug_menu(debug_state, window, viewport, market)
        

        # outline
        pygame.draw.rect(window,colors['main'],pygame.Rect((viewport.pos[0]-outline_width,viewport.pos[1]-outline_width),(viewport.width+2*outline_width,viewport.height+2*outline_width)),width=outline_width) 
        
        newsbox.render(window)      # has to come after the outline drawing


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()   
                market.graph()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and not viewport.follow:
                    viewport.translate(1)
                if event.key == pygame.K_s and not viewport.follow:
                    viewport.translate(-1)
                
                if event.key == pygame.K_d:
                    market.mu += 0.01
                if event.key == pygame.K_a:
                    market.mu -= 0.01
                if event.key == pygame.K_e:
                    market.sigma += 0.001
                if event.key == pygame.K_q:
                    market.sigma -= 0.001
                
                # Corrected the keybinds for the zoom in zoom out of the y axis to match that of the x axis
                # Also simplified the scale_y method

                if event.key == pygame.K_j and viewport.view_height > 1000:
                    viewport.scale_y(-10)
                if event.key == pygame.K_k and viewport.view_height < viewport.max_view_height:
                    viewport.scale_y(10)
                    

                ''' modify x_scale to account for 252 trading days '''
                if event.key == pygame.K_u and viewport.view_length > 5:
                    viewport.scale_x(-5)
                if event.key == pygame.K_i and viewport.view_length < viewport.max_view_length:
                    viewport.scale_x(5)

                if event.key == pygame.K_h:
                    # you can move this code to the viewport class blueprint if you want to make this more organized
                    # add limits
                    if viewport.follow:
                        viewport.translation = viewport.y_vals[-1]
                        viewport.follow = False
                        viewport.surface.fill(colors['bg'])
                    else:
                        viewport.follow = True
                        viewport.surface.fill(colors['bg'])
                
                ''' trading controls '''
                # add trading controls

                ''' time controls '''
                if event.key == pygame.K_SPACE:
                    time_stop = True
                    # phenomena.inheritance()

                # debug tools
                if (event.mod & pygame.KMOD_LCTRL) and (event.key == pygame.K_d):
                    if not debug_state:
                        debug_state = True
                    else:
                        debug_state = False
                if (event.mod & pygame.KMOD_LCTRL) and (event.key == pygame.K_b):
                    if not boundaries_state:
                        boundaries_state = True
                    else:
                        boundaries_state = False
                if event.key == pygame.K_BACKSLASH:
                    print(phenomena.weights)
                    
                    
                
        pygame.display.update()
        pygame.clock.tick(60)
        pygame.display.set_caption(f'BLACK MARKET {pygame.clock.get_fps()}')

game()