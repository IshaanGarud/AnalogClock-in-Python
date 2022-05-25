import PyGameEngine as engine
# make sure to install PyGameEngine.py (for more info check) in the same folder and same name

import pygame, sys, math, datetime

pygame.init()

WIDTH, HEIGHT, FPS = 690, 1485, 60

window = engine.Window(WIDTH, HEIGHT, FPS)
window.set_window()
screen = window.win_return()[0]
screen_rect = window.win_return()[1]

clock = window.set_clock()

bg = engine.Background(WIDTH, HEIGHT, FPS)
bg.screen = screen


COLOURS = {"white":(250, 250, 250),
            "black": (0, 0, 0),
            "gray": (25, 25, 25),
            "l_gray": (150, 150, 150),
            "bg": (25, 25, 75), 
            "red": (215, 65, 90),
            "green": (65, 215, 90),
            "d_green": (50, 190, 100),
            "blue": (100, 100, 255)}

myfont = pygame.font.SysFont("Arial", 30)

sec_angle = 0
min_angle = 0
hour_angle = 0
Meridian = None      
                                    
class Hands:
    def __init__(self, angle, r, colour):     
        self.angle = angle           
        self.r = r      
        self.colour = colour
        self.width = 5
    
    def move(self):
        self.x = (math.cos(math.radians(self.angle-90)) * self.r + screen_rect.w//2)
        self.y = (math.sin(math.radians(self.angle-90)) * self.r + screen_rect.h//2)
            
    def draw(self):
        self.hand = pygame.draw.line(screen, self.colour, screen_rect.center, (self.x, self.y), self.width)
        
          
                                              
while True:
    bg.solid_color(50, 50, 100)
    
    #sec_x = math.cos(math.radians(angle)) * orbit_r_x
    #sec_y = math.sin(math.radians(angle)) * orbit_r_y
    
    frame = pygame.draw.circle(screen, COLOURS["d_green"], screen_rect.center, 350, 6)
    
    sec_hand = Hands(sec_angle, 325, COLOURS["red"])
    min_hand = Hands(min_angle, 300, COLOURS["white"])
    hour_hand = Hands(hour_angle, 200, COLOURS["l_gray"])
    hour_hand.width = 8

    sec_hand.move(), sec_hand.draw()
    min_hand.move(), min_hand.draw()
    hour_hand.move(), hour_hand.draw()
    
    
    current_time = datetime.datetime.now()
    
    sec_angle = current_time.second * (360/60)    # 1sec is divided in 60 parts
    min_angle = current_time.minute * (360/60)    #1min is divided in 60 parts
    hour_angle = current_time.hour * (360/12)    #1hr is divided in 12 parts
   
    if (current_time.hour-12) < 0:
        Meridian = "AM"
    else:
        Meridian = "PM"
   
    time24 = str(current_time.hour)+ ": " + str(current_time.minute) + ": " + str(current_time.second)    
    time12 = str(abs(current_time.hour-12))+ ": " + str(current_time.minute) + ": " + str(current_time.second)+ Meridian  
    digi_time24 = myfont.render(time24, 1, (255, 255, 255))
    digi_time12 = myfont.render(time12, 1, (255, 255, 255))
 
    screen.blit(digi_time24, [0, 0])
    screen.blit(digi_time12, [0, 50])
    pygame.draw.line(screen, COLOURS["white"], (0, 40), (150, 40), 5)
    
    window.ifQuit()
    pygame.display.update()
    clock.tick(FPS)            
