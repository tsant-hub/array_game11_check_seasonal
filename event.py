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
<<<<<<< HEAD
import pandas as pd
=======
# import pandas as pd
>>>>>>> 61e33c8e3955fbe40658c44c79757d0367635ade
from defaults import *
from utils import *


class Event():
<<<<<<< HEAD
    def __init__(self, trade, market, newsbox):
=======
    def __init__(self, level):
>>>>>>> 61e33c8e3955fbe40658c44c79757d0367635ade
        ''' 
        << Event Documentation here >>>
        Name:
        Description:
<<<<<<< HEAD
        Probability:  most rare must be 1 in 1000
        Trigger Condition:
        End Condition:
        '''
        # event entry: [name, probability, trigger decision(bool), msg text]
        self.trade = trade  # calls a copy of the trade class instance
        self.market = market
        self.newsbox = newsbox

        self.events = np.array([
            ['','', 100, False, ''],
            ['Inheritance', 'Regular', 50, False, 'Your deceased kin left you $100,000!'],
            ['Pickpocket', 'Regular', 50, False, 'Someone pickpocketed you $1000!'],
            ['Billiards', 'Regular', 50, False, 'Your friends invite you to billiards.'],
        ], dtype='object')

        self.weights = 0
        self.day = DAY

        
    
    def select(self):
        # reinitialize stuff
        self.trade.render_dash = True
        self.trade.render_butt = True
        
        
        # random selection
        self.weights = list(self.events[:,2].copy()/sum(self.events[:,2]))
        indices = [i for i in range(len(self.events))]
        rng = np.random.choice(indices, p=self.weights)

        match rng:
            case 0:
                self.doNothing()
            case 1:
                self.inheritance()
            case 2:
                self.pickpocket()
            case 3:
                self.billiards()
        
        if rng > 0:
            EVENT_HISTORY.loc[len(EVENT_HISTORY)] = np.insert(self.events[rng],0, self.day)

        return self.events[rng]

        



    def doNothing(self):
        pass

    ''' level 1 '''
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

    def billiards(self):
        ''' 
        Name: Billiards
        Description: Your friends invite you to billiards. Will not be able to trade for the next day
        Probability: 50/1000
        Trigger Condition: By chance. Lessens as you become evil
        End Condition: Instantaneous
        '''
        # if self.newsbox.decision == 0:
        self.trade.render_dash = False
        self.trade.render_butt = False


=======
        Trigger Condition:
        End Condition:
        '''
        self.LEVEL = level
>>>>>>> 61e33c8e3955fbe40658c44c79757d0367635ade


