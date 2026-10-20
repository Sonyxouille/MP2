import time
import pyxel

#TILE MAP DE BASE
TILE_1 = (5,0)
TILE_2 = (6,0)
TILE_3 = (7,0)
TILE_4 = (4,1)
TILE_5 = (5,1)
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

TILE_PLATFORM = (1,0)

#TILE GROTTE
TILE_24 = (0,9)
TILE_25 = (1,9)
TILE_26 = (2,9)
TILE_27 = (3,9)
TILE_28 = (4,9)
TILE_29 = (5,9)
TILE_30 = (6,9)
TILE_31 = (4,11)
TILE_32 = (5,11)

#TILE ITEM
TILE_PIECE_JAUNE = (2,1)

SOLID_TILE = [TILE_PLATFORM, TILE_1, TILE_2, TILE_3, TILE_4, TILE_5, TILE_6, TILE_7,
              TILE_8, TILE_9, TILE_10, TILE_11, TILE_12, TILE_13, TILE_14, TILE_15,
              TILE_16, TILE_17, TILE_18, TILE_19, TILE_20, TILE_21, TILE_22, TILE_23,
              TILE_24, TILE_25, TILE_26, TILE_27, TILE_28, TILE_29, TILE_30, TILE_31,
              TILE_32]

ITEM_TILE = [TILE_PIECE_JAUNE]

ETAGES = [("Map de base", 0, 2040,(50,50)), ("Grotte", 256, 512,(50,352)), ("Grotte Eboulement 1", 384, 512,(50,480)),
          ("Grotte Eboulement 2", 512, 512,(50,608)), ("Grotte Eboulement 3", 640, 512,(70,736)), ("Grotte Eboulement 4", 768, 512,(70,848)),
          ("Grotte Eboulement 5", 896, 512,(72,976))] #0 : nom de l'étage, 1 : map_height, 2 : map_width, 3 : (spawn_x, spawn_y)

scroll_y = 0
scroll_x = 0
SCROLL_BORDER = 64

enemies = []

