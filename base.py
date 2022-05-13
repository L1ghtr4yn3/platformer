import pygame
import random
pygame.init()  
pygame.display.set_caption("easy platformer")  # sets the window title
screen = pygame.display.set_mode((800, 800))  # creates game screen
screen.fill((0,0,0))
clock = pygame.time.Clock() #set up clock
gameover = False #variable to run our game loop

Link = pygame.image.load('dude.png') #load your spritesheet
Link.set_colorkey((255, 255, 255)) #this makes bright pink (255, 0, 255) transparent (sort of

#CONSTANTS
LEFT=0
RIGHT=1
UP = 2
DOWN = 3

#animation variables variables
frameWidth = 16
frameHeight = 16
RowNum = 0 #for left animation, this will need to change for other animations
frameNum = 0
ticker = 0

#player variables
xpos = 500 #xpos of player
ypos = 200 #ypos of player
vx = 0 #x velocity of player
vy = 0 #y velocity of player
keys = [False, False, False, False] #this list holds whether each key has been pressed
isOnGround = False #this variable stops gravity from pulling you down more when on a platform

class platform:
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
    def draw(self, screen):
        pygame.draw.rect(screen, self.color,(self.x, self.y, self.w, self.h))
    def collide(self, xpos, ypos):
        if xpos>self.x and xpos<self.x + self.w and ypos+20>self.y and ypos+20<self.y + self.h:
            return self.y - 20
        else:
            return False
platforms = list()
for _ in range(random.randint(1,8)):
    platforms.append(platform(random.randint(0,700),random.randint(0,700),random.randint(20,50), random.randint(5,20),(random.randint(100,255),random.randint(100,255),random.randint(100,255))))
p1 = platform(100,600, 100, 20,(0,255,255))    
    
    
    
while not gameover: #GAME LOOP############################################################
    clock.tick(60) #FPS
    #Input Section------------------------------------------------------------
    for event in pygame.event.get(): #quit game if x is pressed in top corner
        if event.type == pygame.QUIT:
            gameover = True
     
        if event.type == pygame.KEYDOWN: #keyboard input
            if event.key == pygame.K_ESCAPE:
                gameover = True
            
            if event.key == pygame.K_LEFT:
                keys[LEFT]=True

            elif event.key == pygame.K_UP:
                keys[UP]=True
               
            elif event.key == pygame.K_RIGHT:
                keys[RIGHT]=True
           
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                keys[LEFT]=False

            elif event.key == pygame.K_UP:
                keys[UP]=False
               
            elif event.key == pygame.K_RIGHT:
                keys[RIGHT]= False
         
    #physics section--------------------------------------------------------------------
    #LEFT MOVEMENT
    if keys[LEFT]==True:
        vx=-3
        direction = LEFT
       
    elif keys[RIGHT]==True:
        vx=+3
        direction = RIGHT
    else:
        vx*=.90
    if isOnGround:
        vy = 0
     #ANIMATION-------------------------------------------------------------------
        
    # Update Animation Information
    # Only animate when in motion
    if vx>0:
        RowNum = 0
    if vx < 0: #left animation
        RowNum = 1
        # Ticker is a spedometer. We don't want Link animating as fast as the
        # processor can process! Update Animation Frame each time ticker goes over
        ticker+=1
        if ticker%10==0: #only change frames every 10 ticks
          frameNum+=1
           #If we are over the number of frames in our sprite, reset to 0.
           #In this particular case, there are 10 frames (0 through 9)
        if frameNum>3: 
           frameNum = 0

        if vx>0:
            RowNum = 0
    if vx < 0: #left animation
        RowNum = 0
        # Ticker is a spedometer. We don't want Link animating as fast as the
        # processor can process! Update Animation Frame each time ticker goes over
        ticker+=1
        if ticker%10==0: #only change frames every 10 ticks
          frameNum+=1
           #If we are over the number of frames in our sprite, reset to 0.
           #In this particular case, there are 10 frames (0 through 9)
        if frameNum>3: 
           frameNum = 0
    #turn off velocity
    
        
        #JUMPING
    if keys[UP] == True and isOnGround == True: #only jump when on the ground
        vy = -8
        isOnGround = False
        direction = UP
   
   
    print (isOnGround)
   
    #COLLISION
    if p1.collide(xpos,ypos) != False:
            ypos = p1.collide(xpos,ypos)
            vy = 0
            isOnGround = True
    for i in range(len(platforms)):
        if platforms[i].collide(xpos,ypos) != False:
            ypos = platforms[i].collide(xpos,ypos)
            vy = 0
            isOnGround = True
        #else:
            isOnGround = False
    #stop falling if on bottom of game screen
    if ypos > 760:
        isOnGround = True
        vy = 0
        ypos = 760
   
    #gravity
    if isOnGround == False:
        vy+=.2 #notice this grows over time, aka ACCELERATION
   

    #update player position
    xpos+=vx
    ypos+=vy
   
 
    # RENDER Section--------------------------------------------------------------------------------
           
    screen.fill((0,0,0)) #wipe screen so it doesn't smear
    p1.draw(screen)
    screen.blit(Link, (xpos, ypos), (frameWidth*frameNum, RowNum*frameHeight, frameWidth, frameHeight))
    #red/pink platform
    pygame.draw.circle(screen, (255,0,255), (200, 300), 100)
    for i in range(len(platforms)):
        platforms[i].draw(screen)
   
    pygame.display.flip()#this actually puts the pixel on the screen
   
#end game loop------------------------------------------------------------------------------
pygame.quit()
