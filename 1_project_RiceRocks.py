# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False
level = 1
stages = (5, 10, 15, 25, 30, 35, 50, 75)
game = GameSate()

class GameState:
    def __init__(self)
        self.score = 0
        self lives = 3
        self.time = 0
        self.started = False
        self.level = 1
        self.stages = (5, 10, 15, 25, 30, 35, 50, 75)

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group(canvas, group):
    remove_set = set([])
    for an_object in set(group):
        an_object.draw(canvas)
        an_object.update()
        if an_object.update() == True:
            remove_set.add(an_object)
    group.difference_update(remove_set)
            
def group_collide(group, other_object):
    collision = False
    for an_object in set(group):
        if an_object.collide(other_object) == True:
            explode = Sprite(an_object.get_position(), [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(explode)
            group.remove(an_object)
            collision = True
    return collision
    
def group_group_collide(r_group, m_group):
    global score
    for r in set(r_group):
        if group_collide(m_group, r) == True:
            r_group.discard(r)
            score += 1
        
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos

    def draw(self,canvas):
        if self.thrust == True:
            canvas.draw_image(self.image, (self.image_center[0] + self.image_size[0], self.image_center[1]), self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)


    # define keyhandlers to control ship thrust
    def start_thrust(self):
        self.thrust = True
        ship_thrust_sound.rewind()
        ship_thrust_sound.play()

    def stop_thrust(self):
        self.thrust = False
        ship_thrust_sound.pause()

    # define keyhandlers to control ship_angle
    def turn_right(self):
        self.angle_vel = .05

    def turn_left(self):
        self.angle_vel = -.05

    def stop_turn(self):
        self.angle_vel = 0

    # define keyhandlers to control missile
    def shoot(self):
#        a_missile = Sprite(my_ship.pos, my_ship.vel, my_ship.angle, 0, missile_image, missile_info, missile_sound)
        firing_angle = angle_to_vector(self.angle)
        missile_pos = list(self.pos)
        missile_vel = list(self.vel)
        for i in range(2):
            missile_pos[i] = self.pos[i] + self.radius * firing_angle[i] 
            missile_vel[i] = self.vel[i] + 8 * firing_angle[i]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)

    def update(self):
        dimension = [WIDTH, HEIGHT]
        vel_incr = 0.01
        forward = angle_to_vector(self.angle)
        
        # update angle for ship
        self.angle += self.angle_vel
        
        for i in range(2):
            # update position for ship
            self.pos[i] = (self.pos[i] + self.vel[i]) % dimension[i]

            # update velocity for ship
            if self.thrust:
                self.vel[i] += forward[i] * .1
            self.vel[i] *= (1 - vel_incr)

            
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
    
    def update(self):
        dimension = [WIDTH, HEIGHT]
        
        # update angle
        self.angle += self.angle_vel

        # update position
        for i in range(2):
            self.pos[i] += self.vel[i]
            self.pos[i] = self.pos[i] % dimension[i] 

        # update age
        self.age += 1
        return self.age >= self.lifespan           
          
    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos

    def collide(self, other_object):
        return dist(self.pos, other_object.pos) <= self.radius + other_object.get_radius()
    
    def draw(self, canvas):
        global time
        explosion_dimension = [self.lifespan, 1]
        explosion_index = [time % explosion_dimension[0], (time // explosion_dimension[0]) % explosion_dimension[1]]
        if self.animated == True:
            canvas.draw_image(self.image, 
                    (self.image_center[0] + explosion_index[0] * self.image_size[0], 
                     self.image_center[1] + explosion_index[1] * self.image_size[1]), 
                     self.image_size, self.pos, self.image_size, self.angle)
            time += 1
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
def draw(canvas):
    global time, started, lives
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")

    
    # draw ship and sprites
    my_ship.draw(canvas)
    
    # update ship and sprites
    my_ship.update()

    # draw and update rock sprites
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)
    process_sprite_group(canvas, explosion_group)

    # adjust live score when ship collides with rocks
    if group_collide(rock_group, my_ship) == True:
        lives -= 1
    
    # detect missiles hitting rocks
    group_group_collide(rock_group, missile_group)
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                          splash_info.get_size())
    if lives <= 0:
        started = False
        for rock in rock_group:
            rock_group.discard(rock)
        soundtrack.pause()

            
# timer handler that spawns a rock
def rock_spawner():
    global a_rock, level
    if started == True:
        asteroid_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        asteroid_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
        asteroid_avel = random.random() * .2 - .1
        if score in stages:
            level += 1
        a_rock = Sprite(asteroid_pos, (asteroid_vel[0] * level, asteroid_vel[1] * level), 0, asteroid_avel, asteroid_image, asteroid_info)
        if (len(rock_group) < 12) and (dist(my_ship.pos, asteroid_pos) > 2 * my_ship.radius):
            rock_group.add(a_rock)
        
def keydown(key):
    for i in starts:
        if key == simplegui.KEY_MAP[i]:
            starts[i]()

def keyup(key):
    for i in stops:
        if key == simplegui.KEY_MAP[i]:
            stops[i]()

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score, level
    lives = 3
    score = 0
    level = 1
    soundtrack.rewind()
    soundtrack.play()
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# Inputs for keyboard handlers.
starts = {"right": my_ship.turn_right,
           "left": my_ship.turn_left,
           "up": my_ship.start_thrust,
           "space": my_ship.shoot}
stops = {"up": my_ship.stop_thrust,
           "right": my_ship.stop_turn,
           "left": my_ship.stop_turn}

# register handlers
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
rock_group = set([])
missile_group = set([])
explosion_group = set([])
timer.start()
frame.start()
