import pygame
from random import *
import time

#fonction qui definit les positions x et y de l'objet pomme
def apple(window_x,window_y,block_size,snakeLst):
        global x_apple, y_apple
        x_apple=randint(0, window_x-block_size)
        y_apple=randint(0, window_y-block_size)
        for XnY in snakeLst:
            if (x_apple,y_apple)==XnY:
                apple(window_x,window_y,block_size)
        return x_apple, y_apple

#affiche le message lorsque l'on meurt/perd apres avoir pris un m ur on apres s'être mangé soit meme
def end_message(gameDisplay,fontColor,color):
    msg="You lost, q to quit or r to restart, e for main menu"
    font = pygame.font.Font("images/Misc/font.ttf", 50)
    text = font.render(msg, 1, color)
    textpos = text.get_rect()
    textpos.centerx = gameDisplay.get_rect().centerx
    textpos.centery = gameDisplay.get_rect().centery-50
    gameDisplay.fill(fontColor)
    gameDisplay.blit(text, textpos)
    gameDisplay.blit(gameDisplay, (0, 0))
    pygame.display.flip()


#fonction qui affiche ce que l'on voit lorsque l'on clique sur crédits dans le Menu Principal
def credits_jeu(gameDisplay, black, white):
    msg="Everything excepting music was created by"
    font = pygame.font.Font("images/Misc/font.ttf", 40)
    text = font.render(msg, 1, black)
    textpos = text.get_rect()
    textpos.centerx = gameDisplay.get_rect().centerx
    textpos.centery = gameDisplay.get_rect().centery-50
    msg2="Quentin Tourette"
    text2 = font.render(msg2, 1, black)
    textpos2 = text2.get_rect()
    textpos2.centerx = gameDisplay.get_rect().centerx
    textpos2.centery = gameDisplay.get_rect().centery
    msg3="Music Main menu : Arcade Game Menu Music Loop (8Bit Style)"
    text3 = font.render(msg3, 1, black)
    textpos3 = text3.get_rect()
    textpos3.centerx = gameDisplay.get_rect().centerx
    textpos3.centery = gameDisplay.get_rect().centery+50
    msg4="Music In Game : Vexare - The Clockmaker"
    text4 = font.render(msg4, 1, black)
    textpos4 = text4.get_rect()
    textpos4.centerx = gameDisplay.get_rect().centerx
    textpos4.centery = gameDisplay.get_rect().centery+100
    gameDisplay.fill(white)
    gameDisplay.blit(text, textpos)
    gameDisplay.blit(text2, textpos2)
    gameDisplay.blit(text3, textpos3)
    gameDisplay.blit(text4, textpos4)
    gameDisplay.blit(gameDisplay, (0, 0))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type==pygame.KEYDOWN:
                debut_jeu()

