import simplegui
import random
import math

# helper functions
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def update_pos_vector(s, ds):
    s[0] = (s[0] + ds[0]) % game.WIDTH
    s[1] = (s[1] + ds[1]) % game.HEIGHT
    
def update_vel_vector(v, dv):
    v[0] = (v[0] + dv[0])
    v[1] = (v[1] + dv[1])
    
def rand(a,b):
    return a + (b-a)*random.random()

def draw_centred_text(canvas, frame, text, pos, size, col = "White", face = "sans-serif"):
    x = pos[0]-frame.get_canvas_textwidth(text, size, face)/2
    canvas.draw_text(text,(x, pos[1]), size, col, face)   
    
def draw_right_text(canvas, frame, text, pos, size, col = "White", face = "sans-serif"):
    x = pos[0] - frame.get_canvas_textwidth(text, size, face)
    canvas.draw_text(text,(x, pos[1]), size, col, face) 
#-----------------------------------------------      

class Game:
    def __init__(self):
        self.scale = 1.0
        self.HEIGHT = 800*self.scale
        self.WIDTH = 1024*self.scale
        self.ALIEN_ROWS = 5
        self.ALIEN_COLS = 11
        self.ALIEN_COUNT = self.ALIEN_ROWS * self.ALIEN_COLS
        self.ALIEN_START_TICK_COUNT = 41
        self.ALIEN_START_FIRE_COUNTDOWN = 200
        self.ALIEN_MIN_FIRE_DELAY = 60

        self.BIG_ALIEN_Y = 90
        self.BIG_ALIEN_DELAY_BETWEEN = 900
        self.BIG_ALIEN_SPEED = 2.5
        
        self.TOP_TEXT_Y = 50
        self.TOP_ROW_POS = 170
        self.ROW_GAP = 50
        self.COL_GAP = 50
        self.START_LIVES = 3
        self.MAX_LIVES = 5

        self.BASE_START_SPEED = 4
        self.BASE_EDGE_LIMIT = 120
        self.BASE_HEIGHT = self.HEIGHT - 100

        self.ALIEN_WIN_Y = self.BASE_HEIGHT - 80 
        self.ALIEN_MISSILE_SPEED = 8
        self.ALIEN_MISSILE_RANGE = 650
        self.ALIEN_MISSILE_PROXIMITY_RADIUS = 8
        
        self.PLAYER_MISSILE_SPEED = 15
        self.PLAYER_MISSILE_RANGE = 600
        self.PLAYER_MISSILE_PROXIMITY_RADIUS = 8

        self.MISSILE_HIT_SOUND = simplegui.load_sound("http://dl.dropbox.com/s/nn01nwi52styyef/missile_hit.mp3?dl=0")

        self.PAUSED = 0
        self.RUNNING = 1
        self.BASE_HIT = 2
        self.BASE_PREPARING = 3
        self.OVER = 4
        self.LEVEL_COMPLETE = 5
        self.INTRO = 6
        
        self.PLAYER_DIE_TIME = 180
        self.BASE_PREPARING_DELAY =180
        self.LEVEL_COMPLETE_TIME = 180
        
        self.state = self.INTRO
        
        self.level = 1
        self.score = 0
        self.count = 0
        self.lives = self.START_LIVES
        self.pause_count = 0 
        self.best_score = 0
        
    def increment_score(self, value):
        new_score = self.score + value
        if  (self.score//5000 != new_score//5000) and self.lives<self.MAX_LIVES:
            self.lives+=1
        self.score = new_score
        
    def reset(self):
        self.best_score = max(self.best_score, self.score)
        self.level = 1
        self.score = 0
        self.count = 0
        self.lives = self.START_LIVES
        self.pause_count = 0        
                
#=============================================

# Sprite class
class Sprite:
    def __init__(self, image, centre, size, num_tiles, offset):
        self.image = image
        self.centre = list(centre)
        self.size = list(size)
        self.num_tiles = num_tiles
        self.offset = offset
        
        self.pos = [0, 0]
        self.vel = [0, 0]
        self.angle = 0
        self.angle_vel = 0
        self.scale = 1.0
        self.scale_size = list(self.size)
        
        self.tile_num = 0        # The current tile number within the sprite strip
        self.animating = False   # True if sprite is automatically animating through tile strip
        self.frame_lifespan = 0  # The number of draw calls before moving to next tile if animating
        self.frame_age      = 0  # Age of the current frame
        self.alive = True        # Start sprite as alive
        self.sound = None

    #-----------------------------------------------
   
    def set_motion(self, pos, vel, angle, angle_vel):
        self.pos = list(pos)
        self.vel = list(vel)
        self.angle = angle
        self.angle_vel = angle_vel
    #-----------------------------------------------
    def set_vel(self, v):
        self.vel = list(v)
    #-----------------------------------------------
    def set_pos(self, pos):
        self.pos = list(pos)
    #-----------------------------------------------
    def set_angle(self, angle):
        self.angle = angle
    #-----------------------------------------------
    def set_angle_vel(self, angle_vel):
        self.angle_vel = angle_vel
    #-----------------------------------------------
    
    def set_scale(self, scale):
        self.scale = scale
        self.scale_size[0] = self.size[0] * scale
        self.scale_size[1] = self.size[1] * scale
    
        
    def draw(self, canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        if self.animating:
            self.frame_age-=1
            if self.frame_age<=0:
                self.frame_age = self.frame_lifespan
                self.tile_num = (self.tile_num+1) % self.num_tiles
        centre=(self.centre[0]+self.tile_num*self.offset, self.centre[1])
        canvas.draw_image(self.image, centre, self.size, self.pos, self.scale_size, self.angle)
        
    #-----------------------------------------------
    
    def set_animation(self, truefalse, frame_lifespan=0 ):
        self.animating = truefalse
        if frame_lifespan>0:
            self.frame_lifespan = frame_lifespan
            self.frame_age = 0
    #-----------------------------------------------
    
    def set_sound(self, sound):
        self.sound = sound
    #-----------------------------------------------
    
    def play_sound(self):
        if self.sound:
            self.sound.rewind()
            self.sound.play()
    #-----------------------------------------------
    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel
    #-----------------------------------------------
    
    def get_pos(self):
        return tuple(self.pos)
    #-----------------------------------------------
    
    def is_alive(self):
        return self.alive
    #-----------------------------------------------
    def set_alive(self, truefalse):
        self.alive = truefalse
        if not self.alive and self.sound:
            self.sound.pause()
    #-----------------------------------------------
    
    def get_radius(self):
        return self.redius
    #-----------------------------------------------
    
    def get_vel(self):
        return tuple(self.vel)
    #-----------------------------------------------
    
    def collide(self, other):
        return (self.pos[0] - self.scale_size[0]/2 <= other.pos[0] <= self.pos[0] + self.scale_size[0]/2) and (self.pos[1] - self.scale_size[1]/2 <= other.pos[1] <= self.pos[1] + self.scale_size[1]/2)
 
####### End of Sprite class #####################

#=============================================

class Alien(Sprite):
    def __init__(self, image, centre, size, offset, value):
        Sprite.__init__(self, image, centre, size, 2, offset)
        self.value = value
        self.next_up = None
        self.next_down = None
        self.column = -1
    #-----------------------------------------------
    
    def __str__(self):
        return str(self.column)
    #-----------------------------------------------
        
    def __repr__(self):
        return str(self.column)
    #-----------------------------------------------
 
    def update(self, pos, tile_num):
        self.pos=list(pos)
        self.offset2 = 0 if tile_num==0 else self.offset
    #-----------------------------------------------
        
    def draw(self, canvas):
        centre=(self.centre[0]+self.tile_num*self.offset, self.centre[1])
        canvas.draw_image(self.image, centre, self.size, self.pos, self.scale_size, self.angle)

####### End of Alien class #####################

class BigAlien(Sprite):
    def __init__(self, image, centre, size, value):
        Sprite.__init__(self, image, centre, size, 1, 0)
        self.value = value
        self.running = True
        self.count = 0
        
    def stop_running(self):
        self.running = False
        self.count = 180
        self.vel = [0, 0]
        self.sound.rewind()
        
    def draw(self, canvas):
        if self.running:
            Sprite.draw(self, canvas)
        else:
            self.count-=1
            if self.count > 0:
                canvas.draw_text(str(self.value), (self.pos[0]-20, self.pos[1]), 30, "Red", "sans-serif")
            else:
                self.set_alive(False)
        
####### End of BigAlien class #####################

class Missile(Sprite):
    def __init__(self, image, centre, size, proximity_radius, num_tiles=1, offset=0):
        Sprite.__init__(self, image, centre, size, num_tiles, offset)
        self.max_range = 0
        self.launch_pos = (0,0)
        self.expired = False
        self.proximity_radius = proximity_radius
        
    def launch(self, max_range):
        self.max_range = max_range
        self.launch_pos = tuple(self.pos)
        self.alive = True
        self.expired = False
        self.play_sound()
    
    def update(self):
        Sprite.update(self)
        if dist(self.launch_pos, self.pos) > self.max_range:
            self.alive = False
            self.expired = True
        
####### End of Missile class #####################

class Explosion(Sprite):
    def __init__(self, image, centre, size, num_tiles, offset):
        Sprite.__init__(self, image, centre, size, num_tiles, offset)

    def draw(self, canvas):
        Sprite.draw(self, canvas)
        if self.tile_num == self.num_tiles - 1:
            self.alive = False
        
####### End of Explosion class ###################

class SliderSprite(Sprite):
    def __init__(self, image, centre, size, num_tiles, offset, text, font_size, colour):
        Sprite.__init__(self, image, centre, size, num_tiles, offset)
        self.text = text
        self.font_size = font_size
        self.colour = colour
        self.num_steps = 0

        
    def set_target(self, pos, num_steps):
        self.vel = [(pos[0] - self.pos[0])/float(num_steps),
                    (pos[1] - self.pos[1])/float(num_steps)]
        self.num_steps = num_steps
     
    def draw(self, canvas):
        if self.num_steps > 0:
            Sprite.update(self)
            self.num_steps-=1
            
        if self.image != None:
            Sprite.draw(self, canvas)
        canvas.draw_text(self.text, (self.pos[0]+self.scale_size[0], self.pos[1]+self.font_size/2),
                         self.font_size, self.colour, "sans-serif")
            
####### End of SliderSprite class ###################

    
class AlienManager:
    RUNNING = 0
    ALL_DESTROYED = 1
    LOWER_LIMIT_REACHED = 2
    
    def __init__(self, sprites, game):
        self.sprites = sprites
        self.g = game
        self.max_tick_count = self.g.ALIEN_START_TICK_COUNT
        self.tick_count = 0
        self.alive_count = 0
        self.left = 0
        self.right = 0
        self.bottom =0
        self.dx = 0
        self.at_edge = False
        self.fire_countdown = 0
        self.big_alien = None
        self.big_alien_countdown = self.g.BIG_ALIEN_DELAY_BETWEEN - 10 * self.g.level + random.randrange(600)
        
        self.sound_num = 0
        
        self.isound=[0] *4
        self.isound[0] = simplegui.load_sound("http://dl.dropbox.com/s/fiiycy78txpitwj/invader1.wav?dl=0")
        self.isound[1] = simplegui.load_sound("http://dl.dropbox.com/s/dvy193k2809dygz/invader2.wav?dl=0")
        self.isound[2] = simplegui.load_sound("http://dl.dropbox.com/s/4i52eon80uk62xf/invader3.wav?dl=0")
        self.isound[3] = simplegui.load_sound("http://dl.dropbox.com/s/c4j0f4t4x5ehsqy/invader4.wav?dl=0")
        self.big_alien_sound = simplegui.load_sound("http://dl.dropbox.com/s/bij5bqnvtvi2zxe/big_alien.mp3?dl=0")
        
        self.aliens = [None for c in range(self.g.ALIEN_ROWS * self.g.ALIEN_COLS)]
        self.colums = []
        
        for a in range(self.g.ALIEN_COLS):
            self.aliens[a] = Alien(sprites,(20,14),(27,25),41, 40)
            
        for a in range(self.g.ALIEN_COLS,3*self.g.ALIEN_COLS):
            self.aliens[a] = Alien(sprites,(20,14+29),(33,25),41, 20)
            
        for a in range(3*self.g.ALIEN_COLS,5*self.g.ALIEN_COLS):
            self.aliens[a] = Alien(sprites,(20,14+2*29),(37,25),41, 10)

        self.reset()
            
    #-----------------------------------------------
    def reset(self):
        a=0
        start_x = self.g.WIDTH/2-self.g.ALIEN_COLS/2*self.g.COL_GAP
        for r in range(self.g.ALIEN_ROWS):
            for c in range(self.g.ALIEN_COLS):
                self.aliens[a].alive = True
                self.aliens[a].pos = [start_x+c*self.g.COL_GAP,self.g.TOP_ROW_POS+r*self.g.ROW_GAP]
                a+=1
        self.sound_num=2
        self.alive_count = self.g.ALIEN_ROWS * self.g.ALIEN_COLS
        self.calc_bounds()
        self.next_dx = 10
        self.dx = 10
        self.at_edge = False
        self.max_tick_count = self.g.ALIEN_START_TICK_COUNT
        self.shift_down_count = 0
        self.fire_countdown = max(self.g.ALIEN_START_FIRE_COUNTDOWN - (self.g.level+1)*10 - rand(0,30),
                                  self.g.ALIEN_MIN_FIRE_DELAY)
        
        #Set column pointers to bottom alien in each column
        self.columns =[self.aliens[i] for i in range(self.g.ALIEN_COUNT-self.g.ALIEN_COLS, self.g.ALIEN_COUNT)]
        
        #set aliens to point to next up in column
        for a in range(self.g.ALIEN_COLS, self.g.ALIEN_COUNT):
            self.aliens[a].next_up = self.aliens[a - self.g.ALIEN_COLS]
            
        #set aliens to point to next down in column
        for a in range(self.g.ALIEN_COUNT - self.g.ALIEN_COLS):
            self.aliens[a].next_down = self.aliens[a + self.g.ALIEN_COLS]  
            
        #give each alien its column number
        for a in range(self.g.ALIEN_COUNT):
            self.aliens[a].column = a % self.g.ALIEN_COLS
                
        if self.big_alien != None:
            self.big_alien.set_alive(False)
        self.big_alien = None
        self.big_alien_countdown = self.g.BIG_ALIEN_DELAY_BETWEEN - 10 * self.g.level + random.randrange(600)
        
    #----------------------------------------------- 
    def calc_bounds(self):
        self.left = 5000
        self.right = 0
        self.bottom = 0
        self.alive_count = 0
        for a in self.aliens:
            if not a.alive:
                continue
                
            self.alive_count+=1
            if a.pos[0] > self.right:
                self.right = a.pos[0]
            if a.pos[0] < self.left:
                self.left = a.pos[0]
            if a.pos[1]+a.size[1]/2 > self.bottom:
                self.bottom = a.pos[1]+a.size[1]/2
    #----------------------------------------------- 
    def shift(self, dx, dy):  
        for a in self.aliens:
            a.tile_num = 1-a.tile_num
            a.pos[0]+=dx
            a.pos[1]+=dy
    #----------------------------------------------- 
    
    #Returns True if still running or False if all aliens destroyed
    def update(self, missile_mgr):
        self.calc_bounds()
        if self.alive_count <=0:
            return AlienManager.ALL_DESTROYED
        
        if self.bottom >= self.g.ALIEN_WIN_Y:
            return AlienManager.LOWER_LIMIT_REACHED
            
        self.max_tick_count = self.g.ALIEN_START_TICK_COUNT - (self.g.ALIEN_COUNT-self.alive_count)/4 - self.shift_down_count - 2*self.g.level+1
        self.tick_count+=1
        if self.tick_count>=self.max_tick_count:
            self.tick_count = 0
            
            self.sound_num = (self.sound_num+1) % 4
            self.isound[self.sound_num].rewind()
            self.isound[self.sound_num].play()       
            
            if self.at_edge:
                self.shift(self.dx, 0)
                self.at_edge = False
                self.shift_down_count+=1
                
            elif self.right >= self.g.WIDTH-75:
                self.shift(0, self.g.ROW_GAP/2)
                self.dx = -10
                self.at_edge = True
                self.shift_down_count+=1
                
            elif self.left <= 75:
                self.shift(0, self.g.ROW_GAP/2)
                self.dx = 10
                self.at_edge = True
                
            else:
                self.shift(self.dx,0)
                self.at_edge = False
            
        #Now check if we should fire any missiles
        self.fire_countdown-=1
        if self.fire_countdown <= 0:
            self.fire_countdown = max(self.g.ALIEN_START_FIRE_COUNTDOWN - (self.g.level+1 + self.shift_down_count)*10 + self.alive_count/2 - rand(0,30),
                                      self.g.ALIEN_MIN_FIRE_DELAY)
            cols = [a for a in self.columns if a != None]
            if len(cols) > 0:
                a = random.choice(cols)
                m = Missile(self.sprites, (33.5, 125.5), (23,5),
                            self.g.ALIEN_MISSILE_PROXIMITY_RADIUS, 2, 23)
                m.set_animation(True, 60)
  
                angle = a.angle + math.pi/2.0
                vec = angle_to_vector(angle)
                m.set_motion((a.pos[0],a.pos[1]+20), (vec[0]*self.g.ALIEN_MISSILE_SPEED, vec[1]*self.g.ALIEN_MISSILE_SPEED), angle, 0)
                missile_mgr.add(m)
                #m.launch(self.g.ALIEN_MISSILE_RANGE)
                m.launch(self.g.BASE_HEIGHT - a.pos[1] + 20)
              
            
        #Now check big alien
        if self.big_alien != None:
            self.big_alien.update()
            if self.big_alien.get_pos()[0] > self.g.WIDTH:
                self.big_alien.set_alive(False)
                self.big_alien = None
                
        else:
            self.big_alien_countdown-=1
            if self.big_alien_countdown <= 0:
                self.big_alien_countdown = self.g.BIG_ALIEN_DELAY_BETWEEN - 10 * self.g.level + random.randrange(600)
                self.big_alien = BigAlien(self.sprites, (40.5,104.5), (77, 31), random.choice([100,200,300]))
                self.big_alien.set_pos((self.g.BASE_EDGE_LIMIT, self.g.BIG_ALIEN_Y))
                self.big_alien.set_vel((self.g.BIG_ALIEN_SPEED + self.g.level/10.0, 0))
                                
                self.big_alien.set_sound(self.big_alien_sound)
                self.big_alien.play_sound()
        
        return AlienManager.RUNNING

    #-----------------------------------------------  
    
    def collide(self, missile_mgr, exp_mgr):
        for m in missile_mgr.item_list():            
            for a in self.aliens[::-1]:
                if a.is_alive() and a.collide(m):  
                    m.set_alive(False)
                    self.g.increment_score(a.value)
                    
                    # Create an explosion
                    ex = Explosion(explosion_image, (25,25),(50,50), 74, 50)
                    ex.set_motion (a.get_pos(), (0,0), 0, 0)
                    ex.set_animation(True, 1)
                    ex.set_sound(self.g.MISSILE_HIT_SOUND)
                    ex.play_sound()                    
                    exp_mgr.add(ex)
                    
                    #Now kill the alien and update column information
                    a.set_alive(False)
                    
                    #Update alien above to point to one below
                    if a.next_up!=None:
                        a.next_up.next_down = a.next_down
                    
                    #Update alien below to point to one above
                    if a.next_down == None:
                        #This is the lowest in the column
                        self.columns[a.column] = a.next_up
                    else:
                        a.next_down.next_up = a.next_up

                    break 
                    
        if self.big_alien == None or not self.big_alien.running:
            return
        
        for m in missile_mgr.item_list():
            if m.alive and self.big_alien.collide(m):
                self.big_alien.stop_running()
                self.g.increment_score(self.big_alien.value)
                m.set_alive(False)
                # Create an explosion
                ex = Explosion(explosion_image, (25,25),(50,50), 74, 50)
                ex.set_motion (self.big_alien.get_pos(), (0,0), 0, 0)
                ex.set_animation(True, 1)
                ex.set_sound(self.g.MISSILE_HIT_SOUND)
                ex.play_sound()                    
                exp_mgr.add(ex)
                break
                

    #----------------------------------------------- 
    
    def draw(self, canvas):
        for a in self.aliens:
            if a.alive:
                a.draw(canvas)
        if self.big_alien != None:
            self.big_alien.draw(canvas)
                              

####### End of Alien manager #####################

class Shelter:
    
    def __init__(self, images, game, pos):
        self.g = game
        self.lines =[None for i in range(100)] #each entry will be ( (start x,y),length )
        self.pos = pos
        self.reset()
        
    def reset(self):
        x = self.pos[0]
        y = self.pos[1]
        
        height = 60
        for n in range(20):
            self.lines[n] = [[x+n,y], height+n]
            self.lines[99-n] = [[x+99-n, y], height+n]
            self.lines[20+n] = [[x+20+n, y-20-n],height-n]
            self.lines[79-n] = [[x+79-n, y-20-n],height-n]
            self.lines[40+n] = [[x+40+n, y-40], 40]

        
    #----------------------------------------------- 
    def collide(self, missile_mgr, exp_mgr):
        for m in missile_mgr.item_list():
            r = m.proximity_radius
            if m.pos[0] + r/3 < self.pos[0] or m.pos[0] - r/3 > self.pos[0]+99 or m.pos[1] + r/3 < self.pos[1]-80 or m.pos[1] - r/3 > self.pos[1]:
                continue

            m_mid_x = round(m.pos[0])
            m_left_x = int(max(m_mid_x - r, self.pos[0]))
            m_right_x = int(min(m_mid_x + r, self.pos[0]+99))
            
            #print m_left_x, m_mid_x, m_right_x
            
            sl = m_left_x - self.pos[0]
            hit = False
            for x in range(m_left_x, m_right_x+1): 
                y_len = self.lines[sl][1]
                y_bot = self.lines[sl][0][1]
                y_top = y_bot - y_len
                if y_len > 0 and m.pos[1]+r > y_top and m.pos[1] - r < y_bot: 
                    #hit - was it nearer top or bottom?
                    if abs(m.pos[1] - y_bot) < abs(m.pos[1] - y_top):
                        self.lines[sl][0][1]-=2*r
                    self.lines[sl][1]-=2*r
                    if self.lines[sl][1] < 5:
                        self.lines[sl][1] = 0
                    hit = True
                sl+=1
                
            #Check if there was a hit. If so kill missile and create explosion
            if hit:
                m.set_alive(False)
                ex = Explosion(explosion_image, (25,25),(50,50), 74, 50)
                ex.set_motion (m.get_pos(), (0,0), 0, 0)
                ex.set_animation(True, 1)
                ex.set_sound(self.g.MISSILE_HIT_SOUND)
                ex.play_sound()
                exp_mgr.add(ex)
                
    #-----------------------------------------------  
    def draw(self, canvas):
        for l in self.lines:
            if l[1]>0:
                canvas.draw_line(l[0], ( l[0][0], l[0][1]-l[1]), 1 ,"lime")


####### End of Shelter Class #####################

class Base(Sprite):
    def __init__(self, image, centre, size, num_tiles, offset, game):
        Sprite.__init__(self, image, centre, size, num_tiles, offset)
        self.left = False
        self.right = False
        self.g = game
        self.speed = self.g.BASE_START_SPEED
        self.missile = None
        self.hit_sound=None
        self.die_countdown = 0
        
    def reset(self):
        self.speed = self.g.BASE_START_SPEED
        self.left = False
        self.right = False
        if self.missile != None:
            self.missile.set_alive(False)
        
    def load_missile(self, m):
        self.missile = m
        self.missile.set_alive(False)
        
    def set_hit_sound(self, sound):
        self.hit_sound = sound
        
    def set_alive(self, truefalse):
        if truefalse:
            self.hit_sound.pause()
        else:
            self.hit_sound.rewind()
            self.hit_sound.play()
            self.die_countdown = 255
           
        self.alive = truefalse
            
        
    def update(self):
        Sprite.update(self)
        if self.pos[0] < self.g.BASE_EDGE_LIMIT:
            self.pos[0] = self.g.BASE_EDGE_LIMIT
        elif self.pos[0] > self.g.WIDTH - self.g.BASE_EDGE_LIMIT:
            self.pos[0] = self.g.WIDTH - self.g.BASE_EDGE_LIMIT
            
    def get_firing_point(self):
        return list([self.pos[0], self.pos[1]-25])
    
    def fire_missile(self, missile_mgr):
        if self.missile == None or self.missile.is_alive():
            return
     
        angle = self.angle - math.pi/2.0
        vec = angle_to_vector(angle)
        self.missile.set_motion(self.get_firing_point(), (vec[0]*self.g.PLAYER_MISSILE_SPEED, vec[1]*self.g.PLAYER_MISSILE_SPEED), angle, 0)
        missile_mgr.add(self.missile)
        self.missile.launch(self.g.PLAYER_MISSILE_RANGE)
        
    def collide(self, missile_mgr, ex_mgr):
        for m in missile_mgr.item_list():
            if Sprite.collide(self, m):
                m.set_alive(False)
                # Create an explosion
                ex = Explosion(explosion_image, (25,25),(50,50), 74, 50)
                ex.set_motion (m.get_pos(), (0,0), 0, 0)
                ex.set_animation(True, 1)
                ex.set_sound(self.g.MISSILE_HIT_SOUND)
                ex.play_sound()                    
                ex_mgr.add(ex)
                return True
            
        return False
        
        
    def move_left(self, truefalse):
        self.left = truefalse
        if self.left:
            self.set_vel((-self.speed, 0))
        elif self.right:
            self.set_vel((self.speed, 0))
        else:
            self.set_vel((0, 0))
        
    def move_right(self, truefalse):
        self.right = truefalse
        if self.right:
            self.set_vel((self.speed, 0))
        elif self.left:
            self.set_vel((-self.speed, 0))
        else:
            self.set_vel((0, 0))       
        
    def draw(self, canvas):
        if self.alive:
            Sprite.draw(self, canvas)
            return
        
        r = 2*int(round(self.scale_size[1]))
        for blobs in range(50):
            x = random.randrange(-r, r+1)
            y = random.randrange(-r, 1)
            if x*x +y*y <= r*r:
                canvas.draw_line((self.pos[0]+x-1, self.pos[1]+y),
                                 (self.pos[0]+x+1, self.pos[1]+y), 3, "rgb("+str(self.die_countdown)+",0,0)")
                
        if self.die_countdown > 0:
            self.die_countdown-=1
        
####### End of Base Class #####################  

class SpriteMgr:
    def __init__(self):
        self.items = set()
        
    def add(self, item):
        self.items.add(item)
        
    def reset(self):
        self.items = set()
        
    def count(self):
        return len(self.items)
        
    def item_list(self):
        return set(self.items)
    
    def update(self):
        for i in set(self.items):
            i.update()
            if not i.alive:
                 self.items.remove(i)
                
    def draw(self, canvas):
        for i in self.items:
            if i.is_alive():
                i.draw(canvas)
                
####### End of SpriteMgr Class ############### 

class MissileMgr(SpriteMgr):
    def __init__(self):
        SpriteMgr.__init__(self)
        
    def update(self, ex_mgr):
        for m in set(self.items):
            if m.alive:
                m.update()
            if not m.alive:
                self.items.remove(m)
                if m.expired:
                    ex = Explosion(explosion_image, (25,25),(50,50), 74, 50)
                    ex.set_motion (m.get_pos(), (0,0), rand(0,2*math.pi), 0)
                    ex.set_animation(True, 1)
                    ex_mgr.add(ex)  
                    
        #Now check is any missiles have hit any others
        for m1 in self.items:
            for m2 in self.items:
                if m1.alive and m2.alive and m1 != m2 and m1.collide(m2):
                    m1.alive=False
                    m2.alive=False
                    ex = Explosion(explosion_image, (25,25),(50,50), 74, 50)
                    ex.set_motion (m1.get_pos(), (0,0), rand(0,2*math.pi), 0)
                    ex.set_animation(True, 1)
                    ex_mgr.add(ex)  
            

####### End of MissileMgr Class ############
    
# Handler for keys going down

def keydown(key):
    if game.state == game.INTRO:
        game.reset()
        game.state = game.BASE_PREPARING
        game.count = game.BASE_PREPARING_DELAY
        return
    
    if game.state == game.PAUSED and key == simplegui.KEY_MAP["p"]:
        game.state = game.RUNNING
        return
    
    if game.state != game.RUNNING:
        return
    
    if key == simplegui.KEY_MAP["right"]:
        base.move_right(True)
        
    elif key == simplegui.KEY_MAP["left"]:
        base.move_left(True)
        
    elif key == simplegui.KEY_MAP["space"]:
            base.fire_missile(missile_mgr)
        
    elif key == simplegui.KEY_MAP["p"]:
            game.state = game.PAUSED
# -----------------------------------------------------------------------------------

# Handler for keys going up

def keyup(key):   
    if key == simplegui.KEY_MAP["right"]:
        base.move_right(False)
        
    elif key == simplegui.KEY_MAP["left"]:
        base.move_left(False)
# -----------------------------------------------------------------------------------

def draw_scores_and_lives(canvas):
    for y in [game.TOP_TEXT_Y+10, game.BASE_HEIGHT + 50]:
        canvas.draw_line((20, y), (game.WIDTH-21,y), 5, "Green")
    
    canvas.draw_text("Level " +str(game.level),(30, game.TOP_TEXT_Y), 25, "White", "sans-serif")
    canvas.draw_text("Score " + str(game.score) ,(150, game.TOP_TEXT_Y), 25, "White", "sans-serif")
    canvas.draw_text("Best Score " + str(game.best_score) ,(450, game.TOP_TEXT_Y), 25, "White", "sans-serif")
    
    canvas.draw_text("Lives",(game.WIDTH-270, game.TOP_TEXT_Y), 25, "White", "sans-serif")
    for l in range(game.lives-1):
        lives[l].draw(canvas)    
# -----------------------------------------------------------------------------------

def draw_shelters(canvas):
    for s in shelter_list:
        s.draw(canvas)    
# -----------------------------------------------------------------------------------

def draw(canvas):
    
    if game.state == game.RUNNING:
        base.update()
        missile_mgr.update(explosion_mgr)
        result = alien_mgr.update(missile_mgr)
        if result == AlienManager.ALL_DESTROYED:
            game.state = game.LEVEL_COMPLETE
            game.count = game.LEVEL_COMPLETE_TIME
        
        elif result == AlienManager.LOWER_LIMIT_REACHED or base.collide(missile_mgr, explosion_mgr):
            base.set_alive(False)
            base.reset()
            game.state = game.BASE_HIT
            missile_mgr.reset()
            game.count = game.PLAYER_DIE_TIME
        
        explosion_mgr.update()
        alien_mgr.collide(missile_mgr, explosion_mgr)
        for shelter in shelter_list:
            shelter.collide(missile_mgr, explosion_mgr)

        draw_scores_and_lives(canvas)
        draw_shelters(canvas)
        alien_mgr.draw(canvas)
        base.draw(canvas)
        missile_mgr.draw(canvas)
        explosion_mgr.draw(canvas)
        
    elif game.state == game.LEVEL_COMPLETE:
        draw_scores_and_lives(canvas)
        draw_shelters(canvas)
        if game.count % 20 > 10:
            draw_centred_text(canvas, frame, "Level Complete", (game.WIDTH/2, game.HEIGHT/2), 40)
        game.count-=1
        if game.count <= 0:
            alien_mgr.reset()
            missile_mgr.reset()
            explosion_mgr.reset()
            game.level+=1
            game.state = game.BASE_PREPARING
            game.count = game.BASE_PREPARING_DELAY
        
        
    elif game.state == game.BASE_HIT:
        alien_mgr.update(missile_mgr)
        
        draw_scores_and_lives(canvas)
        draw_shelters(canvas)
        alien_mgr.draw(canvas)
        base.draw(canvas)
        #missile_mgr.draw(canvas)
        explosion_mgr.draw(canvas)
        game.count-=1
        if game.count <= 0:
            game.lives-=1
            if game.lives <=0 :
                game.state = game.OVER
                alien_mgr.reset()
                game.count = 180
            else:
                game.state = game.BASE_PREPARING
                game.count = game.BASE_PREPARING_DELAY
                base.set_alive(True)
            
    elif game.state == game.BASE_PREPARING:
        missile_mgr.update(explosion_mgr)
        alien_mgr.update(missile_mgr)
        explosion_mgr.update()
        
        alien_mgr.collide(missile_mgr, explosion_mgr)
        for shelter in shelter_list:
            shelter.collide(missile_mgr, explosion_mgr)

        draw_scores_and_lives(canvas)
        draw_shelters(canvas)
        alien_mgr.draw(canvas)
        missile_mgr.draw(canvas)
        explosion_mgr.draw(canvas)
        if game.count % 30 > 15:
            draw_centred_text(canvas, frame, "Get Ready", (game.WIDTH/2, game.BASE_HEIGHT+10), 30)
        game.count-=1
        if game.count <= 0:
            game.state = game.RUNNING
            base.set_alive(True)
            base.set_pos((game.BASE_EDGE_LIMIT, game.BASE_HEIGHT))
            
    elif game.state == game.PAUSED:
        draw_scores_and_lives(canvas)
        draw_shelters(canvas)
        alien_mgr.draw(canvas)
        missile_mgr.draw(canvas)
        explosion_mgr.draw(canvas)
        if game.pause_count % 20 > 10:
            draw_centred_text(canvas, frame, "Paused", (game.WIDTH/2, game.HEIGHT/2), 130)
        game.pause_count+=1

    elif game.state == game.INTRO:
        for item in [play, space_invaders, score_table, mystery, little_alien,
                     medium_alien, large_alien, base_info, any_key]:
            item.draw(canvas)
            
    elif game.state == game.OVER:
        if game.count % 20 > 10:
            draw_centred_text(canvas, frame, "Game Over", (game.WIDTH/2, game.HEIGHT/2), 100)
        game.count-=1
        if game.count <= 0:
            for s in shelter_list:
                s.reset()
            game.state = game.INTRO

#========================================================================

def setup_intro():
    y=50
    play.set_pos((game.WIDTH+10, y))
    play.set_target((game.WIDTH/2-50, y), 50)
    
    y+=70
    space_invaders.set_pos((-70, y))
    space_invaders.set_target((game.WIDTH/2-170, y), 50) 
    
    y+=90
    score_table.set_pos((game.WIDTH+500, y))
    score_table.set_target((game.WIDTH/2-130, y), 90)
    
    y+=20
    for slider in [mystery, little_alien, medium_alien, large_alien]:
        if slider != mystery:
            slider.set_scale(1.5)
        slider.set_animation(True, 20)
        y+=70
        slider.set_pos((game.WIDTH+500+y, y))
        slider.set_target((game.WIDTH/2-110, y), 90+y/4)
        
    y+=100
    base_info.set_pos((-500, y))
    base_info.set_target((game.WIDTH/2-360, y), 140)
      
    y = game.HEIGHT-100
    x = game.WIDTH/2 - 200
    any_key.set_pos((x, y+140))
    any_key.set_target((x, y), 50)
    
#========================================================================

sprites = simplegui.load_image("http://dl.dropbox.com/s/strwci4os3f02hy/invaders.png?dl=0")

# Create game objects
game = Game()
alien_mgr =AlienManager(sprites, game)

shelter_images = simplegui.load_image("http://dl.dropbox.com/s/y2ryzq82ozkb62n/Shelter.png?dl=0")
shelter_list = [Shelter(shelter_images, game, (200+i*((game.WIDTH-500)/2), game.HEIGHT-150)) for i in range(3)]


base = Base(sprites,(24, 157), (49, 29), 6, 49, game)
base.set_motion((game.BASE_EDGE_LIMIT, game.BASE_HEIGHT), (0,0), 0, 0)
base_hit_sound=simplegui.load_sound("http://dl.dropbox.com/s/d8004xgri0ixd8v/base_hit.mp3?dl=0")
base.set_hit_sound(base_hit_sound)

m = Missile(sprites, (10.5, 125.5), (21,3), game.PLAYER_MISSILE_PROXIMITY_RADIUS)
missile_sound=simplegui.load_sound("http://dl.dropbox.com/s/k44fllx8m31g4b6/base_missile.mp3?dl=0")
m.set_sound(missile_sound)
base.load_missile(m)

missile_mgr = MissileMgr()
explosion_mgr = SpriteMgr()

explosion_image = simplegui.load_image("http://dl.dropbox.com/s/ydd05yll9tkmf5v/explosion.png?dl=0")


lives = [Base(sprites,(26, 157), (51, 29), 1, 0, game) for l in range(game.MAX_LIVES-1)]
for l in lives:
    l.set_scale(0.6)
    l.set_pos((game.WIDTH-170+lives.index(l)*40, game.TOP_TEXT_Y-10))
    
#create objects for the intro screen
play = SliderSprite(None, (0,0), (0,0), 0, 0, "Play", 50, "White")
space_invaders = SliderSprite(None, (0,0), (0,0), 0, 0, "Space Invaders", 50, "White")
score_table = SliderSprite(None, (0,0), (0,0), 0, 0, "Score Table", 45, "Blue")
mystery = SliderSprite(sprites,(40.5,104.5), (77, 31), 2, 77, " = ?  Mystery", 30, "Red")
little_alien = SliderSprite(sprites,(20,14),(27,25), 2, 41, "     = 30", 30, "Blue")
medium_alien = SliderSprite(sprites,(20,14+29),(33,25), 2, 41, "    = 20", 30, "Purple")                     
large_alien = SliderSprite(sprites,(20,14+2*29),(37,25), 2, 41, "    = 10", 30, "Orange")
base_info = SliderSprite(sprites,(24, 157), (49, 29), 1, 0, "Arrows to move   SPACE to Fire   P to Pause/Resume", 30, "lime")
any_key = SliderSprite(None, (0,0), (0,0), 0, 0, "Press any key to start", 40, "White")

setup_intro()

# initialize frame
frame = simplegui.create_frame("Invaders",game.WIDTH, game.HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

frame.start()