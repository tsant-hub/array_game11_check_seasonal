'''
Utilities Module
Description: For handling the back-end functions and utilities
'''
from multiprocessing.synchronize import Event
from pygame.font import Font

import pygame, os
import numpy as np
import pandas as pd
from defaults import *


pygame.init()

# text initialization
text_main: Font = pygame.font.Font(filename=os.path.join('assets','fonts','vt323-latin-400-normal.ttf'), size=42)
text_viewui = pygame.font.Font(os.path.join('assets','fonts','vt323-latin-400-normal.ttf'), size=24)
text_button: Font = pygame.font.Font(filename=os.path.join('assets','fonts','vt323-latin-400-normal.ttf'), size=32)
text_dash: Font = pygame.font.Font(filename=os.path.join('assets','fonts','vt323-latin-400-normal.ttf'), size=32)
text_end: Font = pygame.font.Font(filename=os.path.join('assets','fonts','vt323-latin-400-normal.ttf'), size=32)
text_end.align = pygame.FONT_CENTER

# sound effects initialization
sound_news = pygame.mixer.Sound(os.path.join('assets','sounds','news.mp3'))
sound_button = pygame.mixer.Sound(os.path.join('assets','sounds','select_sound.mp3'))
sound_start = pygame.mixer.Sound(os.path.join('assets','sounds','start_game.mp3'))

sound_news.set_volume(0.7)
sound_button.set_volume(0.7)
sound_start.set_volume(0.7)


# csv files
# get the csv files cleared
if os.path.exists(os.path.join('data','event_history.csv')):
    os.remove(os.path.join('data','event_history.csv'))
f = open(os.path.join('data','event_history.csv'),'w')
f.write('day,name,type,probability,decision,message,duration\n')
f.close()

# log of past events in the game
EVENT_HISTORY = pd.read_csv(os.path.join('data','event_history.csv'))

# adds events to event csv file
def updateCSV():
    EVENT_HISTORY.to_csv(os.path.join('data','event_history.csv'), index=False)
        


''' debugging features '''
def debug_menu(state, window, viewport, market):
    if state:
        window.blit(text_viewui.render(f'Zoom: x{(viewport.view_height-100)/1000}',False, colors['ui']), (scrx/2-viewport.width+25, scry*0.1+50))

        window.blit(text_viewui.render(f'Number of points:{viewport.view_length}', False, colors['ui']), (scrx/2-viewport.width+25, scry*0.1))

        window.blit(text_viewui.render(f'GBM Model Values', False, colors['ui']), (scrx/2-viewport.width+25, scry*0.1+125))
        
        window.blit(text_viewui.render(f'Ann. Yield (mu): {market.mu}', False, colors['ui']), (scrx/2-viewport.width+25, scry*0.1+150))
        window.blit(text_viewui.render(f'Vol.(sigma): {market.sigma}', False, colors['ui']), (scrx/2-viewport.width+25, scry*0.1+175))
        window.blit(text_viewui.render(f'Latest Price Level: {(market.point*10)//1}', False, colors['ui']), (scrx/2-viewport.width+25, scry*0.1+200))

        # window.blit(text_viewui.render(f'Buy: {bet}' if bet>=0 else f'Sell: {-bet}', False, colors['ui']), (scrx/2-viewport.width+25, scry*0.1+225))

        # window.blit(text_viewui.render(f'Bank: ${money}', False, colors['ui']), (scrx/2-viewport.width+25, scry*0.1+250))
        
        # window.blit(text_viewui.render(f'Shares: ${shares}', False, colors['ui']), (scrx/2-viewport.width+25, scry*0.1+275))
    else:
        pass

def show_boundaries(state, window, viewport):
    if state:
        # center
        pygame.draw.circle(window, 'cyan', (scrx/2,scry/2), outline_width)
        
        # margins
        pygame.draw.line(window, 'cyan', (screen_margin, 0), (screen_margin,scry))
        pygame.draw.line(window, 'cyan', (scrx-screen_margin, 0), (scrx-screen_margin,scry))
        pygame.draw.line(window, 'cyan', (0, screen_margin), (scrx, screen_margin))
        pygame.draw.line(window, 'cyan', (0, scry-screen_margin), (scrx, scry-screen_margin))

        # botton partition
        pygame.draw.line(window, 'fuchsia', (50, viewport.pos[1]+viewport.height+35), (viewport.surface.width+viewport.pos[0]+100,viewport.pos[1]+viewport.height+35))
        # right partition
        pygame.draw.line(window, 'fuchsia', (viewport.surface.width+viewport.pos[0]+100,scry/20+15), (viewport.surface.width+viewport.pos[0]+100,scry-50))
        # bottom right partition
        pygame.draw.line(window, 'fuchsia', (viewport.surface.width+viewport.pos[0]+100,305), (scrx-50,305))

    else:
        pass

# base for all buttons
class Button():
    def __init__(self, pos, size, text, mode):
        '''
        Button Class
        Description: The blueprint for button objects in the game. Handles button rendering, update, and logic.
        '''
        self.surface = pygame.Surface(size)
        self.pos = pos
        self.centered_pos = (pos[0]-self.surface.width/2, pos[1]-self.surface.height/2)  # pos is a 2-item list
        self.rect = pygame.Rect((0,0), (self.surface.width, self.surface.height))
        self.text = text_button.render(text, False, colors['text'])
        self.state = False
        self.color = colors['button']
        self.mode = mode    # either hold or click
        
    def render(self, surf):
        '''
        Render Function
        Description: Renders the button to a specified surface with a position specified in the class initialization.
        '''
        self.surface.fill(colors['bg'])
        pygame.draw.rect(self.surface, self.color, self.rect, width=outline_width)
        self.surface.blit(self.text, ((self.surface.width-self.text.width)/2,(self.surface.height-self.text.height)/2))

        surf.blit(self.surface, self.centered_pos)

    def update(self):
        if self.mode == 'click':
            if self.surface.get_rect(center=(self.pos)).collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_just_pressed()[0]:
                sound_button.play()
                self.color = colors['button_pressed']
                self.state = True
            else:
                self.color = colors['button']
                self.state = False
        elif self.mode == 'hold':
            if self.surface.get_rect(center=(self.pos)).collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_just_pressed()[0]:
                self.color = colors['button_pressed']
                self.state = True            
            if pygame.mouse.get_just_released()[0]:
                self.color = colors['button']
                self.state = False

