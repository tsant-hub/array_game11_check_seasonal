'''
event class testing
'''
import numpy as np
import pygame,sys

pygame.init()
window = pygame.display.set_mode((500, 500))
pygame.clock = pygame.time.Clock()


thing = 1000

class Event():
    def __init__(self):
        self.events = np.array([
            ['','', 100, False, '',1],
            ['Inheritance', 'Regular', 50, False, 'Your deceased kin left you $100,000!',3]
        ], dtype='object')

        self.event_list = []

        self.day = 0

    def select(self):
        ind = np.random.randint(0,2)

        match ind:
            case 0:
                pass
            case 1:
                self.inheritance()
        self.event_list.append(self.events[ind,::5].copy())


    def update(self):
        indices = []
        for i in range(len(self.event_list)):
            if self.event_list[i][1] > 0:
                self.event_list[i][1] -= 1
            else:
                indices.append(i)
        for i in range(len(indices)):
            self.event_list.pop(indices[i])


        


    def inheritance(self):
        global thing
        thing += 1000

phenomena = Event()

while True:
    phenomena.day += 1
    phenomena.select()
    phenomena.update()
    print(phenomena.event_list)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.quit()   
                sys.exit()
        # if event.type==pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:

    pygame.display.update()
    pygame.clock.tick(1)