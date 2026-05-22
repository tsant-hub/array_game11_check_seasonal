'''
Math 154 Final Project
Group Mayad
Kent Nico Balondro
Josef Vincent Jaen
John Christian Nobleza
TJ Nathan Santillan


BLACK CAPITAL, INC.
A social commentary

Main Module
Description: The main process of the game. Handles player input and pygame backend.
'''
import pygame, random, os, sys
import numpy as np 
import sympy as sp
import convert, DDD
from defaults import *
from utils import *
from graph import *
from trade import *
from market import *
from event import *

#initializes pygame
pygame.init()

window = pygame.display.set_mode((scrx, scry))
pygame.clock = pygame.time.Clock()
pygame.display.set_caption('DEATH CAPITAL, INC.')


# calls all the required classes
viewport = Viewport()
trade = Trade(money)
market = Market(1000)
newsbox = NewsBox((60,viewport.pos[1]+viewport.height+45),(630,150))
phenomena = Event(trade, market, newsbox,viewport)

''' title screen'''
button_start = Button((scrx/2,scry/2),(275,50),'Boot Trading System','click')
button_credits = Button((scrx/2,scry/2+75),(250,50),'System Information','click')
def start():
    '''
    Start Screen Function
    Description: Handles the start screen for the game
    '''
    dots = ''
    while True:
        window.fill(colors['bg'])

        if (viewport.interval - pygame.time.get_ticks()) <= 0:
            viewport.interval = pygame.time.get_ticks() + 500
            dots += '.'
        
        if len(dots) < 4:
            text = text_main.render(f'Logging In{dots}',False,colors['main'])
            window.blit(text, (scrx/2-text.width/2,scry/2-text.height/2))
        else:
            button_start.update()
            button_credits.update()
            if button_start.state:
                sound_start.play()
                return game()
            
            text = text_main.render('DEATH CAPITAL, INC.',False,colors['main'])
            window.blit(text, (scrx/2-text.width/2,scry/2-text.height/2-100))
            button_start.render(window)
            button_credits.render(window)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shut_down()

        pygame.display.update()
        pygame.clock.tick(60)
        pygame.display.set_caption(f'DEATH CAPITAL, INC.      |      (FPS):{round(pygame.clock.get_fps())}')

def credits(surf,color,end_y):
    '''
    Credits Screen Function
    Description: Handles the start screen for the game
    '''
    text = open(os.path.join('assets','credits.txt')).read()
    surface_text = text_end.render(text,False,color, wraplength=scrx-250)
    window.blit(surface_text, (scrx/2-surface_text.width/2,scry-end_y))



def shut_down():
    '''
    Shut Down Function for styllistic exit
    Description: For a styllistic shutting down of the system
    '''
    dots = ''
    pygame.mixer.music.stop()
    while True:
        window.fill(colors['bg'])

        # add credits scene here
        text = text_main.render(f'Shutting Down{dots}',False,colors['main'])
        window.blit(text, (scrx/2-text.width/2,scry/2-text.height/2))

        if (viewport.interval - pygame.time.get_ticks()) <= 0:
            viewport.interval = pygame.time.get_ticks() + 500
            dots += '.'
        
        if len(dots) == 4:
            pygame.quit()   
            market.graph()
            sys.exit()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
                

        pygame.display.update()
        pygame.clock.tick(60)
        pygame.display.set_caption('')


''' endings '''
def truebad_end():
    '''
    True Bad Ending Function
    Description: Handles the true bad ending for the game
    '''
    pygame.mixer.music.load(os.path.join('assets','audios','truebad_end.mp3'))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play()

    end_y = 0
    #for 3d
    rotate = 0.7
    zoom = 0
    while True:
        window.fill(colors['bg'])

        dz = DDD.render(window,zoom,rotate)

        if abs(dz) > 0.05:
            zoom = 0

        if not pygame.mixer.music.get_busy():
            shut_down()
        

        
        # add credits scene here
        credits(window,'white',end_y)
        end_y +=0.5

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shut_down()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if zoom:
                        zoom = 0
                    elif not zoom and dz < 0.050833333333:
                        zoom = 1
                if event.key == pygame.K_s:
                    if zoom:
                        zoom = 0
                    elif not zoom and dz > -0.050833333333:
                        zoom = -1

                if event.key == pygame.K_a:
                    rotate *= -1
                if event.key == pygame.K_d:
                    rotate *= -1



        pygame.display.update()
        pygame.clock.tick(60)
        pygame.display.set_caption(f'DEATH CAPITAL, INC.      |      (FPS):{round(pygame.clock.get_fps())}')

