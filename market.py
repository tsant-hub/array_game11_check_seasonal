'''
Market Engine
Description: Handles the market system of the game. Makes use of Geometric Brownian Motion to simulate a stock market base. This base is then modified by random events and player actions (buy/sell, player-controlled events).


NOTES
implement with pure numpy first before graphing with python

potential models:
- trends and seasons
- buyers and sellers
    - buyers set max
    - sellers set min

break down the market into trends and seasons
trend
- cause; end
- direction
- strength
- speed
& variation (added error)

season(al change)
- period
- frequency
- amplitude
& variation (added error)
'''
import random
import matplotlib.pyplot as plt
import numpy as np
from defaults import *
from utils import *

class Trend():
    def __init__(self, direction, strength, speed):
        '''

        '''
        self.a = 'a'

class Season():
    """
    Generalized Sinusoidal Wave Equation used, instead of complex Seasonality formula used to forecast data
    Periodic changes, based on what day it is, used cos function for greater changes in mu in the end and the beginning (winter seasons)
    higher mu = greater yield (from my general understanding of the market)
    Not sure if need to add phase shift from the cosinusoidal wave equation, since if included, mu would change too drastically
    period is probably(?) all we need for the
    reference: https://blog.gopenai.com/sinusoidal-encoding-a-key-concept-for-data-representation-542e5015cd7e
    complex seasonality: https://otexts.com/fpp3/complexseasonality.html
    """
    def __init__(self, period, amplitude):
        self.period = period
        self.amplitude=amplitude
    def Seasonality_Update(self,time):
        season_trend=self.amplitude*np.cos((2*np.pi/self.period)*time)
        return season_trend



# class Event()


# Geometric Brownian Motion model
class Market():
    def __init__(self, initial_price):
        # time horizon has to be premade for this to work

        self.point = 0

        self.time_horizon = 252     # 252 trading days in a year
        self.delta_t = 1
        self.initial_price = initial_price / 10       # accounting for amplification
        self.output = np.array([self.initial_price])
        
        self.mu = 0.30 / self.time_horizon      # % annual yield
        self.sigma = 0.01       # % volatility

        self.test = np.array([self.initial_price])
        self.season=Season(period=63,amplitude=3*(10**-4))
        """
        period=63 since seasons are by quarter in America
        amplitude=3*(10**-4), since generally it would be the value that would affect the mu but not too greatly,
        since mu=0.05/252
        """
        
    def update(self):
        pass

    def gen_points(self):
        #Geometric Brownian Motion + Seasonality
        time=len(self.output) #basically just updates every tick of self.output, linearly added
        add_seasonality=self.season.Seasonality_Update(time)
        new_mu=self.mu+add_seasonality
        self.point = self.output[-1] * np.exp((new_mu - 0.5 * self.sigma ** 2) * self.delta_t + self.sigma * np.sqrt(self.delta_t) * np.random.normal(0,1))
        self.output = np.append(self.output, self.point)
        return (self.point*10)//1      # *100 amplifies the effect of the market
    
    def graph(self):
        plt.plot(self.output*10)
        # plt.show()


# np.random.seed(889571)
# for j in range(100):
#     np.random.seed()
#     market = Market(1000)
#     for i in range(252):
#         market.gen_points()
#     market.graph()

# plt.show()







