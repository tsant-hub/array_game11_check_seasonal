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
        - coup


'''
import pygame, os
import numpy as np
import pandas as pd
from defaults import *
from utils import *


# Creates and pops up events in the game
class Event():
    def __init__(self, trade, market, newsbox,viewport):
        ''' 
        << Event Documentation here >>>
        Name:
        Description:
        Probability:  most rare must be 1 in 1000
        Trigger Condition:
        End Condition:
        '''
        
        self.trade = trade  # calls a copy of the trade class instance
        self.market = market # calls a copy of the market class instance
        self.newsbox = newsbox # calls a copy of the newsbox class instance
        self.viewport = viewport # calls a copy of the viewport class instance

        # event entry: [name, type, probability, trigger decision(bool), msg text, duration]
        self.events = np.array([
            ['','', 1000, False, '',1],
            ['Market Rise', 'Economy', 100, False, 'Market price is predicted to rise',10],
            ['Market Fall', 'Economy', 100, False, 'Market price is predicted to fall',10],
            ['Market Crash', 'Economy', 50, False, 'Market Crashed',1],
            ['Market Jump', 'Economy', 50, False, 'Market Rised Abruptly',1],
            ['True Bad End', 'Ending', 0, True, 'Begin nuclear annihilation?',2],
            ['Bad End', 'Ending', 0, True, 'Someone is knocking at your door. Do you open?',2],
            ['Good End', 'Ending', 0, True, 'The only way to win is to not play. End the game?',2],
            ['Inheritance', 'Regular', 5, False, 'Your deceased kin left you $100,000!',1],
            ['Pickpocket', 'Regular', 50, False, 'Someone pickpocketed you $1000!',1],
            ['Billiards', 'Regular', 100, True, 'Your friends invite you to billiards.',2],
            ['Bond Yields Fall', 'Economy', 50, False, 'Government bond yields fall, investors flock to invest into stock.',15],
            ['Company Increases Interest Rates', 'Economy', 50, False, 'Company has increased its interest rates to attract investors.',84],
            ['Government Increased Taxes','Economy', 10, False, 'Due to economic downturn, the government increases its taxes permanently.',2],
            ['US Raises Tariffs','Economy', 50, False, 'US Government increases tariffs.', 63],
            ['Death of the CEO', 'Rare', 5, False,'The CEO of the company died.', 42],
            ['Minimum Wage Hike', 'Economy', 10, False, 'The government raised minimum wage. Based on the IS-LM Model, stock prices increase.',1],
             ['Company EPS decreases.', 'Rare', 50, False, 'The company earnings per share decrease based on the income statement.', 126],


            ], dtype='object')

        self.event_list = []

        # default values
        self.weights = 0
        self.day = DAY
        self.end = 0
        self.lock = 0
        self.sin = False

        # base levels to go back to after short-term things
        self.regular_mu = self.market.mu
        self.regular_sigma = self.market.sigma

    ''' back end stuff '''
    def select(self):
        # reinitialize stuff
        if not self.lock:
            self.trade.render_dash = True
            self.trade.render_butt = True
        else:
            self.trade.render_dash = False
            self.trade.render_butt = False
        
        # random selection
        self.weights = list(self.events[:,2].copy()/sum(self.events[:,2]))
        indices = [i for i in range(len(self.events))]
        rng = np.random.choice(indices, p=self.weights)

        # specific event checking
        try:
            numpa_ver = np.array(self.event_list)[:,0]
        except:
            numpa_ver = np.array([])

        check = [0]
        match rng:
            # so that certain events won't be triggered if a certain event is already running
            case 1:
                check.extend([2,3,4])
            case 2:    
                check.extend([1,3,4])
            case 3:
                if self.day < 100:
                    rng = np.random.choice(indices, p=self.weights)
            case 4:
                if self.day < 100:
                    rng = np.random.choice(indices, p=self.weights)
            case 5:
                check.extend([10]) 

        if numpa_ver.size>0: 
            for i in check:
                if i in numpa_ver:
                    rng = np.random.choice(indices, p=self.weights)
        
        # dont repeat events if they are already in the event list
        if self.event_list and rng in numpa_ver:
            return self.select()
        
        if rng > 0:
            # self.invoke(rng)
            EVENT_HISTORY.loc[len(EVENT_HISTORY)] = np.insert(self.events[rng],0, self.day)
            self.event_list.append(np.insert(self.events[rng,5],0,rng))
            sound_news.play()

        return self.events[rng]

    def update(self):
        self.market_level = (self.market.output[-1]*10)//1
        self.event_list = [x for x in self.event_list if x[1] > 0]
        
        # bad end handling
        global money
        if self.trade.balance != money:
            self.sin = True

        ''' ending handling '''
        # true bad end
        if self.day > 1260 and self.trade.balance >= 100000 and (self.lock==0 or self.lock==1):
            self.lock = 1
            self.events[5,2] = 100000000
        # bad end
        if self.day > 1260 and self.trade.balance <= 100000 and (self.lock==0 or self.lock==2):
            self.lock = 2
            self.events[6,2] = 100000000
        if self.day > 1260 and self.sin==False and (self.lock==0 or self.lock==3):
            self.lock = 3
            self.events[7,2] = 100000000
            
            
        # elif self.day > 0  and self.trade.balance 


        for evnt in self.event_list:
            if evnt[1] > 0:
                if self.events[evnt[0]][3]:
                    self.invoke(evnt[0],evnt[1],self.newsbox.decision)
                else:
                    self.invoke(evnt[0],evnt[1])

                evnt[1] -= 1
        #print(self.event_list)





    ''' events framework '''
    # matches event to its respective index on the array above
    def invoke(self, num, remaining, decision=None):
        #print(num)
        match num:
            case 0:
                pass
            case 1:
                self.market_rise(remaining)
            case 2:
                self.market_fall(remaining)
            case 3:
                self.market_crash()
            case 4:
                self.market_jump()
            case 5:
                self.ending_truebad(decision)
            case 6:
                self.ending_bad(decision)
            case 7:
                self.ending_good(decision)
            case 8:
                self.inheritance()
            case 9:
                self.pickpocket()
            case 10:
                self.billiards(decision)        
            case 11:
                self.bonds_fall(remaining)
            case 12:
                self.rates_increase(remaining)
            case 13:
                self.tax_increase()
            case 14:
                self.tariffs_increase(remaining)
            case 15:
                self.founder_death(remaining)
            case 16:
                self.gen_income_increase()
            case 17:
                self.lower_eps(remaining)


    ''' custom events '''

    #events affect default values

    def market_rise(self, remaining):
        ''' 
        Name: Market Rise
        Description: Market price is predicted to rise.
        Probability: 10/1000
        Trigger Condition: By chance. Lessens as you become evil
        End Condition: After 10 days

        DEBUG EVENT
        '''
        self.market.mu += ((self.market.mu)/(remaining) * (self.market_level/1000))
        if remaining <= 1:
            self.market.mu = self.regular_mu

    def market_fall(self, remaining):
        ''' 
        Name: Market Fall
        Description: Market price is predicted to rise.
        Probability: 10/1000
        Trigger Condition: By chance. Lessens as you become evil
        End Condition: After 10 days

        DEBUG EVENT
        '''
        if remaining == 10:
            self.market.mu *= -1
        self.market.mu += ((self.market.mu)/(remaining) * (self.market_level/1000))
         
        if remaining <= 1:
            self.market.mu = abs(self.market.mu)
            self.market.mu = self.regular_mu

    def market_jump(self):
        ''' 
        Name: Market Fall
        Description: Market price is predicted to rise.
        Probability: 10/1000
        Trigger Condition: By chance. Lessens as you become evil
        End Condition: After 10 days

        DEBUG EVENT
        '''
        self.trade.render_dash = False
        self.trade.render_butt = False
        self.market.output[-1] *= 1.7

    def market_crash(self):
        ''' 
        Name: Market Fall
        Description: Market price is predicted to rise.
        Probability: 10/1000
        Trigger Condition: By chance. Lessens as you become evil
        End Condition: After 10 days

        DEBUG EVENT
        '''
        self.trade.render_dash = False
        self.trade.render_butt = False
        self.market.output[-1] *= 0.7

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

    def bonds_fall(self, remaining):
        """
        Name: Bond yields fall
        Description: Government bond yields fall, investors flock to invest into the stock.
        Probability: 50/1000
        Trigger Condition: By chance. Fluctuations depend on the government and how they dictate bond prices.
        End Condition: After 15 days
        """
        self.market.mu = self.regular_mu + 0.00002
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
        if (self.market.output[-1]*10)//1 <= 500:
            self.market.sigma = self.regular_sigma + 0.00015
            self.market.mu = self.regular_mu + 0.00001

            # self.market.sigma += 0.003
            # self.market.mu += ((self.market.mu)/(remaining*100))*1.01
            if remaining <= 0:
                self.market.mu = self.regular_mu
                self.market.sigma = self.regular_sigma


    def tax_increase(self):
        """
        Name: US Government Increase Taxes
        Description: Due to economic downturn, the government increases its taxes permanently.
        Thus, stock interest rates and stock yield decrease.

        Probability: 10/1000
        Trigger Condition: Random. Government decides when tax increases are necessary to fill up treasury.
        End Condition: None. Goes on until the games end (1260 days)
        """
        self.market.mu -= 0.00001
        self.regular_mu -= 0.0001

    def tariffs_increase(self, remaining):
        """
        Name: US Raises Tariffs
        Description: US Government increases tariffs.
        Probability: 50/1000
        Trigger Condition: Random
        End Condition: Ends after 3 working months, 63 days.
        """
        self.market.mu = self.regular_mu - 0.000015
        self.market.sigma = self.regular_sigma + 0.00001
        if remaining<=0:
            self.market.mu = self.regular_mu

    def founder_death(self, remaining):
        """
        Name: Death of the founder.
        Description: The founder of the company died.
        Probability: 5/1000
        Trigger Condition: Random
        End Condition: Ends after 2 working months, 42 days.
        """
        self.market.sigma += 0.0005
        if remaining<=0:
            self.market.sigma = self.regular_sigma

    def gen_income_increase(self):
        """
        Name: Minimum Wage Hike
        Description: The government raised minimum wage. Based on the IS-LM Model, stock prices increase.
                     Increase in money = increase in ivestments = stock prices increase
        Probability: 10/1000
        Trigger Condition: Random.
        """
        self.market.mu += 0.005
        self.regular_mu += 0.005

    def lower_eps(self, remaining):
        """
        Name: Company's EPS decreases.
        Description: The company's earnings per share decrease based on its income statement.
        Probability: 50/1000
        Trigger Condition: Random
        """
        self.market.mu = self.regular_mu - 0.00001
        if remaining<=0:
            self.market.mu = self.regular_mu





    ''' endings '''
    def ending_truebad(self, decision):
        ''' 
        Name: True Bad Ending
        '''
        if decision:
            pygame.mixer.stop()
            self.end = 1
        else:
            self.event_list.pop()
            self.newsbox.decision = None

    def ending_bad(self, decision):
        ''' 
        Name: Bad Ending
        '''
        if decision:
            pygame.mixer.stop()
            self.end = 2
        else:
            self.event_list.pop()
            self.newsbox.decision = None

    def ending_good(self, decision):
        ''' 
        Name: Good Ending
        '''
        if decision:
            pygame.mixer.stop()
            self.end = 3
            
        else:
            self.event_list.pop()
            self.newsbox.decision = None

