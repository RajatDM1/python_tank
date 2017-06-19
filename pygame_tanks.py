import pygame
import time
import random

pygame.init()

FPS = 15
white = (255,255,255)
black = (0,0,0)

red = (200,0,0)
light_red = (255,0,0)

yellow = (200,200,0)
light_yellow = (255,255,0)

green = (0,155,0)
light_green = (0,255,0)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Tanks')
pygame.display.update()

clock = pygame.time.Clock()

tankWidth = 40
tankHeight = 20

turretWidth = 5
wheelWidth = 5


smallfont = pygame.font.SysFont(None, 25)
medfont = pygame.font.SysFont(None, 50)
largefont = pygame.font.SysFont(None, 80)

def pause():
    paused = True

    while paused:
        gameDisplay.fill(white)
        message_to_screen("Paused", black, -100, size= "large")
        message_to_screen("Press c to play and q to quit",
                          black,
                          25)
        pygame.display.update()
        clock.tick(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False

                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

                gameDisplay.fill(white)
                message_to_screen("Paused", black, -100, size= "large")
                message_to_screen("Press c to play and q to quit",
                                  black,
                                  25)
                pygame.display.update()
                clock.tick(5)

def score(score):
    text = smallfont.render("Score: "+str(score), True, black)
    gameDisplay.blit(text,[0,0])
    

def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size= "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = ((buttonx + (buttonwidth/2)),(buttony+(buttonheight/2)))
    gameDisplay.blit(textSurf, textRect)
    
    

def message_to_screen(msg,color,y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (display_width/2), (display_height/2)+y_displace
    gameDisplay.blit(textSurf, textRect)

def tank(x,y,turPos):
    x = int(x)
    y = int(y)

    possibleTurrets = [(x-27,y-2),
                       (x-26,y-5),
                       (x-25,y-8),
                       (x-23,y-12),
                       (x-20,y-14),
                       (x-18,y-15),
                       (x-15,y-17),
                       (x-13,y-19),
                       (x-11,y-21)
                       ]

    pygame.draw.circle(gameDisplay, black, (x,y), int(tankHeight/2))
    pygame.draw.rect(gameDisplay, black,( x-tankHeight, y, tankWidth, tankHeight))
    pygame.draw.line(gameDisplay, black, (x,y),possibleTurrets[turPos],turretWidth)
    pygame.draw.circle(gameDisplay, black, (x-15,y+20),wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x-10,y+20),wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x-5,y+20),wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x,y+20),wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x+5,y+20),wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x+10,y+20),wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x+15,y+20),wheelWidth)

    return possibleTurrets[turPos]
  
    
def game_controls():
    gcont = True
    while gcont == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(white)
        message_to_screen("Controls", green , -100, size = "large")
        message_to_screen("Fire: Spacebar", black, -30, "small")
        message_to_screen("Move Turret: Up and Down Arrows", black, 10, "small")
        message_to_screen("Move Tank: Left and Rigt arrows", black, 50, "small")
        message_to_screen("Pause: P", black, 80, "small")
        cur = pygame.mouse.get_pos()
        
        button("play", 150,500,100,50,green,light_green, action = "play")
        button("Main Menu", 350,500,100,50, yellow, light_yellow, action = "main")
        button("quit", 550,500,100,50, red, light_red, action = "quit")

        pygame.display.update()
        clock.tick(FPS)



    
def button(text, x, y, width, height, inactivecolor, activecolor, action):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x +(width) > cur[0] > x and y+height > cur[1] > y:
        pygame.draw.rect(gameDisplay, activecolor, (x,y,width, height))
        if click[0]==1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()
            if action == "controls":
                game_controls()
            if action == "play":
                gameloop()
            if action == "main":
                game_intro()
    else:
        pygame.draw.rect(gameDisplay, inactivecolor, (x,y,width, height))

    text_to_button(text,black,x,y,width,height)
        

def barrier(xlocation, randomHeight, barrier_width):
    pygame.draw.rect(gameDisplay, black, [xlocation, display_height-randomHeight, barrier_width, randomHeight])


