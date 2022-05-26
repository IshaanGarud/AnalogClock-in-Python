import PyGameEngine as engine
# make sure to install PyGameEngine.py (for more info check) in the same folder and same name
import pygame, sys, math, datetime

pygame.init()

WIDTH, HEIGHT, FPS = 690, 800, 60
AVG = min(WIDTH, HEIGHT)

window = engine.Window(WIDTH, HEIGHT, FPS)
window.set_window()
screen = window.win_return()[0]
screen_rect = window.win_return()[1]

clock = window.set_clock()

bg = engine.Background(WIDTH, HEIGHT, FPS)
bg.screen = screen

COLOURS = {"white": (250, 250, 250),
           "black": (0, 0, 0),
           "gray": (25, 25, 25),
           "l_gray": (150, 150, 150),
           "bg": (25, 25, 75),
           "red": (215, 65, 90),
           "green": (65, 215, 90),
           "d_green": (50, 190, 100),
           "blue": (100, 100, 255)}

myfont = pygame.font.SysFont("Arial", 20)
facefont = pygame.font.SysFont("Times New Roman", 30, 1)
datefont = [pygame.font.SysFont("msgothic", 20, 1, 1), pygame.font.SysFont("msgothic", 30, 1, 1)]

sec_angle = 0
min_angle = 0
hour_angle = 0
Meridian = None
column = 0

class Hands:
    def __init__(self, angle, r, colour):
        self.angle = angle
        self.r = round((AVG*r)/690)   # Multiplying by round((WIDTH*r)/690) adjusts the length of all Hands , no matter the width of the window
        self.colour = colour
        self.width = 3

    def move(self):
        self.x = (math.cos(math.radians(self.angle - 90)) * self.r + screen_rect.w // 2)
        self.y = (math.sin(math.radians(self.angle - 90)) * self.r + screen_rect.h // 2)

    def draw(self):
        self.hand = pygame.draw.line(screen, self.colour, screen_rect.center, (self.x, self.y), self.width)


while True:
    bg.solid_color(50, 50, 100)
    frame = pygame.draw.circle(screen, COLOURS["white"], screen_rect.center, round((AVG*350)/690), 3)

    for i in range(1, 13):                  # Controls the Numbers on Clock face
        ix = math.cos(math.radians((i*30)-90))*round((AVG*325)/690) + screen_rect.w//2    # Multiplying by round((AVG*325)/690) adjusts the location of numbers , no matter the width of the window
        iy = math.sin(math.radians((i*30)-90))*round((AVG*325)/690) + screen_rect.h//2
        num = facefont.render(str(i), 1, (255, 255, 255))
        screen.blit(num, [ix-12, iy-12])

    current_time = datetime.datetime.now()
    sec_angle = current_time.second * (360 / 60)  # 1sec is divided in 60 parts
    min_angle = current_time.minute * (360 / 60)  # 1min is divided in 60 parts
    hour_angle = current_time.hour * (360 / 12)  # 1hr is divided in 12 parts

    if (current_time.hour - 12) < 0:    #Decides the Time of Day i.e. AM or PM
        Meridian = "AM"
    else:
        Meridian = "PM"

    face_digital = {"weekday": current_time.strftime("%a"),
                    "month": current_time.strftime("%b"),
                    "date": current_time.strftime("%d"),
                    "year": current_time.strftime("%Y")}

    # This one's a one-liner
    dateObj = screen.blit(datefont[1].render(face_digital["date"], 1, COLOURS["white"]), [screen_rect.w*(4/5), screen_rect.h//2-datefont[1].size(face_digital["date"])[0]//3])    # Displays the date on the screen (don't question why its so big, I wanted  to fit everything in a line)
    weekdayObj = screen.blit(datefont[0].render(face_digital["weekday"], 1, COLOURS["white"]), [screen_rect.w*(1/5), screen_rect.h//2-datefont[0].size(face_digital["weekday"])[0]])    # Displays the weekday on the screen.
    monthObj = screen.blit(datefont[0].render(face_digital["month"], 1, COLOURS["white"]), [screen_rect.w*(1/5), screen_rect.h//(1.9)])    # Displays the month on the screen.
    yearObj = screen.blit(datefont[1].render(face_digital["year"], 1, COLOURS["white"]), [screen_rect.w//2-datefont[1].size(face_digital["year"])[0]//2, screen_rect.h//2+datefont[1].size(face_digital["year"])[0]*2])   # Displays the year on the screen.

    elems = [dateObj, weekdayObj, monthObj, yearObj]
    for elem in elems:
        elem.w += 1
        elem.h += 1
        elem.x -= 5
        elem.y -= 1
        pygame.draw.rect(screen, COLOURS["white"], elem, 2)

    sec_hand = Hands(sec_angle, 325, COLOURS["red"])
    min_hand = Hands(min_angle, 300, COLOURS["white"])
    hour_hand = Hands(hour_angle, 200, COLOURS["l_gray"])
    hour_hand.width = 8

    sec_hand.move(), sec_hand.draw()
    min_hand.move(), min_hand.draw()
    hour_hand.move(), hour_hand.draw()

    time24 = str(current_time.hour) + ": " + str(current_time.minute) + ": " + str(current_time.second)
    time12 = str(abs(current_time.hour - 12)) + ": " + str(current_time.minute) + ": " + str(current_time.second) + Meridian
    digi_time24 = myfont.render(time24, 1, (255, 255, 255))
    digi_time12 = myfont.render(time12, 1, (255, 255, 255))

    screen.blit(digi_time24, [0, 0])
    screen.blit(digi_time12, [0, 25])
    pygame.draw.line(screen, COLOURS["white"], (0, 22), (100, 22))

    # I hated to use too many lines so I just wrote 3 lines in one :)
    screen.blit(pygame.font.SysFont("Arial", 10).render("Made by Ishaan Garud!", 1, COLOURS["white"]), [WIDTH - pygame.font.SysFont("Arial", 10).size("Made by Ishaan Garud!")[0], 0])

    window.ifQuit()
    pygame.display.update()
    clock.tick(FPS)
