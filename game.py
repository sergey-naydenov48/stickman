from tkinter import *
import random
import time

from inspect import currentframe

def getlineno():
    cf = currentframe()
    return cf.f_back.f_lineno

class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("человечек спешит к выходу")
        self.tk.resizable(0, 0)
        # self.tk.wm_attributesb
        self.canvas = Canvas(self.tk, width=500, height=500, \
                            highlightthickness=0)
        self.canvas.pack()
        self.tk.update()
        self.canvas_height = 500
        self.canvas_width = 500
        self.bg = PhotoImage(file="stickman/background.gif")
        w = self.bg.width()
        h = self.bg.height()
        for x in range(0, 5):
            for y in range(0, 5):
                self.canvas.create_image(x * (w + 3), y * (h + 3), \
                        image=self.bg, anchor='nw')
        self.sprites = []
        self.running = True
      
    def mainloop(self):
        while 1:
            if self.running == True:
                for sprite in self.sprites:
                    sprite.move()
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)

class Coords:
    def __init__(self, x1=0, y1=0, x2=0,y2=0) :
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return "Coords(x1=%s, y1=%s, x2=%s, y2=%s)" % ( 
                self.x1, self.y1, self.x2, self.y2)

#def within_x(co1, co2):
#    if (co1.x1 > co2.x1 and co1.x1 < co2.x2) \
#            or (co1.x2 > co2.x1 and co1.x2 < co2.x2) \
#            or (co2.x1 > co1.x1 and co2.x1 < co1.x2) \
#            or (co2.x2 > co1.x1 and co2.x2 < co1.x2):
#        return True
#    else:
#        return False

def between(q, qmin, qmax):
    return qmin <= q and q <= qmax

def within_x(a, b):
    return between(a.x1, b.x1, b.x2) \
           or between(a.x2, b.x1, b.x2) \
           or (a.x1 <= b.x1 and b.x2 <= a.x2)

def within_y(a, b):
    return between(a.y1, b.y1, b.y2) \
           or between(a.y2, b.y1, b.y2) \
           or (a.y1 <= b.y1 and b.y2 <= a.y2)

def collided_left(a, b):
    return within_y(a, b) and (b.x2 >= a.x1 and a.x1 >= b.x1)

def collided_right(co1, co2):
    if within_y(co1, co2):
       if co1.x2 <= co2.x1 and co1.x2 >= co2.x2:
           return True
       return False
       
def collided_top(co1, co2):
    if within_y(co1, co2):
       if co1.y1 <= co2.y2 and co1.y1 >= co2.y1:
           return True
       return False
       
def collided_bottom(y, co1, co2):
    if within_x(co1, co2):
        y_calc = co1.y2 + y
        if y_calc >= co2.y1 and y_calc <= co2.y2:
            return True
    return False
                   
class Sprite:
    def __init__(self, game):
        self.game = game
        self.endgame = False
        self.coordinates = None
    def move(self):
        pass
    def coords(self):
       return self.coordinates
       
