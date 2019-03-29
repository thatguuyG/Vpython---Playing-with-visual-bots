'''
Created on 28 Mar 2019

@author: Aizen
'''

#game that moves a robot along a disk populated by zombies. The robot and the zombies are 3d entities that can move and turn
#The user can move the robot using a graphical User Interface, and the zombies move randomly towards the user's direction
#This program however requires creating a new vpython file inside jupyter noteboook

#here we first of all define all our initial import statements

from vpython import  *
from robot import *
import math
import random
import ipywidgets as widgets
from IPython.core.display import display

#we define the main bot we'll be using 
class MainRobot:
    def __init__(self, position = vector(0, 0, 0),
                 heading = vector(0, 0, 1), speed = 1):
        self.position = position
        self.heading = heading.norm()
        self.speed = speed
        self.parts = []

    def update(self):
        self.turn(0)
        self.forward()

    def turn(self, angle):
        theta = math.radians(angle)#Assumes that all angles are in radians
        self.heading = rotate(self.heading, angle = theta, axis = vector(0, 1, 0))
        for part in self.parts:
            part.rotate(angle = theta, axis = vector(0, 1, 0),#rotates self along its position
                        origin = self.position)

    def forward(self):
        self.position += self.heading * self.speed
        for part in self.parts:
            part.pos += self.heading * self.speed
            
            
class Zombie(MainRobot):#inherits from MainRobot(also inherits its varibales)
    def __init__(self, position = vector(0, 0, 0),
                 heading = vector(0, 0, 1)):
        MainRobot.__init__(self, position, heading)
        self.body = cylinder(pos = self.position,
                             axis = vector(0, 4, 0),
                             radius = 1,
                             color = vector(0, 1, 0))
        self.arm1 = cylinder(pos = self.position + vector(0.6, 3, 0),
                             axis = vector(0, 0, 2),
                             radius = .3,
                             color = vector(1, 1, 0))
        self.arm2 = cylinder(pos = self.position + vector(-0.6, 3, 0),
                             axis = vector(0, 0, 2),
                             radius = .3,
                             color = vector(1, 1, 0))
        self.halo = ring(pos = self.position + vector(0, 5, 0),
                             axis = vector(0, 1, 0),
                             radius = 1,
                             color = vector(1, 1, 0))
        self.head = sphere(pos = self.position + vector(0, 4.5, 0),
                             radius = 0.5,
                             color = vector(1, 1, 1))
        self.parts = [self.body, self.arm1, self.arm2,
                      self.halo, self.head]

    def update(self):
        self.turn(random.uniform(-5, 5))#random angle between -5 and 5
        self.forward()    
                
            
class PlayerBot(MainRobot):
    def __init__(self, position = vector(0, 0, 0),
                 heading = vector(0, 0, 1)):
        MainRobot.__init__(self, position, heading)
        #how the actual user robot would look like. we just use basic shapes
        self.body = cylinder(pos = self.position + vector(0, 0.5, 0),
                               axis = vector(0, 6, 0),
                               radius = 1,
                               color = vector(1, 0, 0))
        self.head = box(pos = vector(0, 7, 0) + self.position,
                               length = 2,
                               width = 2,
                               height = 2,
                               color = vector(0, 1, 0))
        self.nose = cone(pos = vector(0, 7, 1) + self.position,
                               radius = 0.5,
                               axis = vector(0, 0, 1),
                               color = vector(1, 1, 0))
        self.wheel1 = cylinder(pos = self.position + vector(1, 1, 0),
                               axis = vector(0.5, 0, 0),
                               radius = 1,
                               color = vector(0, 0, 1))
        self.wheel2 = cylinder(pos = self.position + vector(-1, 1, 0),
                               axis = vector(-0.5, 0, 0),
                               radius = 1,
                               color = vector(0, 0, 1))
        self.parts = [self.body, self.head, self.nose,
                      self.wheel1, self.wheel2]

    def update(self):
        self.turn(0) 
        self.forward()            
            
            
#After defining all our bots. we build our GUI
###################################################
# variable declarations
global userbot
global running
running = True
GROUND_RADIUS = 50
ZOMBIES = 20

# declare our buttons
fastButton = widgets.Button(description = 'F', width = '60px', height = '60px')
slowButton = widgets.Button(description = 'S', width = '60px', height = '60px')
leftButton = widgets.Button(description = 'L', width = '60px', height = '60px')
rightButton = widgets.Button(description = 'R', width = '60px', height = '60px')
fillerButton0 = widgets.Button(description = '', width = '60px', height = '60px')
resetButton = widgets.Button(description = 'Reset', width = '120px', height = '60px')
quitButton = widgets.Button(description = 'Quit', width = '120px', height = '60px')
fillerButton1 = widgets.Button(description = '', width = '120px', height = '60px')
scene.caption = "To use the directional pad, click on a marked direction. F = Faster, S = Slower, L = turn Left and R = turn Right."

# Readin inputs from our buttons
def fastButton_handler(s):
    global userbot
    userbot.speed += 0.1
fastButton.on_click(fastButton_handler)

def slowButton_handler(s):
    global userbot
    userbot.speed -= 0.1
slowButton.on_click(slowButton_handler)

def leftButton_handler(s):
    global userbot
    userbot.turn(5)
leftButton.on_click(leftButton_handler)

def rightButton_handler(s):
    global userbot
    userbot.turn(-5)
rightButton.on_click(rightButton_handler)

def quitButton_handler(s):
    global running
    running = False
    print("Exiting thE Loop. ENDING SESSION!!")
quitButton.on_click(quitButton_handler)

# now arrange and display our GUI
container0 = widgets.HBox(children = [fillerButton0, fastButton, fillerButton0, quitButton])
container1 = widgets.HBox(children = [leftButton, fillerButton0, rightButton, fillerButton1])
container2 = widgets.HBox(children = [fillerButton0, slowButton, fillerButton0, fillerButton1])
display(container0)
display(container1)
display(container2)

def main():
    global userbot
    global running
    ground = cylinder(pos = vector(0, -1, 0),
                      axis = vector(0, 1, 0),
                      radius = GROUND_RADIUS)
    userbot = PlayerBot()
    zombies = makeZombies()
    while running:
        rate(30)#speed of bots
        userbot.update()
        if mag(userbot.position) >= GROUND_RADIUS:
            userbot.turn(180)
        for z in zombies:
            z.update()
            if mag(z.position) >= GROUND_RADIUS:
                z.turn(random.uniform(150, 210))

def makeZombies():
    zombies = []
    for z in range(ZOMBIES):
        theta = random.uniform(0, 360)
        r = random.uniform(0, GROUND_RADIUS)
        x = r * cos(math.radians(theta))
        z = r * sin(math.radians(theta))
        zombies.append(Zombie(position = vector(x, 0, z)))
    return zombies
main()