def bad_end():
    '''
    Bad End Function
    Description: Handles the bad end screen for the game
    '''
    pygame.mixer.music.load(os.path.join('assets','audios','bad_end.mp3'))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()

    end_y = 0
    while True:
        window.fill(colors['bg'])

        # add credits scene here
        # text = text_main.render('True Bad End\nDeath Capital Inc.\na Math 154 Final Project by Group Mayad',False,'white')
        # window.blit(text, (scrx/2-text.width/2,scry/2-text.height/2))

        credits(window,colors['main'],end_y)
        end_y+=0.5

        if not pygame.mixer.music.get_busy():
            shut_down()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shut_down()

        pygame.display.update()
        pygame.clock.tick(60)
        pygame.display.set_caption(f'DEATH CAPITAL, INC.      |      (FPS):{round(pygame.clock.get_fps())}')

''' main game'''
def game():
    '''
    Main Game Function
    Description: Handles the main game, calling on pygame backend updates and user input.
    '''
    # for testing purposes
    SEED = np.random.randint(0,1000000)
    np.random.seed(SEED)
    # SEED = np.random.seed(921731)
    print(f'GAME SEED: {SEED}')


    debug_state = False         # ctrl + d
    boundaries_state = False    # ctrl + b
    
    paused = False

    occurence = ['','', 100, False, '']   
    
    #game loop
    while True:
        window.fill(colors['bg'])

        market.update()
        trade.update(viewport.y_vals[-1])
        newsbox.update(occurence)

        # events here happen every update
        if not paused and (viewport.interval - pygame.time.get_ticks()) <= 0:
            # update the viewport
            
            viewport.interval = pygame.time.get_ticks() + interval
            viewport.update(market.gen_points())
            
            
            
            phenomena.day+=1
            occurence = phenomena.select()
            phenomena.update()
            # print(market.mu, phenomena.market.mu, phenomena.regular_mu) #uncomment if wanna see the current state of stock
            updateCSV()

        trade.render(window)
        viewport.draw(colors['main'])
        viewport.render(window)
    
        # logo drawing on top right
        # pygame.draw.rect(window, 'red4', pygame.Rect((700, scry/20+15),((scrx-screen_margin)-700,305-(scry/20+15))))
        # window.blit(text_main.render('LOGO',False,colors['bg']),(((scrx-screen_margin+700)/2,(305)/2)))
        
        # time bar
        if not paused:
            pygame.draw.rect(window, colors['ui'], pygame.Rect((viewport.pos[0], scry/20),((viewport.interval - pygame.time.get_ticks())/(2*interval/1000),10)))
        else:
            pause_text = text_main.render('PAUSED',False,colors['bg'])
            pygame.draw.rect(window, colors['ui'], pygame.Rect((viewport.pos[0], scry/20-pause_text.height/2),(viewport.width,40)))
            window.blit(pause_text, (viewport.pos[0]+viewport.width/2-pause_text.width/2,scry/20-pause_text.height/2-2))
        
        ''' ending check '''
        if not phenomena.end:
            pass
        else:
            match phenomena.end:
                case 1:
                    return truebad_end()
                case 2:
                    return bad_end()
                case 3:
                    pygame.quit()   
                    market.graph()
                    sys.exit()


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
                shut_down()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and not viewport.follow:
                    viewport.translate(1)
                if event.key == pygame.K_s and not viewport.follow:
                    viewport.translate(-1)
            
                # Fixed? zoom scaling
                if event.key == pygame.K_j and viewport.view_height > 100:
                    viewport.scale_y(-10)
                if event.key == pygame.K_k and viewport.view_height < viewport.max_view_height:
                    viewport.scale_y(10)
                # if event.key == pygame.K_j and viewport.view_height > 100:
                #     viewport.scale_y(-1)
                # if event.key == pygame.K_k and viewport.view_height < viewport.max_view_height:
                #     viewport.scale_y(1)

                ''' modify x_scale to account for 252 trading days '''
                # if event.key == pygame.K_u and viewport.view_length > 5:
                #     viewport.scale_x(-5)
                # if event.key == pygame.K_i and viewport.view_length < viewport.max_view_length:
                #     viewport.scale_x(5)
                if event.key == pygame.K_u and viewport.view_length > 11    :
                    viewport.scale_x(-10)
                if event.key == pygame.K_i and viewport.view_length < viewport.max_view_length:
                    viewport.scale_x(10)

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
                    if not paused:
                        paused = True
                    else:
                        paused = False

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
        pygame.display.set_caption(f'DEATH CAPITAL, INC.      |      (FPS):{round(pygame.clock.get_fps())}')

# game()
start()