def fireshell(xy, tankx, tanky, turPos,gun_power):
    fire = True
    startingShell = list(xy)
    print("Fire")
    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print(startingShell[0],startingShell[1])
        pygame.draw.circle(gameDisplay, green, (startingShell[0],startingShell[1]),5)
        startingShell[0] -= (10-turPos)*2
        startingShell[1] += int((((startingShell[0]-xy[0])*0.01/(gun_power/50))**2) - (turPos+turPos/(12-turPos)))
        if startingShell[1] > display_height or startingShell[0] < 0:
            print("Last  Shell: ", startingShell[0], startingShell[1])
            hit_x = int((startingShell[0]*display_height)/startingShell[1])
            hit_y = int(display_height)
            print("Impact :", hit_x, hit_y)
            fire = False
        pygame.display.update()
        clock.tick(100)
        
    
def power(level):
    text = smallfont.render("Power: "+str(level)+"%", True, black)
    gameDisplay.blit(text,[display_width/2,0])



def game_intro():
    intro = True
    while intro == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                    gameloop()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()


                
        gameDisplay.fill(white)
        message_to_screen("Welcome to TANKS!", green , -100, size = "large")
        message_to_screen("The objective of the game is to shoot and Distroy", black, -30, "small")
        message_to_screen("The enemy tank before they distroy you.", black, 10, "small")
        message_to_screen("The more enemies you destroy the harder they get", black, 50, "small")
        #message_to_screen("Press c to play or q to quit", black, 80, "small")
        cur = pygame.mouse.get_pos()
        
        button("play", 150,500,100,50,green,light_green, action = "play")
        button("Controls", 350,500,100,50, yellow, light_yellow, action = "controls")
        button("quit", 550,500,100,50, red, light_red, action = "quit")

        pygame.display.update()
        clock.tick(FPS)


def gameloop():
    gameExit = False
    gameOver = False
    mainTankX  = display_width*0.9
    mainTankY = display_height*0.7
    tankMove = 0

    currentTurPos = 0
    changeTur= 0
    barrier_width = 50

    fire_power = 50
    power_change = 0

    xlocation = (display_width/2)+ random.randint(-0.2*display_width,0.2*display_width)
    randomHeight = random.randint(display_height*0.1,display_height*0.6)

    
    while not gameExit:
        gameDisplay.fill(white)
        gun = tank(mainTankX, mainTankY, currentTurPos)
        
        while gameOver == True :
            gameDisplay.fill(white)
            message_to_screen("Game over",red,-50, size="large")
            message_to_screen("Press c to play again or q to quit", black, 50)
            pygame.display.update()

            for event in pygame.event.get() :
                if event.type == pygame.QUIT:
                    gameover = False
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameOver = False
                        gameExit = True

                    if event.key == pygame.K_c:
                        gameloop()                       
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                        pause()
                if event.key == pygame.K_LEFT:
                     tankMove = -5
                elif event.key == pygame.K_RIGHT:
                     tankMove = 5
                elif event.key == pygame.K_UP:
                    changeTur = 1
                elif event.key == pygame.K_DOWN:
                    changeTur = -1
                elif event.key == pygame.K_p:
                       pause()
                elif event.key == pygame.K_SPACE:
                    fireshell(gun,mainTankX,mainTankY,currentTurPos,fire_power)
                elif event.key == pygame.K_a:
                    power_change = 1 
                elif event.key == pygame.K_d:
                    power_change = -1

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    tankMove = 0

                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    changeTur = 0

                if event.key == pygame.K_a or event.key == pygame.K_d :
                    power_change = 0
                    

        
        mainTankX += tankMove

        currentTurPos += changeTur
        if currentTurPos > 8:
            currentTurPos = 8
        elif currentTurPos <0:
            currentTurPos = 0

        if mainTankX - (tankWidth/2) < xlocation + barrier_width:
            mainTankX +=5

        fire_power += power_change

        power(fire_power)

        barrier(xlocation, randomHeight, barrier_width)
        
        pygame.display.update()
        clock.tick(FPS)
                

    pygame.quit()
    quit()


    
game_intro()
gameloop()
