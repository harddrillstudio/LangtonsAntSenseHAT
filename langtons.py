from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from enum import Enum
import time
import random

sense = SenseHat()
sense.low_light = False
sense.clear()


class Direction(Enum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3
    
    
Colors = {
    "anter": [255, 255, 255],
    "black": {
        "color": [0, 0, 0],
        "turn": "left",
        "next": "white"
    },
    "white": {
        "color": [50, 50, 50],
        "turn": "right",
        "next": "red"
    },
    "red": {
        "color": [50, 0, 0],
        "turn": "right",
        "next": "blue"
    },
    "blue": {
        "color": [0, 0, 50],
        "turn": "left",
        "next": "green"
    },
    "green": {
        "color": [0, 50, 0],
        "turn": "left",
        "next": "purple"
    },
    "purple": {
        "color": [50, 0, 50],
        "turn": "right",
        "next": "black"
    }
}

class Ant:
    def __init__(self, x=3, y=3):
        self.x = x
        self.y = y
        self.dir = Direction.RIGHT.value
    
    def turn_right(self):
        self.dir -= 1
        if self.dir < 0:
            self.dir += 4
        
    def turn_left(self):
        self.dir += 1
        self.dir %= 4
    
    def forward(self):
        if self.dir == Direction.RIGHT.value:
            self.x += 1
        elif self.dir == Direction.UP.value:
            self.y += 1
        elif self.dir == Direction.LEFT.value:
            self.x -= 1
        elif self.dir == Direction.DOWN.value:
            self.y -= 1
    
    def move(self, matrix):
        current = matrix.matrix[self.x][self.y]
        
        if current["turn"] == "left":
            self.turn_left()
            
        if current["turn"] == "right":
            self.turn_right()
        
        matrix.matrix[self.x][self.y] = Colors[current["next"]]
            
        #if current == Colors['0']:
            #self.turn_left()
            #matrix.matrix[self.x][self.y] = Colors['1']
            
        #if current == Colors['1']:
            #self.turn_right()
            #matrix.matrix[self.x][self.y] = Colors['0']
            
        self.forward()
        
        self.x = (self.x + 8) % 8
        self.y = (self.y + 8) % 8
        
        
    def __str__(self):
        return "{} {} {}".format(self.x, self.y, Direction(self.dir).name)
    

class Matrix:
    matrix = [[0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0]]
    
    def __init__(self):
        for y in range(8):
            for x in range(8):
                self.matrix[x][y] = Colors['black']
                
    def restart(self):
        for y in range(8):
            for x in range(8):
                self.matrix[x][y] = Colors['black']

    def render(self):
        matrix_1d = [j["color"] for cols in self.matrix for j in cols]
        sense.set_pixels(matrix_1d)
        #for y in range(8):
            #for x in range(8):
                #sense.set_pixel(x, y, self.matrix[x][y])
                
    def render_ant(self, ant):
        sense.set_pixel(ant.y, ant.x, Colors["anter"])
    
    def turn(self, x, y, color):
        self.matrix[x][y] = color

    def __str__(self):
        to_print = ""
        for y in range(8):
            for x in range(8):
                to_print += "{}, ".format(self.matrix[x][y]["color"])
            to_print += "\n"
        return to_print
            

ant = Ant(4, 4)

matrix = Matrix()
print(matrix)


timeout = 0.1

def pushed_left(event):
    if event.action != ACTION_RELEASED:
        global timeout
        timeout *= 1.2

def pushed_right(event):
    if event.action != ACTION_RELEASED:
        global timeout
        timeout *= 0.8
    
def pushed_up(event):
    if event.action != ACTION_RELEASED:
        global matrix
        matrix.restart()
        
def pushed_down(event):
    if event.action != ACTION_RELEASED:
        global Colors
        Colors["anter"] = [random.randint(0, 255) for x in range(3)]
    
sense.stick.direction_left = pushed_left
sense.stick.direction_right = pushed_right
sense.stick.direction_up = pushed_up
sense.stick.direction_down = pushed_down

while True:
    #print(ant)
      
    matrix.render()
    matrix.render_ant(ant)
    
    #Colors["anter"] = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
    
    time.sleep(timeout)
    ant.move(matrix)
