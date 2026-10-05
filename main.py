import pyxel

class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def droite(self):
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 1

    def gauche(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 1

    def monter(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= 1

    def descendre(self):
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += 1

    def mouvement(self):
        self.monter()
        self.descendre()
        self.gauche()
        self.droite()

    def update(self):
        self.mouvement()

    def draw(self):
        pyxel.blt(self.x,self.y,0,0,0,8,8)

class App:
    def __init__(self):
        pyxel.init(160,120, title="")
        self.player = Player(50,50)
        pyxel.run(self.update, self.draw)
        pyxel.load("player.pyxres")

    def update(self):
        self.player.update()

    def draw(self):
        pyxel.cls(1)
        self.player.draw()

App()