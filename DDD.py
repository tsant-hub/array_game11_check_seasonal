''' 
prototypr idea #1 for math 154 fproj 

source for 3d model: https://github.com/alecjacobson/common-3d-test-models/blob/master/data/rocker-arm.obj
'''
import pygame, random, os, sys, math
import numpy as np 
import sympy as sp
from defaults import *
from convert import *

pygame.init()

window = pygame.display.set_mode((scrx, scry))
pygame.clock = pygame.time.Clock()
pygame.display.set_caption('Prototype Game')

# 5 for dots
# 25 for water color effect
size = 25
       
# p = (x,y)
def point(p,color,surf):
    pygame.draw.rect(surf, (color[0],color[1],color[2]), ((p[0]-size/2,p[1]-size/2),(size,size)))
    # pygame.draw.circle(window, (color[0],color[1],color[2]), (p[0]-size/2,p[1]-size/2),size)

def screen(p):
    point = ((p[0] + 1)/2 * scrx, (1-(p[1] + 1)/2) * scry)
    return point 

def project(p3d):
    point_3d = (p3d[0]/p3d[2], p3d[1]/p3d[2])
    return point_3d
    

def translate_x(p3d, dx):
    point_3d = (p3d[0] + dx, p3d[1], p3d[2])
    return point_3d

def translate_z(p3d, dz):
    point_3d = (p3d[0], p3d[1], p3d[2] + dz)
    return point_3d


def rotate_xz(p3d, angle):
    point_3d = (
        p3d[0]*math.cos(angle) - p3d[2]*math.sin(angle),
        p3d[1],
        p3d[0]*math.sin(angle) + p3d[2]*math.cos(angle),
    )
    return point_3d

def rotate_yz(p3d,angle):
    point_3d = (
        p3d[0],
        p3d[1]*math.cos(angle) + p3d[2]*math.sin(angle),
        -p3d[1]*math.sin(angle) + p3d[2]*math.cos(angle),
    )
    return point_3d



def line(p1, p2,surf):
    pygame.draw.line(surf, 'white', p1, p2)

# vertices = []

# faces = []
dt = 1/60
dz = 0.01
angle = 0
rotate = 0.7
zoom = 1
def render(surf,zoom,rotate):
    global angle
    # global zoom
    # global rotate
    global vertices
    global faces
    global dz
    global dt

    # render vertices
    for v in vertices:
        # point(screen(project(translate_z(rotate_xz(v, angle),dz))),[255,255,255], surf)
        point(screen(project(translate_z(rotate_xz(v, angle),dz))),[abs(v[0]*255),abs(v[1]*255),abs(v[2]*255)],surf)

    # for f in faces:
    #     for i in range(len(f)):
    #         # print(f)
    #         a = vertices[f[i]]
    #         b = vertices[f[(i+1)%len(f)]]
            
    #         line(screen(project(translate_z(rotate_xz(a, angle),dz))), screen(project(translate_z(rotate_xz(b, angle),dz))),surf)

    # dz += 1 * dt

    if rotate:
        angle += math.pi * dt * rotate/10
    
    if zoom:
        dz += 0.05 * dt * zoom
    
    return dz


def game():
    global dt
    global dz
    global angle
    global rotate
    global zoom
    i = 0
    # pygame.mixer.music.load(os.path.join('assets','audios','truebad_end.mp3'))
    # pygame.mixer.music.set_volume(0.5)
    # pygame.mixer.music.play()

    while True:
        window.fill('black')

        render(window)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()   
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if rotate:
                        rotate = 0
                    else:
                        rotate = 1
                        # axis = 'yz'
                if event.key == pygame.K_s:
                    if rotate:
                        rotate = 0
                    else:
                        rotate = -1
                        # axis = 'yz'
                if event.key == pygame.K_d:
                    if rotate:
                        rotate = 0
                    else:
                        rotate = 1
                        # axis = 'xz'
                if event.key == pygame.K_a:
                    if rotate:
                        rotate = 0
                    else:
                        rotate = -1
                        # axis = 'xz'
                
                if event.key == pygame.K_j:
                    if zoom:
                        zoom = 0
                    else:
                        zoom = 1
                        # axe = 'z'
                if event.key == pygame.K_u:
                    if zoom:
                        zoom = 0
                    else:
                        zoom = -1
                        # axe = 'z'
                if event.key == pygame.K_h:
                    if zoom:
                        zoom = 0
                    else:
                        zoom = 1
                        # axe = 'x'
                if event.key == pygame.K_k:
                    if zoom:
                        zoom = 0
                    else:
                        zoom = -1
                        # axe = 'x'
                    


        pygame.display.update()
        pygame.clock.tick(60)
        pygame.display.set_caption(f'DEATH CAPITAL, INC.      |      (FPS):{round(pygame.clock.get_fps())}')

