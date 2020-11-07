import pygame
import time
import random
import os


cwd = os.getcwd()
print(cwd)
pygame.init()
pygame.font.init()
global display_width
global display_height
display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (240,0,0)
blue = (0,0,240)
green = (0,240,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
yellow = (255,255,0)
pink = (255,0,255)
car_width = 25
car_height = 12
meteorHei = 30
meteorWid = 15
spkWid = 68
spkHei = 53
global check_yminMeteor
global check_ymaxMeteor

meteorStartX = []
meteorStartY = []
meteorSpd = []

spikeStartX = []
spikeStartY = []
spikeSpeed = []

scale = []
meteor = cwd + '/meteor.png'
spike = cwd + '/spike.png'
#choose_color = [black,green,blue,red,yellow,pink]
#choose_color = [white,white,white,white,white,white]
car_spd =5
#################################
global gameDisplay
global numb

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Driving Test')
clock = pygame.time.Clock()

carImg = pygame.image.load(cwd + '/car.png')
meteorImg = pygame.image.load(meteor)
spikeImg = pygame.image.load(spike)
def car(x,y):
    gameDisplay.blit(carImg,(x,y))

def text_objects(text, font,color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(text,size,color,textX,textY,delayTime):
    largeText = pygame.font.Font('freesansbold.ttf',size)
    TextSurf, TextRect = text_objects(text, largeText,color)
    TextRect.center = ((display_width/textX),(display_height/textY))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(delayTime)
    
def loadMeteor(pedesx, pedesy):
	#pygame.draw.rect(gameDisplay, white, [pedesx, pedesy,meteorWid,meteorHei])
	gameDisplay.blit(meteorImg,(pedesx,pedesy))	
	
def loadSpike(spkX,spkY):
	#pygame.draw.rect(gameDisplay, white, [spkX, spkY,spkWid,spkHei])
	gameDisplay.blit(spikeImg,(spkX,spkY))
	
def crash():
	message_display('You Crashed',60,red,2,3,2)
	message_display('Press ESC to quit',30,red,2,2.2,1)
	meteorStartX.clear()
	meteorStartY.clear()
	spikeStartX.clear()
	spikeStartY.clear()
	game_intro("Wanna Try Again?")

def score(count):
	font = pygame.font.SysFont(None,25)
	text = font.render("Score : " + str(count), True, black)
	gameDisplay.blit(text,(0,0))

def genMeteor(meteorStartX,meteorStartY,numb):
	for i in range(numb):
		meteorStartX.append(random.randrange(0,display_width))
		meteorStartY.append(random.randrange(-700,-200))
		meteorSpd.append(i)
		scale.append(random.randrange(1,2))

def genSpike(spikeStartX,spk_stary,numb):
	for i in range(numb):
		spikeStartX.append(random.randrange(-700,-200))
		spikeStartY.append(random.randrange(0,display_height))
		spikeSpeed.append(i)
def game_loop():
	global display_width
	global display_height
	global gameDisplay
	global numb
	numb = 3
	start = time.time()
	
	#x = random.randrange((display_width * 0.1),(display_width * 0.8))
	#y = random.randrange((display_height * 0.5),(display_height*0.8))
	x = 300
	y = 300
	x_change = 0
	y_change = 0
	#genMeteor(meteorStartX,meteorStartY,numb)
	#genSpike(spikeStartX,spikeStartY,numb)
	dodged = 0
	gameExit = False
	while not gameExit:
		genMeteor(meteorStartX,meteorStartY,numb)
		genSpike(spikeStartX,spikeStartY,numb)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quitGame()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					y_change = -6
				if event.key == pygame.K_DOWN:
					y_change = 6
				if event.key == pygame.K_LEFT:
					x_change = -car_spd
				if event.key == pygame.K_RIGHT:
					x_change = car_spd
				if event.key == pygame.K_ESCAPE:
					message_display('Exiting...',50,blue,2,3,1)
					#print("Exiting...")
					quitGame()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					x_change = 0
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					y_change = 0
			
		x += x_change
		y += y_change
		gameDisplay.fill(white)
		car(x,y)
		score(dodged)
		if x > display_width - car_width or x < 0 or y <0 or y > display_height - car_width:
			crash()
			game_loop()

		check_collisionMeteor(x,y,numb)
		check_collisionSpike(x,y,numb)
		dodged = int(time.time() -start)
		#print("Dodged = " + str(dodged))
		if(dodged >= 20):
			numb = int(dodged/20)+3
			if(dodged == 20):
				message_display("It's Ok",40,black,2,2.5,0)
				message_display("Difficulty++",30,red,2,2,0)
			elif(dodged == 40):
				message_display("You're good!",40,black,2,2.5,0)
				message_display("Difficulty++",30,red,2,2,0)
			elif(dodged == 60):
				message_display("It's Insane!",40,black,2,2.5,0)
				message_display("Difficulty++",30,red,2,2,0)
			elif(dodged == 80):
				message_display("Wow!Let's Go Pro!",40,black,2,2.5,0)
				message_display("Difficulty++",30,red,2,2,0)
			elif(dodged == 100):
				message_display("Are you in Fast & Furious?",40,black,2,2.5,0)
				message_display("Difficulty++",30,red,2,2,0)
		#print(" Number Object = " + str(numb))
		
		pygame.display.update()
		clock.tick(100)
def check_collisionMeteor(x,y,numb):

	for i in range(numb):
		meteorStartY[i]+=meteorSpd[i]
		loadMeteor(meteorStartX[i],meteorStartY[i])	
		#print(" meteorStartX = " + str(meteorStartX[i]) +", meteorStartY = " + str(meteorStartY[i]))	
		if meteorStartY[i] > display_height:
			meteorStartY[i] = 0 - meteorHei
			meteorStartX[i] = random.randrange(0,display_width-meteorWid)
			meteorSpd[i] +=scale[i]
			if(meteorSpd[i] > 7):
				meteorSpd[i] = 7

		if (meteorStartY[i]+meteorHei/2> y  and meteorStartY[i]-meteorHei/2<y):
			if(x+car_width > meteorStartX[i]-meteorWid and x + car_width < meteorStartX[i]+meteorWid) or (x > meteorStartX[i]-meteorWid and x < meteorStartX[i]+meteorWid):
				#print(" x = " + str(x) +", y = " + str(y))
				crash()
				game_loop()

def check_collisionSpike(x,y,numb):

	for i in range(numb):
		spikeStartX[i]+=spikeSpeed[i]
		loadSpike(spikeStartX[i],spikeStartY[i])
		#print(" spikeStartX = " + str(spikeStartX[i]) +", spikeStartY = " + str(spikeStartY[i]))		
		if spikeStartX[i] > display_width:
			spikeStartX[i] = 0 - spkHei
			spikeStartY[i] = random.randrange(0,display_height-spkHei)
			meteorSpd[i] +=scale[i]
			if(spikeSpeed[i] > 7):
				spikeSpeed[i] = 7
		if (spikeStartX[i]+spkWid/2> x and spikeStartX[i]-spkWid/2<x):
			if(y  > spikeStartY[i]-spkHei/2 and y -car_height*1.5 < spikeStartY[i]+spkHei/2):
				#print(" x = " + str(x) +", y = " + str(y))
				crash()
				game_loop()

def game_intro(text):

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                quitGame()
                
        gameDisplay.fill(white)
        largeText = pygame.font.SysFont("freesansbold.ttf",80)
        TextSurf, TextRect = text_objects(text, largeText,black)
        TextRect.center = ((display_width/2),(display_height/2.8))
        gameDisplay.blit(TextSurf, TextRect)

        button("GO!",150,300,100,50,green,bright_green,game_loop)
        button("Quit",550,300,100,50,red,bright_red,quitGame)

        pygame.display.update()
        clock.tick(100)
		
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("freesansbold.ttf",40)
    textSurf, textRect = text_objects(msg, smallText,black)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)		
def quitGame():
	pygame.quit()
	quit(0)
game_intro("How good can you drive???")
game_loop()
quitGame()
