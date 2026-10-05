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
        pyxel.blt(self.x,self.y,0,0,8,8,8)

class App:
    def __init__(self):
        pyxel.init(160,120, title="")
        self.player = Player(50,50)
        pyxel.run(self.update, self.draw)
        pyxel.load("1.pyxres")

    def update(self):
        self.player.update()

    def draw(self):
        pyxel.cls(1)
        self.player.draw()

App()