#boucle du jeu principal
def jeu(music):
    #init des couleurs
    white = (255,255,255)
    black = (0,0,0)
    red = (200,0,0)
    green = (0,200,0)
    blue = (0,0,200)

    #init pygame + font pour tout ce qui est texte
    pygame.init()
    pygame.font.init()

    #init des variables
    gameExit=False
    test="bonjour cette partie du code vient d'etre activé"
    window_x=1280
    window_y=720
    block_size=17
    x=window_x/2-block_size
    y=window_y/2-block_size
    x_change=0
    y_change=0
    score=1
    direction=0
    vertical=1
    horizontal=1
    global x_apple,y_apple
    x_apple=randint(0, window_x-block_size)
    y_apple=randint(0, window_y-block_size)

    #init de l'horloge de jeu
    clock=pygame.time.Clock()


    gameDisplay = pygame.display.set_mode((window_x,window_y))
    pygame.display.set_caption("SNAKE v3.02")
    pygame.display.update()
    gameExit=False


    background_img = pygame.image.load("images/Backgrounds/Background.png")

    Head_img = pygame.image.load("images/Snake/Head.png")
    Body_img = pygame.image.load("images/Snake/Body.png")
    apple_img = pygame.image.load("images/Misc/apple.png")

    Head_img = pygame.transform.scale(Head_img, (block_size ,block_size))
    Body_img = pygame.transform.scale(Body_img, (block_size ,block_size))

    Music_Menu = pygame.mixer.music.load("music/IG.ogg")
    apple_sound = pygame.mixer.Sound("music/apple_sound.ogg")

    if music:
        pygame.mixer.music.play(-1)
    
    #boucle principale du jeu qui tourne 30*/sec
    while True:
        #creation des listes contenant x y et direction du serpent en dehors de la boucle de jeu pour qu'elle ne soit pas réinit a chaque fois
        snakeDir=[]
        snakeLst=[]
        
        #positionnement de l'objet
        gameDisplay.blit(background_img,(0,0))

        #boucle de jeu qui tourne tant que l'on ne perd pas
        while not gameExit:
            #si le serpent et en dehors des dimensions de la fenetre, fait sortir de la boucle principale après 0.5 secondes
            if x<=0 or x+block_size>window_x or y<=0 or y+block_size>window_y:
                gameExit=True
                time.sleep(0.5)

            #test de la touche sur laquelle l'utilisateur appuie ou s'il appuie sur la croix
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                        
                    if vertical==1:
                        if event.key==pygame.K_UP:
                            y_change=-block_size
                            x_change=0
                            vertical=0
                            horizontal=1
                            direction=1
                            
                        elif event.key==pygame.K_DOWN:
                            y_change=block_size
                            x_change=0
                            vertical=0
                            horizontal=1
                            direction=3
                            
                    if horizontal==1:
                        if event.key==pygame.K_LEFT:
                            x_change=-block_size
                            y_change=0
                            vertical=1
                            horizontal=0
                            direction=4
                            
                        elif event.key==pygame.K_RIGHT:
                            x_change=block_size
                            y_change=0
                            vertical=1
                            horizontal=0
                            direction=2
                    
            #creation d'une liste qui renvoi les position x et ySound( de la tete actuelle afin de les stocker
            snakeHeadPOS = []
            snakeHeadPOS.append(x)
            snakeHeadPOS.append(y)

            snakeLst.append(snakeHeadPOS)
            if len(snakeLst)>score:
                    del snakeLst[0]

            #ajout de la direction que chaque morceaux du corps doit prendre (droite,gauche,haut,bas)
            snakeDir.append(direction)
            if len(snakeDir)>score:
                del snakeDir[0]
            snakeDIR=list(reversed(snakeDir))
            
            #redéfinition des variables x et y, permettant de faire bouger le serpent
            x+=x_change
            y+=y_change

            #test si on se mange soi meme
            for i in range(len(snakeLst)):
                try:
                    if snakeLst[0]==snakeLst[i+1]:
                        gameExit=True
                        time.sleep(0.5)
                except:
                    pass
            
            #remplissage par le fond d'écran pour "redessiner" nos objets dessus
            gameDisplay.blit(background_img, (0, 0), (0, 0, window_x, window_y))

            #création des lists contenant les x et y contenants chaque parties du corps

            snakeHead = snakeHeadPOS
            
            snakeBody = []

            if len(snakeBody)>score+1:
                del snakeBody[0]           

            #rotation de la tete et de la queue                 
            Head_DIR = snakeDIR[0]
            Head_img = pygame.transform.rotate(Head_img, (Head_DIR-1)*90)
            
            #on positionne l'objet corps
            A=0
            for XnY in snakeLst:
                x_Body=int(XnY[0])
                y_Body=int(XnY[1])
                if A==0:
                    pass
                elif A==len(snakeLst):
                    pass
                else:
                    gameDisplay.blit(Body_img,[x_Body,y_Body])
                A+=1

               
            #on positionne l'objet corps
            gameDisplay.blit(Body_img,snakeLst[0])
            
            #on positionne l'objet tete
            gameDisplay.blit(Head_img,[x,y])
            #pygame.draw.rect(gameDisplay, couleur, [x1,y1,block_size,block_size])

            #test si la pomme est mangé, si oui on redefinit de nouvelles coordonnées
            if (x>=x_apple and x<=x_apple+block_size and y>=y_apple and y<=y_apple+block_size) or (x+block_size>=x_apple and x+block_size<=x_apple+block_size and y+block_size>=y_apple and y+block_size<=y_apple+block_size):
                score+=1
                if music:
                    pygame.mixer.Sound.play(apple_sound)
                apple(window_x,window_y,block_size,snakeLst)
                

            #création l'objet pomme
            apple_img = pygame.transform.scale(apple_img, (block_size+2 ,block_size+2))
            gameDisplay.blit(apple_img,[x_apple,y_apple])

            #création l'objet score
            score_message = "Score : " + str(score-1)
            font = pygame.font.Font("images/Misc/font.ttf", 60)
            score_text = font.render(score_message, 1, black)
            gameDisplay.blit(score_text, [0,0])

            #affichage de tout les objets créé jusque la + définition de la répétition de la boucle soit 30X/sec
            pygame.display.update()

            #remise droite de l'image de la tete pour ne pas qu'elle tourne en continu
            Head_img = pygame.transform.rotate(Head_img, -(Head_DIR-1)*90)

            #définition du nombre d'images par seconde (ici 30)
            clock.tick(30)

            
        #boucle qui se lance après qu'on ai perdu, test les touches pour savoir si l'utilisateur veut recommencer ou quitter
        while gameExit:
            end_message(gameDisplay, white, red)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_a:
                        pygame.quit()
                        quit()
                    elif event.key==pygame.K_r:
                        if music:
                            pygame.mixer.fadeout(1000)
                        jeu(music)
                    elif event.key==pygame.K_e:
                        debut_jeu()


