
import math
import pygame
import random
 
BLACK = (0 ,0, 0)
WHITE = (255, 255, 255)
 
class Ball(pygame.sprite.Sprite):
 
   
    def __init__(self):

        super().__init__()
 
       
        self.image = pygame.Surface([10, 10])
 
       
        self.image.fill(WHITE)
 
        
        self.rect = self.image.get_rect()
 
        
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
 
        
        self.speed = 0
 
        
        self.x = 0
        self.y = 0
 
       
        self.direction = 0
 
       
        self.width = 10
        self.height = 10
 
        
        self.reset()
 
    def reset(self):
        self.x = random.randrange(50,750)
        self.y = 350.0
        self.speed=8.0
 
       
        self.direction = random.randrange(-45,45)
 
       
        if random.randrange(2) == 0 :
           
            self.direction += 180
            self.y = 50
 
   
    def bounce(self,diff):
        self.direction = (180-self.direction)%360
        self.direction -= diff
 
        
        self.speed *= 1.1
 
    
    def update(self):
        
        direction_radians = math.radians(self.direction)
 
        
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)
 
        if self.y < 0:
            self.reset()
 
        if self.y > 600:
            self.reset()
 
        
        self.rect.x = self.x
        self.rect.y = self.y
 
        
        if self.x <= 0:
            self.direction = (360-self.direction)%360
            print(self.direction)
           
        
        if self.x > self.screenwidth-self.width:
            self.direction = (360-self.direction)%360
 

class Player(pygame.sprite.Sprite):
   
    def __init__(self, joystick, y_pos):
        
        super().__init__()
 
        self.width=75
        self.height=15
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE)
        self.joystick = joystick
 
        
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
 
        self.rect.x = 0
        self.rect.y = y_pos
 
    
    def update(self):
 
       
        horiz_axis_pos= self.joystick.get_axis(0)
 
        
        self.rect.x=int(self.rect.x+horiz_axis_pos*15)
 
        
        if self.rect.x > self.screenwidth - self.width:
            self.rect.x = self.screenwidth - self.width
 
score1 = 0
score2 = 0
 

pygame.init()
 

screen = pygame.display.set_mode([800, 600])
 

pygame.display.set_caption('Pong')
 

pygame.mouse.set_visible(0)
 

font = pygame.font.Font(None, 36)
 

background = pygame.Surface(screen.get_size())
 

ball = Ball()

balls = pygame.sprite.Group()
balls.add(ball)
 

joystick_count = pygame.joystick.get_count()
if joystick_count < 1:
    
    print ("Error, I didn't find enough joysticks.")
    pygame.quit()
    exit()
else:
    
    joystick1 = pygame.joystick.Joystick(0)
    joystick1.init()
    joystick2 = pygame.joystick.Joystick(1)
    joystick2.init()
 

player1 = Player(joystick1,580)
player2 = Player(joystick2,25)
 
movingsprites = pygame.sprite.Group()
movingsprites.add(player1)
movingsprites.add(player2)
movingsprites.add(ball)
 
clock = pygame.time.Clock()
done = False
exit_program = False
 
while not exit_program:
 
    
    screen.fill(BLACK)
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_program = True
 
    
    if abs(score1 - score2) > 3:
        done = True
 
    if not done:
       
        player1.update()
        player2.update()
        ball.update()
 
    
    if done:
        text = font.render("Game Over", 1, (200, 200, 200))
        textpos = text.get_rect(centerx=background.get_width()/2)
        textpos.top = 50
        screen.blit(text, textpos)
 
    
    if pygame.sprite.spritecollide(player1, balls, False):
        
        diff = (player1.rect.x + player1.width/2) - (ball.rect.x+ball.width/2)
 
        
        ball.y = 570
        ball.bounce(diff)
        score1 += 1
 
    
    if pygame.sprite.spritecollide(player2, balls, False):
        # The 'diff' lets you try to bounce the ball left or right depending where on the paddle you hit it
        diff = (player2.rect.x + player2.width/2) - (ball.rect.x+ball.width/2)
 
        # Set the ball's y position in case we hit the ball on the edge of the paddle
        ball.y = 40
        ball.bounce(diff)
        score2 += 1
 
    
    scoreprint = "Player 1: "+str(score1)
    text = font.render(scoreprint, 1, WHITE)
    textpos = (0, 0)
    screen.blit(text, textpos)
 
    scoreprint = "Player 2: "+str(score2)
    text = font.render(scoreprint, 1, WHITE)
    textpos = (300, 0)
    screen.blit(text, textpos)
 
    
    movingsprites.draw(screen)
 
    
    pygame.display.flip()
     
    clock.tick(30)
 
pygame.quit()
