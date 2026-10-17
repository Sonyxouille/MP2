import time
import pyxel

TILE_1 = (4,1)
TILE_2 = (5,0)
TILE_3 = (5,8)
TILE_4 = (6,0)
TILE_5 = (7,0)
TILE_6 = (6,1)
TILE_7 = (7,1)
TILE_8 = (5,2)
TILE_9 = (6,2)
TILE_10 = (7,2)
TILE_11 = (5,3)
TILE_12 = (6,3)
TILE_13 = (7,3)
TILE_14 = (5,4)
TILE_15 = (6,4)
TILE_16 = (7,4)
TILE_17 = (5,5)
TILE_18 = (6,5)
TILE_19 = (7,5)
TILE_20 = (6,6)
TILE_21 = (7,6)
TILE_22 = (6,7)
TILE_23 = (7,7)
TILE_24 = (5,1)

TILE_PLATFORM = (1,0)

SOLID_TILE = [TILE_1, TILE_2, TILE_3, TILE_4, TILE_5, TILE_6, TILE_7, TILE_8, TILE_9, TILE_10, TILE_11, TILE_12, TILE_13, TILE_14, TILE_15, TILE_16, TILE_17, TILE_18, TILE_19, TILE_20, TILE_21, TILE_22, TILE_23, TILE_24, TILE_PLATFORM ]

scroll_x = 0
SCROLL_BORDER = 64

class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vx = 2
        self.vy = 2
        self.f = 8
        self.mouvement = False
        self.physics = Physics()
        self.is_on_the_ground = False
        self.touch_a_left_wall = False
        self.touch_a_right_wall = False
        self.jump_force = 6
        self.key_down = 0

    def update(self):
        if pyxel.btn(pyxel.KEY_RIGHT) and self.touch_a_right_wall == False:
            self.f = 8
            self.x += self.vx
        if pyxel.btn(pyxel.KEY_LEFT) and self.touch_a_left_wall == False and self.x > 0:
            self.f = -8
            self.x -= self.vx
        if pyxel.btnp(pyxel.KEY_UP) and self.is_on_the_ground:
            self.is_on_the_ground = False
            self.vy -= self.jump_force

        self.vy += self.physics.gravity
        self.y += self.vy

        if self.physics.is_on_floor(self.x, self.y) and (self.physics.get_tile(self.x + 2, self.y + 8) == TILE_PLATFORM or self.physics.get_tile(self.x + 4, self.y + 8) == TILE_PLATFORM) and pyxel.btnp(pyxel.KEY_DOWN):
            self.is_on_the_ground = False
            self.key_down = time.time()
        elif self.physics.is_on_floor(self.x, self.y) and self.vy >= 0 and (time.time() - self.key_down) > 0.2:
            self.is_on_the_ground = True
            self.vy = 0
            self.y = self.physics.get_tile_y(self.y)
        else:
            self.is_on_the_ground = False
        
        if self.physics.touch_a_left_wall(self.x, self.y):
            self.touch_a_left_wall = True
        else:
            self.touch_a_left_wall = False

        if self.physics.touch_a_right_wall(self.x, self.y):
            self.touch_a_right_wall = True
        else:
            self.touch_a_right_wall = False

        if self.physics.touch_a_ceiling(self.x, self.y):
            self.vy = 0
            self.y += 1

    def draw(self):
        screen_x = self.x - scroll_x
        if (pyxel.frame_count // 5) % 2 == 0:
            pyxel.blt(screen_x,self.y,0,0,16,self.f,8,2)
        else:
            pyxel.blt(screen_x,self.y,0,8,16,self.f,8,2)
        #pyxel.rect(self.x + 2 - scroll_x, self.y - 1,1,1,9)
        #pyxel.rect(self.x + 4 - scroll_x, self.y - 1,1,1,9)
        #pyxel.rect(self.x + 5 - scroll_x, self.y + 8,1,1,9)
        #pyxel.rect(self.x + 3 - scroll_x, self.y + 8,1,1,9)
        #pyxel.rect(self.x + 8 - scroll_x, self.y + 3,1,1,9)
        #pyxel.rect(self.x -1 - scroll_x, self.y + 3,1,1,9)

class Enemy:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vx = 1
        self.f = 8
        self.hp = 100 #HP temporaire
        self.direction = True #False pour gauche, True pour droite
        self.physics = Physics()

    def update(self):
        if self.direction == False:
            self.x -= self.vx
            self.f = -8
        else:
            self.x += self.vx
            self.f = 8

        if self.physics.touch_a_left_wall(self.x, self.y) or self.x < 0:
            self.direction = True
        if self.physics.touch_a_right_wall(self.x, self.y):
            self.direction = False

    def draw(self):
        pyxel.blt(self.x - scroll_x ,self.y,0,0,24,self.f,8,2)


class Physics:
    def __init__(self):
        self.gravity = 0.5

    def get_tile(self,x,y):
        tile_x = x//8
        tile_y = y//8
        if y < 0:
            tile_y = y//-8
            return pyxel.tilemaps[0].pget(tile_x,tile_y)
        return pyxel.tilemaps[0].pget(tile_x,tile_y)
    
    def is_on_floor(self,x,y):
        tile_left = self.get_tile(x + 2, y + 8)
        tile_right = self.get_tile(x + 4, y + 8)
        if tile_left in SOLID_TILE or tile_right in SOLID_TILE:
            return True
        else:
            return False

    def touch_a_left_wall(self,x,y):
        tile_left = self.get_tile(x-1,y)
        if tile_left in SOLID_TILE and not tile_left == TILE_PLATFORM:
            return True
        else:
            return False

    def touch_a_right_wall(self,x,y):
        tile_right = self.get_tile(x+9,y)
        if tile_right in SOLID_TILE and not tile_right == TILE_PLATFORM:
            return True
        else:
            return False
    
    def touch_a_ceiling(self,x,y):
        tile_left = self.get_tile(x + 2, y - 1)
        tile_right = self.get_tile(x + 4, y - 1)
        if tile_left == TILE_PLATFORM or tile_right == TILE_PLATFORM:
            return False
        elif tile_left in SOLID_TILE or tile_right in SOLID_TILE:
            return True
        else:
            return False

    def get_tile_y(self,y):
        tile_y = (y+8) // 8
        floor_y = tile_y * 8
        return floor_y - 8

class App:
    def __init__(self):
        pyxel.init(128, 128, title="LE JEU DE LA MORT QUI TUE")
        pyxel.load("1.pyxres")
        self.map_whidth = 2040
        self.physics = Physics()
        self.player = Player(50, 50)
        self.enemy1 = Enemy(10, 112)
        pyxel.run(self.update, self.draw)

    def update(self):
        global scroll_x
        scroll_x = self.player.x - SCROLL_BORDER
        scroll_x = max(0,min(scroll_x,self.map_whidth-128))
        self.player.update()
        self.enemy1.update()

    def draw(self):
        pyxel.cls(1)
        pyxel.bltm(0,0,0,scroll_x,0,256,256)
        self.player.draw()
        self.enemy1.draw()
        pyxel.text(10,10,f"Player : {self.player.x},{self.player.y}",9)
        tile_x ,tile_y = self.physics.get_tile(self.player.x, self.player.y)
        pyxel.text(10,20,f"tile x,y : {tile_x,tile_y}",9)
        pyxel.text(10,30,f"on floor : {self.physics.is_on_floor(self.player.x,self.player.y)}",9)
App()