#fonction qui définit la fenetre, affiche tout le menu principal et test si l'utilisateur appuie sur l'un des "bouttons" 
def debut_jeu():
    white = (255,255,255)
    black = (0,0,0)
    red = (200,0,0)
    green = (0,200,0)
    blue = (0,0,200)

    pygame.init()
    pygame.font.init()

    test="bonjour cette partie du code vient d'etre activé"

    window_x=1280
    window_y=720

    music=True

    gameDisplay = pygame.display.set_mode((window_x,window_y))
    pygame.display.set_caption("SNAKE v3.02")
    gameExit=False

    Music_Menu = pygame.mixer.music.load("music/Main Menu.ogg")
    pygame.mixer.music.play(-1)
    
    startup = pygame.image.load("images/Backgrounds/Startup.png")
    
    music_button = pygame.image.load("images/Misc/music_button.png")
    button_off = pygame.image.load("images/Misc/button_off.png")

    music_button = pygame.transform.scale(music_button, (50 ,50))
    button_off = pygame.transform.scale(button_off, (50 ,50))
    
    gameDisplay.blit(startup,[0,0])    
    gameDisplay.blit(music_button,[window_x-80,window_y-80])
    pygame.display.update()


    def music_display():
        gameDisplay.blit(startup,[0,0])
        if music:
            gameDisplay.blit(music_button,[window_x-80,window_y-80])
            pygame.display.update()
        if not music:
            gameDisplay.blit(music_button,[window_x-80,window_y-80])
            gameDisplay.blit(button_off,[window_x-80,window_y-80])
            pygame.display.update()
            
    
    #test si l'utilisateur appuie sur la croix ou s'il clic sur l'un des bouttons et lance la commande appropriée
    while True:
        if not music:
            pygame.mixer.music.pause()

        if music:
            pygame.mixer.music.unpause()
                       
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type==pygame.MOUSEBUTTONUP:
                a = list(pygame.mouse.get_pos())
                x=a[0]
                y=a[1]
                if x>=500 and x<=790 and y >=435 and y<=500:
                    pygame.mixer.quit()
                    jeu(music)
                elif x>=515 and x<=780 and y>=530 and y<=600:
                    pygame.quit()
                    quit()
                elif x>=460 and x<=840 and y>=635 and y<=705:
                    credits_jeu(gameDisplay,black,white)
                elif x>=window_x-80 and x<=window_x-30 and y>=window_y-90 and y<=window_y-40 and music==True:
                    music=False
                elif x>=window_x-80 and x<=window_x-30 and y>=window_y-90 and y<=window_y-40 and music==False:
                    music=True
                
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                    
            music_display()            

                    
#lance la fonction qui lance le menu principal soit tout le jeu
#début du jeu
debut_jeu()