# responisible for the text appearing
class TextBox():
    def __init__(self, pos, size):
        self.size = size
        self.pos = np.array(pos)
        self.surface = pygame.Surface(self.size)
        self.buttons = []
        # self.rect = pygame.Rect(pos,size)
        

    def render(self,window):
        self.surface.fill(colors['bg_light'])
        window.blit(self.surface, self.pos)
        
        for button in self.buttons:
            button.render(window)
        
        
    def update(self):
        for button in self.buttons:
            button.update()

# default window
class Window():
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.surface = pygame.Surface(size)
        self.buttons = []

    def update(self):
        for button in self.buttons:
            button.update()

    def render(self,window):
        window.blit(self.surface, self.pos)

        for button in self.buttons:
            button.render(window)

# newsbox of the game
class NewsBox(TextBox):
    def __init__(self, pos, size):
        TextBox.__init__(self, pos, size)
        
        # button initialize
        self.button_log = Button(self.pos+np.array([self.size[0]-50,self.size[1]-25]), (100,50), 'Log', 'click')
        self.button_scrollup = Button(self.pos+np.array([self.size[0]-25,self.size[1]-75]), (50,50), '^', 'click')
        self.button_scrolldown = Button(self.pos+np.array([self.size[0]-75,self.size[1]-75]), (50,50), 'v', 'click')
        self.button_agree = Button(self.pos+np.array([205,self.size[1]-25]), (100,50), 'Yes', 'click')
        self.button_disagree = Button(self.pos+np.array([380,self.size[1]-25]), (100,50), 'No', 'click')
        self.buttons.extend([self.button_log])
        
        self.evnt = ['','', 100, False, '']
        
        self.message = ''

        # log viewing
        self.view_log = False
        self.entry = 0

        # decision box initialize
        self.decision = None
        


    def update(self, evt):
        for button in self.buttons:
            button.update()
        pass
        
        self.evnt = evt

        # view log logic
        if self.view_log:
            self.button_scrollup.update()
            self.button_scrolldown.update()
        
        if self.button_log.state and not self.view_log:
            self.view_log = True
        elif self.button_log.state and self.view_log:
            self.bet = 0
            self.view_log = False

        if self.button_scrollup.state and self.entry > 0 and len(EVENT_HISTORY)>4:
            self.entry -= 1
        if self.button_scrolldown.state and len(EVENT_HISTORY)>4:
            self.entry += 1
        
        # for the decision logic
        if self.evnt[3]:
            self.button_agree.update()
            self.button_disagree.update()
        else:
            self.decision = None

        if self.button_agree.state and self.decision == None:
            self.decision = True
        if self.button_disagree.state and self.decision == None:
            self.decision = False

        self.message = text_dash.render(f'{self.evnt[4]}',False, colors['ui'], wraplength=self.size[0]-140)
        


    def render(self,window):
        self.surface.fill(colors['bg_light'])
        
        # header design
        for i in range(4):
            pygame.draw.polygon(self.surface, f'{colors['main']}{4-i%4}', ((50*i,0),(50+50*i,0),(25+50*i,30),(-25+50*i,30)))
           
        for i in range(7):
            pygame.draw.polygon(self.surface, f'{colors['main']}{i%4+1}', ((400+50*i,0),(450+50*i,0),(425+50*i,30),(375+50*i,30)))
            

        if self.view_log:
            # this code handles the event history logs
            latest = np.array(EVENT_HISTORY)[::-1]
        
            if len(latest) > 0:
                for i in range(min(4,len(latest))):
                    if i + self.entry > len(latest) - 1:
                        self.entry = len(latest) - 1-i
                    current = latest[i+self.entry]
                    txt = text_viewui.render(f'{str(current[5])[:40]}',False,colors['ui'],wraplength=self.size[0]-190)
                    dy = text_viewui.render(str(current[0]),False,colors['ui'])
                    
                    self.surface.blit(txt,(100,40+dy.height*i))
                    self.surface.blit(dy,(25,40+dy.height*i))
            else:
                self.surface.blit(text_dash.render('No events as of the moment',False, colors['ui']),(100,40))
        
            self.surface.blit(text_main.render('History',False, colors['main'] if self.message.width>0 else colors['text']), (220,-5))
            
            window.blit(self.surface, self.pos)

            self.button_scrollup.render(window)
            self.button_scrolldown.render(window)
            

        else:
            # if we are not viewing the logs
            self.surface.blit(self.message, (25,40))
            self.surface.blit(text_main.render('Bulletin',False, colors['main'] if self.message.width>0 else colors['text']), (220,-5))
            
            window.blit(self.surface, self.pos)


        # decision making
        if self.evnt[3] and self.decision == None and not self.view_log:
            self.button_agree.render(window)
            self.button_disagree.render(window)
            



        # render the buttons
        for button in self.buttons:
            button.render(window)
    
    def history(self):
        pass

        
        