class StickFigureSprite(Sprite):
    def __init__(self, game):
        Sprite.__init__(self, game)
        self.images_left = [
            PhotoImage(file="stickman/figure-L1.gif") ,
            PhotoImage(file="stickman/figure-L2.gif") ,
            PhotoImage(file="stickman/figure-L3.gif") 
        ]
        self.images_right = [
            PhotoImage(file="stickman/figure-R1.gif") ,
            PhotoImage(file="stickman/figure-R2.gif") ,
            PhotoImage(file="stickman/figure-R3.gif") 
        ]
        self.image = game.canvas.create_image(200, 470, \
                image=self.images_left[0], anchor='nw')
        self.x = -2
        self.y= 0
        self.current_image = 0
        self.current_image_add = 1
        self.jump_count = 0
        self.last_time = time.time()
        self.coordinates = Coords()
        game.canvas.bind_all('<KeyPress-Left>', self.turn_left)            
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)            
        game.canvas.bind_all('<space>', self.jump)
                 
    def turn_left(self, evt):
        if self.y == 0:
            self.x = -2
                         
    def turn_right(self, evt):
        if self.y == 0:
            self.x = 2
            
    def jump(self, evt):
        if self.y == 0:
            self.y = -4
            self.jump_count = 0 
    
    def animate(self):
        if self.x != 0 and self.y == 0:
            if time.time() - self.last_time > 0.1:
                self.last_time = time.time()
                self.current_image += self.current_image_add
                if self.current_image >= 2:
                    self.current_image_add = -1
                if self.current_image <= 0:
                    self.current_image_add = 1
                    
        if self.x < 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, \
                        image=self.images_left[2])
            else:
                self.game.canvas.itemconfig(self.image, \
                        image=self.images_left[self.current_image])
        elif self.x > 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, \
                        image=self.images_right[2])
            else:
                self.game.canvas.itemconfig(self.image, \
                        image=self.images_right[self.current_image])
              
    def coords(self):
        xy = self.game.canvas.coords(self.image)
        self.coordinates.x1 = xy[0]                            
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0] + 27
        self.coordinates.y2 = xy[1] + 30
        return self.coordinates
        
    def move(self) :
        self.animate()
        if self.y < 0:
            self.jump_count += 1
            print("jump_count=", self.jump_count)
            if self.jump_count > 20:
                self.y = 4
                print('line=', getlineno())
        if self.y > 0:
            self.jump_count -= 1
        co = self.coords()
        left = True
        right = True
        top = True
        bottom = True
        falling = True
        if self.y > 0 and co.y2 >= self.game.canvas_height:
            self.y = 0
            print("canvas_h=%d, co=%s" % (self.game.canvas_height, co))
            print('line=', getlineno())
            bottom = False
        elif self.y < 0 and co.y1 <= 0:
            self.y = 0
            print('line=', getlineno())
            top = False
        
        for sprite in self.game.sprites:
            if sprite == self:
                continue
            sprite_co = sprite.coords()
            if top and self.y < 0 and collided_top(co, sprite_co) :
                self.y = -self.y
                print("co=%s sprite_co=%s" % (co, sprite_co))
                print('line=', getlineno())
                top = False
            if bottom and self.y > 0 and collided_bottom(self.y, \
                    co, sprite_co):
                self.y = sprite_co.y1 - co.y2
                print('line=', getlineno())
                if self.y < 0:
                    self.y = 0
                    print('line=', getlineno())
                bottom = False
                top = False
            if bottom and falling and self.y == 0 \
                    and co.y2 < self.game.canvas_height \
                    and collided_bottom(1, co, sprite_co) :
                falling = False                                
            if left and self.x < 0 and collided_left(co, sprite_co):
                    self.x = 0
                    left = False
                    if sprite.endgame:
                        self.game.running = False
            if right and self.x > 0 and collided_right(co, sprite_co):
                    slef.x = 0
                    right = False
                    if sprite.endgame:
                        self.game.running = False

        if falling and bottom and self.y == 0 \
               and co.y2 < self.game.canvas_height:
            self.y = 4
            print('line=', getlineno())
        self.game.canvas.move(self.image, self.x, self.y)                                                        

class PlatformSprite(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, \
                image=self.photo_image, anchor='nw')
        self.coordinates = Coords(x, y, x + width, y + height)
        
class DoorSprite(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, \
                image=self.photo_image, anchor='nw')
        self.coordinates = Coords(x, y, x + (width / 2), y + height)
        self.endgame = True                
             
             
g = Game()
platform1 = PlatformSprite(g, PhotoImage(file="stickman/platform1.gif"), \
      0, 480, 100, 10)
platform2 = PlatformSprite(g, PhotoImage(file="stickman/platform1.gif"), \
      150, 440, 100, 10)
platform3 = PlatformSprite(g, PhotoImage(file="stickman/platform1.gif"), \
      300, 400, 100, 10)
platform4 = PlatformSprite(g, PhotoImage(file="stickman/platform1.gif"), \
      300, 160, 100, 10)      
platform5 = PlatformSprite(g, PhotoImage(file="stickman/platform2.gif"), \
      175, 350, 66, 10)      
platform6 = PlatformSprite(g, PhotoImage(file="stickman/platform2.gif"), \
      50, 300, 66, 10)      
platform7 = PlatformSprite(g, PhotoImage(file="stickman/platform2.gif"), \
      170, 120, 66, 10)      
platform8 = PlatformSprite(g, PhotoImage(file="stickman/platform2.gif"), \
      45, 60, 66, 10)      
platform9 = PlatformSprite(g, PhotoImage(file="stickman/platform3.gif"), \
      170, 250, 32, 10)      
platform10 = PlatformSprite(g, PhotoImage(file="stickman/platform3.gif"), \
      230, 200, 32, 10)      
      
            
g.sprites.append(platform1)
g.sprites.append(platform2)
g.sprites.append(platform3)
g.sprites.append(platform4)
g.sprites.append(platform5)
g.sprites.append(platform6)
g.sprites.append(platform7)
g.sprites.append(platform8)
g.sprites.append(platform9)
g.sprites.append(platform10)
door = DoorSprite(g, PhotoImage(file="stickman/door1.gif"), 45, 30, 40, 35)
g.sprites.append(door)      
sf = StickFigureSprite(g)
g.sprites.append(sf)      
      
g.mainloop()           
