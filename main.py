import pyxel

class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vx = 1
        self.vy = 1
        

    def update(self):
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.vx
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.vx
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= self.vy
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += self.vy

    def draw(self):
        if (pyxel.frame_count // 5) % 2 == 0:
            pyxel.blt(self.x,self.y,0,0,16,8,8,2)
        else:
            pyxel.blt(self.x,self.y,0,8,16,8,8,2)

class App:
    def __init__(self):
        pyxel.init(160, 120, title="LE JEU DE LA MORT QUI TUE")
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