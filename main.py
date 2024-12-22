import pyxel
import numpy as np
import time

WINDOW_ASPECT = 1 # 1.33
WINDOW_SCALE = 256
WINDOW_H = int(WINDOW_SCALE * 1)
WINDOW_W = int(WINDOW_SCALE * WINDOW_ASPECT)


LETTER_SHI = (0, 0, 100, 9)

BGM = 0

SCENE_TITLE = 0
SCENE_DOOR = 1
SCENE_BAR = 2

class App:
    def __init__(self):
        pyxel.init(WINDOW_W, WINDOW_H)
        pyxel.load("./assets/palinka5yrs.pyxres")
        # pyxel.images[2].load(0, 0, "assets/images/BarPalinkaCounter_w256.png")
        self.scene = SCENE_TITLE
        self.music_on = False
        self.time_start = None

        self.logo_scale = 0
        self.counter_pos = 260
        self.matsuzawa_pos = -100

        self.matsuzawa_first_move = False
        self.matsuzawa_rot = 0

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

    def draw(self):
        if self.scene == SCENE_TITLE:
            pyxel.blt(WINDOW_W//2 - (63-16)//2,WINDOW_H//2-30,
                    1, 
                    16,8, 63,63, 
                    11)
            pyxel.text(WINDOW_W//2 - 50, WINDOW_H//2 - 4, 
                       "CAUTION\n Sound will be played\n \nENTER or CLICK", 
                       pyxel.COLOR_WHITE)
            
        elif self.scene == SCENE_DOOR:
            pyxel.cls(0)
            self.draw_bar_logo(scale=self.logo_scale)
            self.draw_snow()
        
        elif self.scene == SCENE_BAR:
            pyxel.cls(0)
            self.draw_bar_wall()
            self.draw_matsuzawa()
            self.draw_bar_counter()
            self.draw_snow()

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
                  0, 0, scale=1)
        if time.time() - self.time_start <= logo_end_time:
            self.draw_bar_logo(scale=1)
        if self.counter_pos > 0:
            self.counter_pos -= 0.5

    def draw_bar_counter(self):
        logo_end_time = 30
        if self.time_start is None:
            self.time_start = time.time()

        pyxel.blt(self.counter_pos,WINDOW_H//2 + 25, 
                  0, 
                  0,88, 256,112-88, 
                  0, 0, scale=1)
        if time.time() - self.time_start <= logo_end_time:
            self.draw_bar_logo(scale=1)
        if self.counter_pos > 0:
            self.counter_pos -= 0.5
    
    def draw_matsuzawa(self):
        target_pos = WINDOW_W//2 - (63-16)//2

        if self.counter_pos <= 0 and not self.matsuzawa_first_move:
            pyxel.blt(self.matsuzawa_pos,WINDOW_H//2-20,
                      1, 
                      16,8, 71-16,63-8, 
                      11)
            if self.matsuzawa_pos < target_pos:
                self.matsuzawa_pos += 0.5
            else:
                self.matsuzawa_first_move = True
        
        if self.matsuzawa_first_move:
            pyxel.blt(self.matsuzawa_pos,WINDOW_H//2-20,
                      1, 
                      16,8, 71-16,63-8, 
                      11, rotate=self.matsuzawa_rot)  
            self.matsuzawa_rot += 0.5       
    
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