class Player:
    def __init__(self,x,y):
        self.etage_actuel = 0
        self.x = x
        self.y = y
        self.vx = 2
        self.vy = 2
        self.f = 8
        self.jump_force = 6
        self.key_down = 0
        self.time_invincible = 0
        self.hp = 100
        self.max_hp = 100
        self.spawn_x = ETAGES[self.etage_actuel][3][0]
        self.spawn_y = ETAGES[self.etage_actuel][3][1]
        self.physics = Physics()
        self.healthbar = HealthBar(self.x,self.y,self.max_hp,self.hp)
        self.is_on_the_ground = False
        self.touch_a_left_wall = False
        self.touch_a_right_wall = False
        self.invincible = False
        self.flappy_bird = False

    def invincible_timer(self):
        self.invincible = True
        return time.time()

    def take_damage(self):
        self.hp -= 10
        self.vy -= self.jump_force

    def update(self):
        if self.flappy_bird == False:
            if pyxel.btn(pyxel.KEY_RIGHT) and self.touch_a_right_wall == False:
                self.f = 8
                self.x += self.vx
            if pyxel.btn(pyxel.KEY_LEFT) and self.touch_a_left_wall == False and self.x > 0:
                self.f = -8
                self.x -= self.vx
            if pyxel.btnp(pyxel.KEY_UP) and self.is_on_the_ground:
                self.is_on_the_ground = False
                self.vy -= self.jump_force
        elif self.flappy_bird == True:
            self.f = 8
            if self.touch_a_right_wall == False:
                self.x += self.vx
            if pyxel.btnp(pyxel.KEY_UP):
                self.vy = -self.jump_force
            

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

        for enemy in enemies:
            #if self.invincible == False:
                if enemy.check_collision(self.x, self.y, self.vy) == True:
                    self.vy = -self.jump_force
                    enemy.take_damage(self.vy)
                elif enemy.check_collision(self.x, self.y, self.vy) == False and self.invincible == False:
                    self.take_damage()
                    self.time_invincible = self.invincible_timer()

        if (time.time() - self.time_invincible) > 0.5:
            self.invincible = False

        self.healthbar.update(self.x,self.y,self.max_hp,self.hp)
        if self.hp <= 0:
            print("Game Over")  
            pyxel.quit()    

        if self.spawn_y != ETAGES[self.etage_actuel][3][1]:
            self.spawn_x = ETAGES[self.etage_actuel][3][0]
            self.spawn_y = ETAGES[self.etage_actuel][3][1]
            self.x = self.spawn_x
            self.y = self.spawn_y

        if self.y >= (120 + ETAGES[self.etage_actuel][1]):
                    self.take_damage()
                    self.vy = 0
                    self.x = self.spawn_x
                    self.y = self.spawn_y

    def draw(self):
        screen_x = self.x - scroll_x
        screen_y = self.y - scroll_y
        if self.flappy_bird == False:
            if self.invincible == False:
                if (pyxel.frame_count // 5) % 2 == 0:
                    pyxel.blt(screen_x,screen_y,0,0,16,self.f,8,2)
                else:
                    pyxel.blt(screen_x,screen_y,0,8,16,self.f,8,2)
            else:
                if (pyxel.frame_count // 5) % 2 == 0:
                    pyxel.dither(0.5)
                    pyxel.blt(screen_x,screen_y,0,0,16,self.f,8,2)
                    pyxel.dither(1)
                else:
                    pyxel.blt(screen_x,screen_y,0,8,16,self.f,8,2)
        elif self.flappy_bird == True:
            if (pyxel.frame_count // 5) % 2 == 0:
                pyxel.blt(screen_x, screen_y, 0, 16, 16, self.f, 8, 2)
            else:
                pyxel.blt(screen_x, screen_y, 0, 24, 16, self.f, 8, 2)
        if self.hp < self.max_hp:
            self.healthbar.draw()

class Enemy:
    def __init__(self,x,y,hp,vx=1):
        self.x = x
        self.y = y
        self.vx = vx
        self.f = 8
        self.hp = hp
        self.max_hp = self.hp
        self.direction = True #False pour gauche, True pour droite
        self.physics = Physics()
        self.healthbar = HealthBar(self.x,self.y,self.max_hp,self.hp)

    def take_damage(self,vy):
        if vy < 0:
            self.hp -= 10 * -vy // 2
        elif vy > 0:
            self.hp -= 10 * vy // 2

    def check_collision(self,x,y,vy):
        if (x < self.x + 8 and x + 8 > self.x and y < self.y + 8 and y + 8 > self.y) and self.hp > 0:
            if vy > 0 and y + 8 <= self.y + 4:
                return True
            else:
                return False

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

        self.healthbar.update(self.x,self.y,self.max_hp,self.hp)

    def draw(self):
        if self.hp > 0:
            pyxel.blt(self.x - scroll_x ,self.y - scroll_y,0,0,24,self.f,8,2)
        if self.hp > 0 and self.hp < self.max_hp:
            self.healthbar.draw()

class HealthBar:
    def __init__(self,x,y,max_hp,current_hp):
        self.x = x
        self.y = y
        self.max_hp = max_hp
        self.current_hp = current_hp

    def update(self,x,y,max_hp,current_hp):
        self.x = x
        self.y = y
        self.max_hp = max_hp
        self.current_hp = current_hp

    def draw(self):
        pyxel.rect(self.x - scroll_x, self.y - 2 - scroll_y,8,1,0)
        pyxel.rect(self.x - scroll_x, self.y - 2 - scroll_y,(self.current_hp/self.max_hp)*8,1,7)

class Physics:
    def __init__(self):
        self.gravity = 0.5

    def get_tile(self,x,y):
        tile_x = x//8
        tile_y = y//8
        if y < 0:
            tile_y = y//-8
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

class TakeItems:
    def __init__(self):
        pass

    def check_item(self,x,y,player):
        tile_x = x//8
        tile_y = y//8
        if y < 0:
            tile_y = y//-8
        if pyxel.tilemaps[0].pget(tile_x,tile_y) == TILE_PIECE_JAUNE:
            pass

class Creatif:
    def __init__(self):
        self.active = False
        self.selectionne = 0
        self.choix_menu = 0
        self.page = "menu"
        self.options = ["Modifier le perso", "Placer un ennemi", "Modifier les tiles"]
        self.choix_stat = 0
        self.stats_perso = [("hp", 10), ("max_hp", 10), ("vx", 1), ("jump_force", 1), ("flappy_bird", False), ("etage_actuel", 1)]
        self.choix_stat_ennemi = 0
        self.stats_ennemi = [("hp", 10), ("vx", 1)]
        self.valeurs_ennemi = {"hp": 100, "vx": 1}

    def on_off(self):
        self.active = not self.active
        self.page = "menu"
        pyxel.mouse(self.active)

    def update(self, player):
        if pyxel.btnp(pyxel.KEY_TAB):
            self.page = "menu"
        if self.page == "menu":
            self.update_menu()
        elif self.page == "tiles":
            self.update_tiles(player)
        elif self.page == "perso":
            self.update_perso(player)
        elif self.page == "ennemi":
            self.update_ennemi()

    def update_perso(self, player):
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.choix_stat = (self.choix_stat + 1) % len(self.stats_perso)
        if pyxel.btnp(pyxel.KEY_UP):
            self.choix_stat = (self.choix_stat - 1) % len(self.stats_perso)

        variable, pas = self.stats_perso[self.choix_stat]
        if type(getattr(player, variable)) == int:
            if pyxel.btnp(pyxel.KEY_RIGHT, 10, 3):
                setattr(player, variable, getattr(player, variable) + pas)
            if pyxel.btnp(pyxel.KEY_LEFT, 10, 3):
                setattr(player, variable, max(0, getattr(player, variable) - pas))
        elif type(getattr(player, variable)) == bool:
            if pyxel.btnp(pyxel.KEY_RIGHT):
                setattr(player, variable, True)
            if pyxel.btnp(pyxel.KEY_LEFT):
                setattr(player, variable, False)
        player.hp = max(1,min(player.hp, player.max_hp))
        player.max_hp = max(1,player.max_hp)
        player.etage_actuel = min(player.etage_actuel, len(ETAGES) - 1)

    def draw_perso(self, player):
        pyxel.rect(14, 30, 100, 60, 0)
        pyxel.rectb(14, 30, 100, 60, 10)
        
        affichage_max = 5
        debut = max(0, self.choix_stat - affichage_max + 1)
        fin = min(debut + affichage_max, len(self.stats_perso))

        for i in range(debut, fin):
            nom = self.stats_perso[i][0]
            if i == self.choix_stat:
                couleur = 10
            else:
                couleur = 7
            pyxel.text(20, 38 + (i - debut) * 10, f"{nom} : {getattr(player, nom)}", couleur)

        if len(self.stats_perso) > affichage_max:
            h_barre = 52
            taille = h_barre * affichage_max // len(self.stats_perso)
            position = h_barre * debut // len(self.stats_perso)
            pyxel.rect(108, 34, 2, h_barre, 5)
            pyxel.rect(108, 34 + position, 2, taille + 1, 10)

    def update_ennemi(self):
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.choix_stat_ennemi = (self.choix_stat_ennemi + 1) % len(self.stats_ennemi)
        if pyxel.btnp(pyxel.KEY_UP):
            self.choix_stat_ennemi = (self.choix_stat_ennemi - 1) % len(self.stats_ennemi)

        variable, pas = self.stats_ennemi[self.choix_stat_ennemi]
        if pyxel.btnp(pyxel.KEY_RIGHT, 10, 3):
            self.valeurs_ennemi[variable] += pas
        if pyxel.btnp(pyxel.KEY_LEFT, 10, 3):
            self.valeurs_ennemi[variable] = max(1, self.valeurs_ennemi[variable] - pas)

        pos_x = (pyxel.mouse_x + scroll_x) // 8
        pos_y = (pyxel.mouse_y + scroll_y) // 8
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            enemies.append(Enemy(pos_x * 8, pos_y * 8, self.valeurs_ennemi["hp"], self.valeurs_ennemi["vx"]))

    def draw_ennemi(self):
        pos_x = (pyxel.mouse_x + scroll_x) // 8
        pos_y = (pyxel.mouse_y + scroll_y) // 8
        pyxel.rectb(pos_x * 8 - scroll_x, pos_y * 8 - scroll_y, 8, 8, 10)

        pyxel.rect(14, 30, 100, 30, 0)
        pyxel.rectb(14, 30, 100, 30, 10)
        for i, stat in enumerate(self.stats_ennemi):
            if i == self.choix_stat_ennemi:
                couleur = 10
            else:
                couleur = 7
            pyxel.text(20, 38 + i * 10, f"{stat[0]} : {self.valeurs_ennemi[stat[0]]}", couleur)

    def update_menu(self):
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.choix_menu = (self.choix_menu + 1) % len(self.options)
        if pyxel.btnp(pyxel.KEY_UP):
            self.choix_menu = (self.choix_menu - 1) % len(self.options)
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.page = ["perso", "ennemi", "tiles"][self.choix_menu]

    def draw_menu(self):
        pyxel.rect(14, 30, 100, 50, 0)
        pyxel.rectb(14, 30, 100, 50, 10)
        for i, texte in enumerate(self.options):
            if i == self.choix_menu:
                couleur = 10
            else:
                couleur = 7
            if i == self.choix_menu:
                prefixe = "> "
            else:
                prefixe = "  "
            pyxel.text(20, 38 + i * 12, prefixe + texte, couleur)

    def update_tiles(self,player):
        if pyxel.btn(pyxel.KEY_RIGHT): 
            player.x += 3
        if pyxel.btn(pyxel.KEY_LEFT) and player.x > 0: 
            player.x -= 3
        if pyxel.btn(pyxel.KEY_UP): 
            player.y -= 3
        if pyxel.btn(pyxel.KEY_DOWN): 
            player.y += 3
        player.vy = 0
        self.selectionne = (self.selectionne + pyxel.mouse_wheel) % len(SOLID_TILE)

        pos_x = (pyxel.mouse_x + scroll_x) // 8
        pos_y = (pyxel.mouse_y + scroll_y) // 8
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            pyxel.tilemaps[0].pset(pos_x, pos_y, SOLID_TILE[self.selectionne])
        elif pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT):
            pyxel.tilemaps[0].pset(pos_x, pos_y, (0,0))

    def draw_tiles(self):
        pos_x = (pyxel.mouse_x + scroll_x) // 8
        pos_y = (pyxel.mouse_y + scroll_y) // 8
        pyxel.rectb(pos_x * 8 - scroll_x, pos_y * 8 - scroll_y, 8, 8, 10)

        tile = SOLID_TILE[self.selectionne]
        u = tile[0] * 8
        v = tile[1] * 8

        pyxel.rect(108, 4, 12, 12, 0)
        pyxel.rectb(108, 4, 12, 12, 10)
        pyxel.blt(110, 6, 0, u, v, 8, 8)

        pyxel.text(10, 30, f"Tile : {tile}", 10)

class App:
    def __init__(self):
        pyxel.init(128, 128, title="SUPER ZBOOBI")
        pyxel.load("1.pyxres")
        self.map_width = 0
        self.player = Player(50, 50)
        self.creatif = Creatif()
        self.take_item = TakeItems()
        enemies.append(Enemy(10, 112, 100))
        pyxel.run(self.update, self.draw)

    def update(self):
        global scroll_x, scroll_y
        if pyxel.btnp(pyxel.KEY_F1):
            self.creatif.on_off()
        if self.creatif.active:
            self.creatif.update(self.player)
        else:
            self.player.update()
            for enemy in enemies:
                enemy.update()
        self.take_item.check_item(self.player.x + 8,self.player.y,self.player)
        self.take_item.check_item(self.player.x - 1,self.player.y,self.player)
        self.map_width = ETAGES[self.player.etage_actuel][2]
        scroll_x = self.player.x - SCROLL_BORDER
        scroll_x = max(0, min(scroll_x,self.map_width - 128))
        scroll_y = ETAGES[self.player.etage_actuel][1]

    def draw(self):
        pyxel.cls(1)
        pyxel.bltm(0,0,0,scroll_x,scroll_y,256,256)
        for enemy in enemies:
            enemy.draw()
        pyxel.text(10,10,f"Player : {self.player.x},{self.player.y}",9)
        self.player.healthbar.update(self.player.x, self.player.y, self.player.max_hp, self.player.hp)
        self.player.draw()
        if self.creatif.active:
            if self.creatif.page == "menu":
                self.creatif.draw_menu()
            elif self.creatif.page == "tiles":
                self.creatif.draw_tiles()
            elif self.creatif.page == "perso":
                self.creatif.draw_perso(self.player)
            elif self.creatif.page == "ennemi":
                self.creatif.draw_ennemi()

App()
