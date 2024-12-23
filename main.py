import pyxel
import numpy as np
import time

WINDOW_ASPECT = 1 # 1.33
WINDOW_SCALE = 256
WINDOW_H = int(WINDOW_SCALE * 1)
WINDOW_W = int(WINDOW_SCALE * WINDOW_ASPECT)


LETTER_SHI = (0, 0, 100, 9)

# BOTTLE_BRANDS
MTBD = (16, 72, 30, 30)
IRSAI = (48, 72, 30, 30)
FRAULEIN = (16, 104, 30, 30)
GRANDMONTE = (48, 104, 30, 30)


BGM = 0

SCENE_TITLE = 0
SCENE_DOOR = 1
SCENE_BAR = 2

def draw_text_with_border(x, y, s, col, bcol, font):
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx != 0 or dy != 0:
                pyxel.text(
                    x + dx,
                    y + dy,
                    s,
                    bcol,
                    font,
                )
    pyxel.text(x, y, s, col, font)

class App:
    def __init__(self):
        pyxel.init(WINDOW_W, WINDOW_H)
        pyxel.load("./assets/palinka5yrs.pyxres")

        # Load fonts
        self.umplus10 = pyxel.Font("assets/fonts/umplus_j10r.bdf")
        self.umplus12 = pyxel.Font("assets/fonts/umplus_j12r.bdf")

        # pyxel.images[2].load(0, 0, "assets/images/BarPalinkaCounter_w256.png")
        self.scene = SCENE_TITLE
        self.music_on = False
        self.time_start = None
        self.text_A = None

        self.logo_scale = 0

        self.counter_pos = 0
        self.counter_scale = 0
        self.counter_scale_step = 0.001

        self.matsuzawa_time = 0
        self.matsuzawa_pos = -100
        self.matsuzawa_pos_step = 0.3
        self.matsuzawa_state = "inback_wait"
        self.matsuzawa_rot = 0
        self.matsuzawa_rot_level = 0

        self.visitor_state = 0

        self.bottles_scale = 0
        self.bottles_rot = 0

        self.snowflakes = [[np.random.randint(0, WINDOW_W), np.random.randint(0, WINDOW_H)] for _ in range(100)]
        
        pyxel.run(self.update, self.draw)

    def update(self):
        self.update_snow()

        if self.scene == SCENE_TITLE:
            self.update_title_scene()

        elif self.scene == SCENE_DOOR:
            if not self.music_on:
                self.music_on = True
                pyxel.playm(BGM, loop=True)
            self.update_snow()
            self.update_door_scene()

        elif self.scene == SCENE_BAR:
            self.update_bar_scene()
            self.update_matsuzawa()
            self.update_visitor()

    def draw(self):
        if self.scene == SCENE_TITLE:
            pyxel.blt(WINDOW_W//2 + (63-16) - 15,WINDOW_H//2-30,
                    1, 
                    16,8, 63,63, 
                    11)
            pyxel.text(WINDOW_W//2-50, WINDOW_H//2-4, 
                       "THIS CONTENT CONTAINS\nSOUND EFFECTS.\nMAY NOT WORK ON SAFARI.\n\nENTER OR CLICK TO CONTINUE", 
                       pyxel.COLOR_WHITE)
            # draw_text_with_border(WINDOW_W//2-70,WINDOW_H//2,
            #                       "CAUTION:", 
            #                       7, 0, 
            #                       self.umplus12)
            # draw_text_with_border(WINDOW_W//2-70,WINDOW_H//2+15,
            #                       "This content contains", 
            #                       7, 0, 
            #                       self.umplus12)
            # draw_text_with_border(WINDOW_W//2-70,WINDOW_H//2+30,
            #                       "sound effects", 
            #                       7, 0, 
            #                       self.umplus12)
            # draw_text_with_border(WINDOW_W//2-70,WINDOW_H//2+55,
            #                       "ENTER or CLICK to continue", 
            #                       7, 0, 
            #                       self.umplus12)
            
        elif self.scene == SCENE_DOOR:
            pyxel.cls(0)
            self.draw_bar_logo(scale=self.logo_scale)
            self.draw_snow()
            if self.text_A is not None:
                draw_text_with_border(WINDOW_W//2-70,WINDOW_H-40,
                                    self.text_A, 
                                    7, 0, 
                                    self.umplus12)
        
        elif self.scene == SCENE_BAR:
            pyxel.cls(0)
            self.draw_bar_wall()
            self.draw_matsuzawa_turn()
            self.draw_bar_counter()
            self.draw_snow()
            if self.text_A is not None:
                draw_text_with_border(20,WINDOW_H-40,
                                    self.text_A, 
                                    7, 0, 
                                    self.umplus12)

    def update_title_scene(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_KP_ENTER):
            self.scene = SCENE_DOOR

    def update_door_scene(self):
        logo_start_time = 5
        logo_end_time = 15

        if self.time_start is None:
            self.time_start = time.time()

        if time.time() - self.time_start > logo_start_time and time.time() - self.time_start <= logo_end_time:
            self.logo_scale = 1
        elif time.time() - self.time_start > logo_end_time:
            self.scene = SCENE_BAR
    
    def update_bar_scene(self):
        if self.time_start is None:
            self.time_start = time.time()

    def draw_bar_logo(self, scale=1):
        pyxel.blt(WINDOW_W//2 - 50, WINDOW_H//2 - 4,
                  0, 
                  *LETTER_SHI, 
                  0, 0, scale=scale)
    
    def draw_bar_wall(self):
        logo_end_time = 30
        if self.time_start is None:
            self.time_start = time.time()

        pyxel.blt(self.counter_pos,WINDOW_H//2-(87-24) + 25, 
                  0, 
                  0,24, 256,87-24, 
                  0, 0, scale=self.counter_scale)
        if time.time() - self.time_start <= logo_end_time:
            self.draw_bar_logo(scale=1)
        # if self.counter_pos > 0:
        #     self.counter_pos -= 0.5
        if self.counter_scale < 1:
            self.counter_scale += self.counter_scale_step

    def draw_bar_counter(self):
        logo_end_time = 33
        if self.time_start is None:
            self.time_start = time.time()

        pyxel.blt(self.counter_pos,WINDOW_H//2 + 25, 
                  0, 
                  0,88, 256,112-88, 
                  0, 0, scale=self.counter_scale)
        if time.time() - self.time_start <= logo_end_time:
            self.draw_bar_logo(scale=1)
        # if self.counter_pos > 0:
        #     self.counter_pos -= 0.5
        if self.counter_scale < 1:
            self.counter_scale += self.counter_scale_step
    
    def update_matsuzawa(self):
        target_pos = WINDOW_W//2 - (63-16)//2

        if self.matsuzawa_state == "inback_wait":
            self.matsuzawa_time = time.time()
            if self.counter_pos <= 0 and self.counter_scale >= 1:
                self.matsuzawa_state = "arrive"

        elif self.matsuzawa_state == "arrive":
            if self.matsuzawa_pos < target_pos:
                self.matsuzawa_pos += self.matsuzawa_pos_step
            else:
                self.matsuzawa_pos = target_pos
                self.matsuzawa_state = "welcome"

        elif self.matsuzawa_state == "welcome":
            self.text_A = "まつざわ 「はれ、おあがりて」"
            self.matsuzawa_time = time.time()
            self.matsuzawa_state = "welcome_sleep"
        
        elif self.matsuzawa_state == "welcome_sleep":
            if time.time() - self.matsuzawa_time > 0:
                self.matsuzawa_state = "welcome_wait"
        
        elif self.matsuzawa_state == "welcome_wait":
            pass

        elif self.matsuzawa_state == "takeorder":
            self.text_A = "まつざわ 「なんに する かな」"
            self.update_bottles()
            self.matsuzawa_time = time.time()
            self.matsuzawa_state = "takeorder_sleep"

        elif self.matsuzawa_state == "takeorder_sleep":
            self.update_bottles()
            if time.time() - self.matsuzawa_time > 0:
                self.matsuzawa_state = "takeorder_wait"
        
        elif self.matsuzawa_state == "takeorder_wait":
            self.update_bottles()
            self.matsuzawa_time = time.time()
        
        elif self.matsuzawa_state == "serve":
            self.update_bottles()
            self.text_A = "・・・"
            if time.time() - self.matsuzawa_time > 3 and time.time() - self.matsuzawa_time <= 6:
                self.text_A = "・・・ ・・・"
            elif time.time() - self.matsuzawa_time > 6 and time.time() - self.matsuzawa_time <= 9:
                self.text_A = "・・・ ・・・ ・・・！"
            elif time.time() - self.matsuzawa_time > 9 and time.time() - self.matsuzawa_time <= 12:
                if 2 ** self.matsuzawa_rot_level > 1:
                    self.text_A = f"まつざわ の {2 ** self.matsuzawa_rot_level}ばい ジェット ふんしゃ！"
                else:
                    self.text_A = f"まつざわ の ジェット ふんしゃ！"
                self.matsuzawa_state = "rotate"
        
        elif self.matsuzawa_state == "afterjet":
            if time.time() - self.matsuzawa_time > 3:
                self.matsuzawa_state = "takeorder"

        elif self.matsuzawa_state == "rotate":
            self.update_bottles()
            # self.matsuzawa_rot_state = self.matsuzawa_rot_param * self.matsuzawa_rot_state * (1 - self.matsuzawa_rot_state)
            self.matsuzawa_rot += 2 ** self.matsuzawa_rot_level
            pyxel.play(3,3,loop=True)
            if self.matsuzawa_rot >= 360 * (3 - 1 + 2 ** self.matsuzawa_rot_level):
                self.matsuzawa_rot = 0
                self.matsuzawa_rot_level += 1
                if self.matsuzawa_rot_level >= 10:
                    self.matsuzawa_rot_level = 1
                pyxel.play(3,3,loop=False)
                self.bottles_scale = 0
                self.bottles_rot = 0

                self.matsuzawa_state = "afterjet"
                self.matsuzawa_time = time.time()
                self.text_A = "かんな"
            
            if self.matsuzawa_rot >= 360 and self.matsuzawa_rot_level < 3:
                self.text_A = "まつざわ は まわって いる"

    def update_visitor(self):
        if self.visitor_state == 0:
            if self.matsuzawa_state == "welcome_wait":
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    self.matsuzawa_state = "takeorder"
            if self.matsuzawa_state == "takeorder_wait":
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    # self.text_A = "まつざわ は まわる じゅんび を はじめた"
                    self.matsuzawa_state = "serve"

    
    def draw_matsuzawa_turn(self):
        if self.matsuzawa_state == "inback_wait":
            self.draw_matsuzawa((self.matsuzawa_pos,WINDOW_H//2-20))
        elif self.matsuzawa_state == "arrive":
            self.draw_matsuzawa((self.matsuzawa_pos,WINDOW_H//2-20))
        elif self.matsuzawa_state == "welcome":
            self.draw_matsuzawa((self.matsuzawa_pos,WINDOW_H//2-20))
        elif self.matsuzawa_state == "welcome":
            self.draw_matsuzawa((self.matsuzawa_pos,WINDOW_H//2-20))
        elif self.matsuzawa_state == "welcome_sleep":
            self.draw_matsuzawa((self.matsuzawa_pos,WINDOW_H//2-20))
        elif self.matsuzawa_state == "welcome_wait":
            self.draw_matsuzawa((self.matsuzawa_pos,WINDOW_H//2-20))

        elif self.matsuzawa_state == "takeorder":
            self.draw_matsuzawa((self.matsuzawa_pos,WINDOW_H//2-20))
            self.draw_bottles()
        elif self.matsuzawa_state == "takeorder_sleep":
            self.draw_matsuzawa((self.matsuzawa_pos,WINDOW_H//2-20))
            self.draw_bottles()
        elif self.matsuzawa_state == "takeorder_wait":
            self.draw_matsuzawa((self.matsuzawa_pos,WINDOW_H//2-20))
            self.draw_bottles()
        elif self.matsuzawa_state == "serve":
            self.draw_matsuzawa((self.matsuzawa_pos,WINDOW_H//2-20), 
                                rot=self.matsuzawa_rot)
            self.draw_bottles()
        elif self.matsuzawa_state == "rotate":
            self.draw_matsuzawa((self.matsuzawa_pos,WINDOW_H//2-20), 
                                rot=self.matsuzawa_rot)
            self.draw_bottles()
    
    def draw_matsuzawa(self, pos, rot=0, scale=1):
        pyxel.blt(pos[0], pos[1],
                  1, 
                  16,8, 
                  71-16,63-8, 
                  11,
                  rotate=rot, scale=scale)
    
    def update_bottles(self):
        if self.bottles_scale < 1:
            self.bottles_scale += 0.01
        self.bottles_rot += 5
        if self.bottles_rot >= 360:
            self.bottles_rot = 0

    def draw_bottles(self):
        self.draw_bottle(MTBD, (WINDOW_W//2-70, WINDOW_H//4), self.bottles_rot, self.bottles_scale)
        self.draw_bottle(GRANDMONTE, (WINDOW_W//2-35, WINDOW_H//4), self.bottles_rot, self.bottles_scale)
        self.draw_bottle(FRAULEIN, (WINDOW_W//2+5, WINDOW_H//4), self.bottles_rot, self.bottles_scale)
        self.draw_bottle(IRSAI, (WINDOW_W//2+40, WINDOW_H//4), self.bottles_rot, self.bottles_scale)

    def draw_bottle(self, brand, pos, rot, scale):
        pyxel.blt(pos[0], pos[1],
                  1, 
                  *brand, 
                  0, rotate=rot, scale=scale)     
    
    def update_snow(self):
        for flake in self.snowflakes:
            flake[1] += 0.5
            if flake[1] > WINDOW_H:
                flake[0] = np.random.randint(0, WINDOW_W)
                flake[1] = 0

    def draw_snow(self):
        for flake in self.snowflakes:
            pyxel.pset(flake[0], flake[1], pyxel.COLOR_WHITE)

App()