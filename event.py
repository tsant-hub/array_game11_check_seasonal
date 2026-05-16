'''
Events Engine

Makes the game not boring!
'''

'''
PLAN

- TECHNICALITIES
    - Event engine handles the event selection, event processing
    - events are subclasses from a parent event class
    - keep all the possible events in a numpy array

- EVENTS
    - ATTRIBUTES
        - level: 1,2, or 3
        - conditions for proc
        - change in mu
        - change in sigma
        - change in player balance
    
    
    - LEVEL 1
        - picked-up cash on the ground
        - relative gave money
        - pickpocket
    - LEVEL 2
        - market rumors
    - LEVEL 3
        - war
        - pandemic
        - cuop


'''
import pygame, os
import numpy as np
import pandas as pd
from defaults import *
from utils import *


class Event():
    def __init__(self, trade, market, newsbox):
        ''' 
        << Event Documentation here >>>
        Name:
        Description:
        Probability:  most rare must be 1 in 1000
        Trigger Condition:
        End Condition:
        '''
        
        self.trade = trade  # calls a copy of the trade class instance
        self.market = market
        self.newsbox = newsbox

        # event entry: [name, type, probability, trigger decision(bool), msg text, duration]
        self.events = np.array([
            ['','', 1000, False, '',1],
            ['Inheritance', 'Regular', 30, False, 'Your deceased kin left you $100,000!',1],
            ['Pickpocket', 'Regular', 50, False, 'Someone pickpocketed you $1000!',1],
            ['Billiards', 'Regular', 200, True, 'Your friends invite you to billiards.',2],
            ['Market Rise', 'Economy', 100, False, 'Market price is predicted to rise',10],
            ['Bond Yields Fall', 'Economy', 50, False, 'Government bond yields fall, investors flock to invest into stock.',15],
            ['Company Increases Interest Rates', 'Economy', 50, False, 'Company has increased its interest rates to attract investors.',84],
            ['Government Increased Taxes','Economy', 10, False, 'Due to economic downturn, the government increases its taxes permanently.',1260],
            ['US Raises Tariffs','Economy', 100, False, 'US Government increases tariffs.', 63],
            ['Death of the Owner', 'Rare', 5, False,'The founder of the company died.', 84]

            ], dtype='object')

        self.event_list = []

        self.weights = 0
        self.day = DAY

        # base levels to go back to after short-term things
        self.regular_mu = self.market.mu
        self.regular_sigma = self.market.sigma

    ''' back end stuff '''
    def select(self):
        # reinitialize stuff
        self.trade.render_dash = True
        self.trade.render_butt = True
        
        # random selection
        self.weights = list(self.events[:,2].copy()/sum(self.events[:,2]))
        indices = [i for i in range(len(self.events))]
        rng = np.random.choice(indices, p=self.weights)
        
        # need to fix vvv para secure nga indi na siya magsulit; cant have two instances of a function running at once
        if self.event_list and rng in self.event_list[:][0]:
            rng = np.random.choice(indices, p=self.weights)
        
        if rng > 0:
            # self.invoke(rng)
            EVENT_HISTORY.loc[len(EVENT_HISTORY)] = np.insert(self.events[rng],0, self.day)
            self.event_list.append(np.insert(self.events[rng,5],0,rng))

        return self.events[rng]

    def update(self):
        self.event_list = [x for x in self.event_list if x[1] > 0]

        for evnt in self.event_list:
            if evnt[1] > 0:
                if self.events[evnt[0]][3]:
                    self.invoke(evnt[0],evnt[1],self.newsbox.decision)
                else:
                    self.invoke(evnt[0],evnt[1])

                evnt[1] -= 1
        print(self.event_list)




    ''' events framework '''
    def invoke(self, num, remaining, decision=None):
        match num:
            case 0:
                pass
            case 1:
                self.inheritance()
            case 2:
                self.pickpocket()
            case 3:
                self.billiards(decision)        
            case 4:
                self.market_rise(remaining)
            case 5:
                self.bonds_fall(remaining)
            case 6:
                self.rates_increase(remaining)
            case 7:
                self.tax_increase()
            case 8:
                self.tariffs_increase(remaining)
            case 9:
                self.founder_death(remaining)

    
    def inheritance(self):
        ''' 
        Name: Inheritance
        Description: You recieved inheritance from your recently deceased kin
        Probability: 50/1000
        Trigger Condition: By chance. Can only happen 4x in a run
        End Condition: Instantaneous
        '''
        self.trade.balance += 100000
    
    def pickpocket(self):
        ''' 
        Name: Pickpocket
        Description: Someone pickpocketed you!
        Probability: 50/1000
        Trigger Condition: By chance.
        End Condition: Instantaneous
        '''
        self.trade.balance -= 1000

    def billiards(self, decision):
        ''' 
        Name: Billiards
        Description: Your friends invite you to billiards. Will not be able to trade for the next day
        Probability: 50/1000
        Trigger Condition: By chance. Lessens as you become evil
        End Condition: Instantaneous
        '''
        if decision:
            self.trade.render_dash = False
            self.trade.render_butt = False

    def market_rise(self, remaining):
        ''' 
        Name: Market Rise
        Description: Market price is predicted to rise.
        Probability: 10/1000
        Trigger Condition: By chance. Lessens as you become evil
        End Condition: After 10 days

        DEBUG EVENT
        '''
        self.market.mu += (self.market.mu)/(remaining*100)
        if remaining <= 0:
            self.market.mu = self.regular_mu

    def bonds_fall(self, remaining):
        """
        Name: Bond yields fall
        Description: Government bond yields fall, investors flock to invest into the stock.
        Probability: 80/1000
        Trigger Condition: By chance. Fluctuations depend on the government and how they dictate bond prices.
        End Condition: After 15 days
        """
        self.market.mu += ((self.market.mu)/(remaining*100))*0.9
        if remaining <= 0:
            self.market.mu = self.regular_mu

    def rates_increase(self, remaining):
        """
        Name: Company Increases Interest Rates
        Description: Company has increased its interest rates to attract investors.
        Probability: 50/1000
        Trigger Condition: Company sees that annual yields are not going so great,
                            decide to increase rates, which affect volatility and annual yield
        End Condition: After 84 days, 4 working months, companies return to original interest rate after a few months
        """
        if self.market.mu<=0.0009:
            self.market.sigma += 0.003
            self.market.mu += ((self.market.mu)/(remaining*100))*1.01
            if remaining <= 0:
                self.market.mu = self.regular_mu
                self.market.sigma = self.regular_sigma


    def tax_increase(self):
        """
        Name: US Government Increase Taxes
        Description: Due to economic downturn, the government increases its taxes permanently.
        Thus, stock interest rates and stock yield decrease.

        Probability: 20/1000
        Trigger Condition: Random. Government decides when tax increases are necessary to fill up treasury.
        End Condition: None. Goes on until the games end (1260 days)
        """

        self.market.mu = self.market.mu-0.0001

    def tariffs_increase(self, remaining):
        """
        Name: US Raises Tariffs
        Description: US Government increases tariffs.
        Probability: 100/1000
        Trigger Condition: Random
        End Condition: Ends after 3 working months, 63 days.
        """

        self.market.mu = self.market.mu-(0.000001*remaining)
        if remaining<=0:
            self.market.mu = self.regular_mu

    def founder_death(self, remaining):
        """
        Name: Death of the founder.
        Description: The founder of the company died.
        Probability: 5/1000
        Trigger Condition: Random
        End Condition: Ends after 4 working months, 84 days.
        """
        self.market.sigma += 0.0005
        if remaining<=0:
            self.market.sigma = self.regular_sigma



