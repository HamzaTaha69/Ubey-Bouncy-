import pygame
from pygame.locals import *
from pygame import mixer

pygame.init()

WIDTH = 1000
HEIGHT = 1000

BLUE = 0, 125, 250

direction = " "

game_name = "Uber Bouncy"

FPS = 60

score = 0

loses = 0

start = False

playstart = False

bx = WIDTH / 2 - 50
by = HEIGHT - 200
speed_bx = 0

ball_x = WIDTH / 2 - 50
ball_y = HEIGHT - 800
speed_ball_x = 0
speed_ball_y = 0

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(game_name)

crs = pygame.Rect(5, 5, 5, 5)

board_img = pygame.image.load("img/board.svg")
board_img = pygame.transform.scale(board_img, (100, 20))

board = pygame.Rect(bx, by, 100, 20)

title_screen = pygame.image.load("img/home screen.svg")
title_screen = pygame.transform.scale(title_screen, (WIDTH, HEIGHT))

play_button_img = pygame.image.load("img/play button.svg")
play_button_img = pygame.transform.scale(play_button_img, (200, 100))

play_button = play_button_img.get_rect(center=(WIDTH / 2, HEIGHT - 235))

restart_button_img = pygame.image.load("img/restart button.svg")
restart_button_img = pygame.transform.scale(restart_button_img, (50, 50))

restart_button = restart_button_img.get_rect(center=(100, 100))

home_button_img = pygame.image.load("img/home button.svg")
home_button_img = pygame.transform.scale(home_button_img, (50, 50))

home_button = home_button_img.get_rect(center=(165, 100))

background = pygame.image.load("img/backdrop.svg")
background = pygame.transform.scale(background, (WIDTH * 1.2, HEIGHT * 1.2))

ball_img = pygame.image.load("img/ball.svg")
ball_img = pygame.transform.scale(ball_img, (30, 30))

ball = pygame.Rect(ball_x, ball_y, 30, 30)

def draw_game():
    screen.fill("white")
    screen.blit(background, (-85, 0))
    screen.blit(board_img, (bx, by))
    screen.blit(ball_img, (ball_x, ball_y))
    screen.blit(restart_button_img, (restart_button.x, restart_button.y))
    screen.blit(home_button_img, (home_button.x, home_button.y))
    game_UI()
    pygame.display.update()
    
def draw_home_screen():
    screen.blit(title_screen, (0, 0))
    screen.blit(play_button_img, (play_button.x, play_button.y))
    pygame.display.update()
    
class BoardPhysics():
    def movement(self):
        
        global direction
        global speed_bx
        global bx
        
        mx, my = pygame.mouse.get_pos()
        
        if bx < mx:
            direction = "right"
        else:
            if bx > mx:
                direction = "left"
                
        if direction == "right":
            speed_bx += 1
        else:
            if direction == "left":
                speed_bx -= 1
        
        if board.x > WIDTH - 101:
            if direction == "right":
                speed_bx = 0
            else:
                if board.x < 1:
                    if direction == "left":
                        speed_bx = 0
        
        speed_bx = speed_bx * 0.9
        
        bx += speed_bx
        
        self.x = bx
        self.y = by
        
class BallStuff():
    
    def ball_kill(self):
        
        global loses
        
        if self.y > HEIGHT - 1:
            BallStuff.respawn(ball)
            
            loses += 1
                
    def BallPhysics(self):
        
        global ball_x
        global ball_y
        global speed_ball_x
        global speed_ball_y
        global direction
        global BallSound
        
        BallSound = mixer.Sound("sound/ball bounce.wav")
        
        if not self.colliderect(board):
            speed_ball_y -= 0.455
        else:
            if self.colliderect(board):
                speed_ball_y = 14.555
                
                BallSound.play()
                
        if self.colliderect(board):
            if direction == "right":
                speed_ball_x += 1.5
            else:
                if direction == "left":
                    speed_ball_x -= 1.5
                    
        if ball_x < 1:
            speed_ball_x += 10
        else:
            if ball_x > (WIDTH - 1):
                speed_ball_x -= 10
                
        ball_x += speed_ball_x
        ball_y -= speed_ball_y
                
        self.x = ball_x
        self.y = ball_y

    def respawn(self):
            
        global score
        global ball_x
        global ball_y
        global speed_ball_x
        global speed_ball_y
        global loses
        
        ball_y = HEIGHT - 800
        ball_x = WIDTH / 2 - 50
        speed_ball_y = 0
        speed_ball_x = 0
        score = 0
            
font = pygame.font.SysFont(None, 40)
            
def score_system():
    
    global score
    
    if ball.colliderect(board):
        score += 1
            
def game_UI():
    screen_text = font.render(str(score), True, "BLACK")
    screen.blit(screen_text, (WIDTH / 2 - 5, 100))
    screen_text = font.render("score:", True, "BLACK")
    screen.blit(screen_text, (WIDTH / 2 - 100, 100))
    screen_text = font.render(str(loses), True, "BLACK")
    screen.blit(screen_text, (WIDTH / 2 + 365, 100))
    screen_text = font.render("loses:", True, "BLACK")
    screen.blit(screen_text, (WIDTH / 2 + 275, 100))
    pygame.display.update()

def game_loop():
    
    global start
    global bx
    global playstart
    global score
    global loses
    global BallSound
    
    gameClock = pygame.time.Clock()
    gameRun = True
    while gameRun == True:
        
        BallSound = mixer.Sound("sound/ball bounce.wav")
        
        mx, my = pygame.mouse.get_pos()
        
        gameClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRun = False
                
        crs.x = mx
        crs.y = my
                
        if start == True:
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if crs.colliderect(restart_button):
                    BallStuff.respawn(ball)
                    bx = WIDTH / 2 - 50
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if crs.colliderect(home_button):
                    start = False
            
            playstart = False
            
            score_system()
            BoardPhysics.movement(board)
            BallStuff.BallPhysics(ball)
            BallStuff.ball_kill(ball)
            game_UI()
            draw_game()
        else:
            if start == False:
                
                mixer.music.stop()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if crs.colliderect(play_button):
                        start = True
                        playstart = True
                        BallStuff.respawn(ball)
                        score = 0
                        loses = 0
                        BallSound.play()
                
                draw_home_screen()
                
    pygame.quit()
    
if __name__ == "__main__":
    game_loop()