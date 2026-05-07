'''
trading engine
'''
import pygame, os
import numpy as np
# import pandas as pd
from defaults import *
from utils import *

class Trade():
    def __init__(self, balance):
        # vars
        self.balance = balance
        self.share = 0
        self.value = 1
        self.price = 0
        self.prev_value = 0

        self.bet = 0
        self.power = 0

        # buttons
        self.button_buy = Button((825+70,650-30), (100,50), 'Buy', 'click')
        self.button_sell = Button((825-70,650-30), (100,50), 'Sell', 'click')
        
        self.button_add = Button((915,650-95), (50,50), '+', 'click')
        self.button_min = Button((735,650-95), (50,50), '-', 'click')

        self.button_exp = Button((855,650-95), (50,50), 'x10', 'click')
        self.button_log = Button((795,650-95), (50,50), '/10', 'click')

        self.BUTTONS = np.array([self.button_buy,self.button_sell,self.button_add,self.button_min, self.button_exp, self.button_log])

        self.render_dash = True
        self.render_butt = True


    def render(self, window):
        if self.render_butt:
            for button in self.BUTTONS:
                button.render(window)
        
        if self.render_dash:
            # blits the current bet
            curr_bet = text_dash.render(str(self.bet), False, colors['ui'])
            pos_bet = (700+15,650-165)
            pygame.draw.rect(window, colors['bg_light'], ((pos_bet[0]-10,pos_bet[1]),(curr_bet.width+20,curr_bet.height+5)))
            window.blit(curr_bet, pos_bet)
            # blits the current bet in dollars
            curr_val = text_dash.render(f'${round(self.bet*self.price)}', False, colors['ui'])
            pos_val = (950-15-curr_val.width,650-165)
            pygame.draw.rect(window, colors['bg_light'], ((pos_val[0]-10,pos_val[1]),(curr_val.width+20,curr_val.height+5)))
            window.blit(curr_val, pos_val)
            # blits the current power of 10
            curr_pow = text_dash.render(f'{self.power}',False,colors['text'])
            window.blit(curr_pow, (825-curr_pow.width/2,620-curr_pow.height/2))


            # blits the current balance
            text_bal = text_dash.render(f'Balance: ${self.balance}', False, colors['ui'])
            window.blit(text_bal, (705,305))
            # blits the current share
            text_shr = text_dash.render(f'Shares: {round(self.share)}', False, colors['ui'])
            window.blit(text_shr, (705,305+text_shr.height))
            # blits the current dollar value of share
            text_val = text_dash.render(f'Val: ${self.value}', False, colors['ui'])
            window.blit(text_val, (705,305+text_shr.height+text_val.height))
            # blits the previous dollar value of share
            text_prev = text_dash.render(f'Prev: ${round(self.prev_value)}', False, colors['ui'])
            window.blit(text_prev, (705,305+text_shr.height+text_val.height+text_prev.height))
            # blits the current share price
            text_pri = text_dash.render(f'Price: ${round(self.price)}', False, colors['ui'])
            window.blit(text_pri, (705,305+text_shr.height+text_val.height+text_prev.height+text_pri.height))



    def update(self, price):
        for button in self.BUTTONS:
            button.update()

        self.price = price
        self.value = round(self.price*self.share)

        # bet config
        ''' change bet into stocks '''
        if self.button_add.state:
            self.bet = int(np.round(self.bet))
            new_bet = self.bet + 10**self.power
            if new_bet < 1000:
                self.bet = new_bet
            else:
                self.bet = 1000
        elif self.button_min.state:
            new_bet = self.bet - 10**self.power
            if new_bet < 0:
                self.bet = 0
            else:
                self.bet = new_bet
        elif self.button_exp.state and self.power < 3:
            self.power += 1
        elif self.button_log.state and self.power > 0:
            self.power -= 1

        if self.button_buy.state:
            if self.bet*self.price <= self.balance:
                self.buy(self.bet)
                self.bet = 0
            else:
                self.bet = round(self.balance/self.price)
        elif self.button_sell.state:
            if self.bet*self.price <= self.value:
                self.sell(self.bet)
                self.bet = 0
            else:
                self.bet = round(self.value/self.price)

    # how tf do you buy and sell with shares
    def buy(self, amt):
        self.share+=amt
        self.prev_value=self.price
        self.balance-=self.prev_value*amt


    
    def sell(self, amt):
        self.share-=amt
        self.balance+=amt*self.price
        


