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
TILE_24 = (1,0)

SOLID_TILE = [TILE_1, TILE_2, TILE_3, TILE_4, TILE_5, TILE_6, TILE_7, TILE_8, TILE_9, TILE_10, TILE_11, TILE_12, TILE_13, TILE_14, TILE_15, TILE_16, TILE_17, TILE_18, TILE_19, TILE_20, TILE_21, TILE_22, TILE_23, TILE_24 ]

class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vx = 1.5
        self.vy = 1.5
        self.f = 8
        self.mouvement = False

    def get_tile(self,x,y):
        tile_x = x//8
        tile_y = y//8
        return pyxel.tilemaps[0].pget(tile_x,tile_y)

    def tile(self):
        tile_under_left = self.get_tile(self.x + 2, self.y + 8)
        tile_under_right = self.get_tile(self.x + 6, self.y + 8)
        tile_under_middle = self.get_tile(self.x + 4, self.y + 10)
        tile_right = self.get_tile(self.x + 8, self.y + 6)
        tile_left = self.get_tile(self.x - 1, self.y + 6)

    def update(self):
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.f = 8
            self.x += self.vx
        if pyxel.btn(pyxel.KEY_LEFT):
            self.f = -8
            self.x -= self.vx
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= self.vy
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += self.vy

    def draw(self):
        if (pyxel.frame_count // 5) % 2 == 0:
            pyxel.blt(self.x,self.y,0,0,16,self.f,8,2)
        else:
            pyxel.blt(self.x,self.y,0,8,16,self.f,8,2)

class App:
    def __init__(self):
        pyxel.init(128, 128, title="LE JEU DE LA MORT QUI TUE")
        pyxel.load("1.pyxres")
        self.player = Player(50, 50)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()

    def draw(self):
        pyxel.cls(1)
        pyxel.bltm(0,0,0,0,0,256,256)
        self.player.draw()

App()