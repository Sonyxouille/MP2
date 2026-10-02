import pyxel

class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def update(self):
        self.x = (self.x + 1) % pyxel.width

    def draw(self):
        pyxel.rect(self.x, 0, 8, 8, 9)

class App:
    def __init__(self):
        pyxel.init(160,120)
        self.player = Player(50,50)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()

    def draw(self):
        pyxel.cls(0)
        self.player.draw()

App()