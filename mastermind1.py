import pygame, random, time

#Colors and answers
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), 
        (255, 255, 0), (255, 0, 255), (0, 255, 255),
        (128, 0, 0), (0, 128, 0), (0, 0, 128)]
answers = [random.choice(COLORS), random.choice(COLORS), random.choice(COLORS), random.choice(COLORS)]
# This dictionary is used to keep track of how many of each color there is. Specifically in the answers
colorsAns = {(255, 0, 0): 0,
                 (0, 255, 0): 0,
                 (0, 0, 255): 0, 
                 (255, 255, 0): 0,
                 (255, 0, 255): 0,
                 (0, 255, 255): 0,
                 (128, 0, 0): 0, 
                 (0, 128, 0): 0,
                 (0, 0, 128): 0,
                 (0, 0, 0): 0}
for answer in answers:
    colorsAns[answer] += 1 # Adds the correct values to color ans

#Default Cords
xCoordinatePosition = 70
yCoordinatePosition = 150

# status
statusList = [False, False, False, False]

# Classes
class CheckButton: # Made for the check button
    def __init__(self, x, y, width, height):
        self.surface = pygame.Surface((width, height)) # for collosions
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), rect=self.rect) # draw the rectangle at the rectangles coordinates
        textSurface = font.render('Check', False, (255, 255, 255))  # create a font object
        screen.blit(textSurface, (self.rect.x+5, self.rect.y)) # add the font object onto the screen at the same spot as the rectangle

    def handle_click(self): # handles clicks
        count = None
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos): # only work if its colliding first
            if pygame.mouse.get_pressed()[0]: # checks for left click [0] = left
                time.sleep(0.2) # sleeps so u dont accidentally use all your checks
                count = self.checkWin() # call the checkwin to evaluate your answers
        return count
    
    def checkWin(self): # evaluates answers
        global answers, mindNodes, checks, statusList, ai # Use global since they are outside of the class scope
        inpColors = {(255, 0, 0): 0, # Dictionary to store the amount of guesses for each colors
                    (0, 255, 0): 0,
                    (0, 0, 255): 0, 
                    (255, 255, 0): 0,
                    (255, 0, 255): 0,
                    (0, 255, 255): 0,
                    (128, 0, 0): 0, 
                    (0, 128, 0): 0,
                    (0, 0, 128): 0,
                    (0, 0, 0): 0}
        count = 0
        for i, mindNode in enumerate(mindNodes): # loop through all your mindnodes
            # Line below is made so you can detect duplicates
            inpColors[mindNode.color] += 1 # Add it to the inpColors so you know how many times the user used that color
            if (colorsAns[mindNode.color] >= inpColors[mindNode.color]): # If you haven't guessed that color more than the amount it shows up, purpose is to prevent you from playing the same color all four times and having the code say your close for each one
                if mindNode.color == answers[i]: # if the color of the mindnode is equal to the answer
                    statusList[i] = 'YES' # Status is set to yet, status is like the text it should draw on top
                    count += 1 # increase count so you know when you win, (win = 4)
                elif mindNode.color in answers: # if its in the list, then you have the right color
                    statusList[i] = 'Close' # Set to close so you know its in the list
                else:
                    statusList[i] = 'NO' # Set 'NO' since it's clearly not in the list
            else:
                statusList[i] = 'NO' # No incase you spammed it. This signifies that there isn't double/triple/quadruple of one color
        ai.check() # check the AI also
        
        checks += 1 # Add one to checks since you should lose after using 7 (AI wins in 5 so this never happens but still)
        return count # return count to use in the main function

class MastermindButton: # Node class
    def __init__(self, x, y, radius, color, yours): # set position & basic shape
        self.x = x 
        self.y = y
        self.radius = radius
        self.color = color
        self.menuColors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), # values for the menu 
                           (255, 255, 0), (255, 0, 255), (0, 255, 255),
                           (128, 0, 0), (0, 128, 0), (0, 0, 128)]  
        self.yours = yours # is it yours or does it belong to the AI

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius) # always draw the circle with the values given

        mouseX, mouseY = pygame.mouse.get_pos() # get mouse position
        if self.is_hovering(mouseX, mouseY) and self.yours: # If its yours and your hovering over it
            cell_size = self.radius*30/50 # these values are used to that you can draw the cell_size correctly
            menu_x = self.x - 0.9*self.radius
            menu_y = self.y - 0.9*self.radius
            for i in range(3): # 3x3 grid so use 2 for loops
                for j in range(3):
                    # the rectangles position is the initial x+j*cellsize. we do j*cellsize so you can add the same distance each iteration. Same principle for i
                    color_rect = pygame.Rect(menu_x + j * cell_size, menu_y + i * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, self.menuColors[i * 3 + j], color_rect)  # draw the rectangle created above. Its color is equal to its position
                    if color_rect.collidepoint(mouseX, mouseY): # If its colliding with the rectangle (individual color)
                        if pygame.mouse.get_pressed()[0]: # left click 
                            self.color = self.menuColors[i * 3 + j]  # set the color equal to the one your pressing

    def is_hovering(self, mouseX, mouseY): # check for hovering
        distance_from_center = ((mouseX - self.x) ** 2 + (mouseY - self.y) ** 2) ** 0.5 # distance formula
        return distance_from_center <= self.radius # when its smaller than radius that means your inside

class AI:
    def __init__(self):
        self.colors = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)] # default node colors
        self.mindNodes = [MastermindButton(xCoordinatePosition, yCoordinatePosition+250, 50, (0, 0, 0), False),
                          MastermindButton(xCoordinatePosition+110, yCoordinatePosition+250, 50, (0, 0, 0), False),
                          MastermindButton(xCoordinatePosition+220, yCoordinatePosition+250, 50, (0, 0, 0), False),
                          MastermindButton(xCoordinatePosition+330, yCoordinatePosition+250, 50, (0, 0, 0), False)]
        self.result = ['NO', 'NO', 'NO', 'NO'] # default results
        self.correct = [] # used for the 'ai'
        self.fakeResult = [random.choice(['Close', 'No', 'Yes']), random.choice(['Close', 'No', 'Yes']), random.choice(['Close', 'No']), random.choice(['Close', 'No', 'Yes'])] # fake results since i didn't want to code real ai to guess
    
    def draw(self):
        global win # global war since its not within class scope
        global AIturnsTillWin, checks
        if checks > AIturnsTillWin: # If AIwins
            for i, mindNode in enumerate(self.mindNodes): # change each mindnode to YES
                mindNode.draw(win)
                textSurfaceAI = font.render('YES', False, (255, 255, 255))
                win.blit(textSurfaceAI, (mindNode.x-25, mindNode.y-25)) 
        elif checks < 2: # If there is less than 2 checks draw the results of itself (colors are preset)
            for i, mindNode in enumerate(self.mindNodes):
                mindNode.draw(win)
                textSurfaceAI = font.render(self.result[i], False, (255, 255, 255))
                win.blit(textSurfaceAI, (mindNode.x-25, mindNode.y-25)) 
        else:
            for i, mindNode in enumerate(self.mindNodes): # If checks inbetween the two, then draw a fake result
                mindNode.draw(win)
                textSurfaceAI = font.render(self.fakeResult[i], False, (255, 255, 255))
                win.blit(textSurfaceAI, (mindNode.x-25, mindNode.y-25)) 
            
        
    def moveOne(self): # move one is preset to the first 4 colors
        self.colors = [(255, 0, 0),
                 (0, 255, 0),
                 (0, 0, 255), 
                 (255, 255, 0)]
        
    def moveTwo(self): # move two is preset to the next 4 colors
        self.colors = [(255, 0, 255),
                 (0, 255, 255),
                 (128, 0, 0), 
                 (0, 128, 0)]
        
    def moves(self): # every move after that just sees how many correct it knows. I put in the variables based on how many turns i would figure it out in
        if len(self.correct) == 4:
            return 0
        elif len(self.correct) == 3:
            return 1
        elif len(self.correct) == 2:
            return 2
        elif len(self.correct) == 1:
            return 2
        else:
            return 0
        
    def check(self): # this is the AI check
        global answers # functions are really similar to the check
        AIinpColors = {(255, 0, 0): 0,
                 (0, 255, 0): 0,
                 (0, 0, 255): 0, 
                 (255, 255, 0): 0,
                 (255, 0, 255): 0,
                 (0, 255, 255): 0,
                 (128, 0, 0): 0, 
                 (0, 128, 0): 0,
                 (0, 0, 128): 0,
                 (0, 0, 0): 0}
        # same things but instead of using global mindnodes, use the AI's nodes
        for i ,color in enumerate(self.colors):
            AIinpColors[color] += 1
            if (colorsAns[color] >= AIinpColors[color]):
                if color == answers[i]:
                    self.result[i] = 'YES' 
                elif color in answers:
                    self.result[i] = 'Close'
                else:
                    self.result[i] = 'NO'
            else:
                self.result[i] = 'NO'

            if not self.result[i] == 'NO' and (not color in self.correct):
                self.correct.append(color) # if its correct, append to correct so the AI knows which ones are right
                
    def win(self):
        return (not 'NO' in self.result) # unfortunately this line is useless, kept it since it was a good concept and might reuse in the future

# pygame initialization
pygame.init()
font = pygame.font.SysFont('Comic Sans MS', 30) # set font
win = pygame.display.set_mode((500, 500)) # create window

pygame.display.set_caption("MasterLoss") # set name of window

checks = 0

#Create CheckButton, x=200, y=250, width=100, height=50
check = CheckButton(200, 250, 100, 50)        

# Masterminds; Xord, Yord, radius, start color, yours

mind1 = MastermindButton(xCoordinatePosition, yCoordinatePosition, 50, (0, 0, 0), True) 
mind2 = MastermindButton(xCoordinatePosition+110, yCoordinatePosition, 50, (0, 0, 0), True)
mind3 = MastermindButton(xCoordinatePosition+220, yCoordinatePosition, 50, (0, 0, 0), True)
mind4 = MastermindButton(xCoordinatePosition+330, yCoordinatePosition, 50, (0, 0, 0), True)
mindNodes = [mind1, mind2, mind3, mind4]

ai = AI()
AIturnsTillWin = 100000 # set to a large number so the AI won't just win instantly and it needs time to calculate 
aiWin = False

running = True
while running:
    textSurfaceChecks = font.render(f'Checks Left: {7-checks}', False, (0, 0, 0)) # Title
    textSurfaceAITitle = font.render(f'AI:', False, (0, 0, 0)) # AI text 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # When you press the x it'll close
    
    mouseX, mouseY = pygame.mouse.get_pos() # get the mouse position
   
    win.fill((255, 255, 255)) # set background to white
    
    for mind in mindNodes:
        mind.draw(win) # draw each mindnode
    check.draw(win) # draw the check button
    
    
    numberOfCorrect = check.handle_click() # check if the check button is clicked
    
    for i, status in enumerate(statusList):
        if status == False: # draw the statuses
            pass
        else:
            if not mindNodes[i].is_hovering(mouseX, mouseY):
                textSurfaceFour = font.render(status, False, (0, 0, 0))
                win.blit(textSurfaceFour, (mindNodes[i].x-25, mindNodes[i].y-25)) 
    
    # AI SECTION
    win.blit(textSurfaceAITitle, (25, 300)) # draw the AI text title
    ai.draw() # draw the AI mindnodes
    if checks == 0:
        ai.moveOne() # play move 1
    elif checks == 1: 
        ai.moveTwo() # play move 2
        AIturnsTillWin = ai.moves() + checks # calculate how many moves to win
    else:
        if ((ai.moves() + checks) < AIturnsTillWin): # if u can win faster then change it. ONLY after move 2
            AIturnsTillWin = ai.moves() + checks
    
    if numberOfCorrect == 4 and (checks > AIturnsTillWin): # if four is correct but AI is also correct, then its a draw
        textSurfaceThree = font.render(f'DRAW, NEXT TIME!!!', False, (0, 0, 0))
        win.blit(textSurfaceThree, (100, 10))
        pygame.display.flip() # update screen
        time.sleep(5)
        break
    
    elif numberOfCorrect == 4: # If you win
        textSurfaceThree = font.render(f'YOU WIN!!!', False, (0, 0, 0)) # you win
        win.blit(textSurfaceThree, (100, 10))
        pygame.display.flip()
        time.sleep(5)
        break
    
    elif checks > 6 or (checks > AIturnsTillWin): # if you lost to ai, or u ran out of checks
        textSurfaceThree = font.render(f'YOU LOSE!!!', False, (0, 0, 0)) # you lose
        win.blit(textSurfaceThree, (100, 10))
        pygame.display.flip()
        time.sleep(5)
        break
    else:
        win.blit(textSurfaceChecks, (100, 10))
        
    
    pygame.display.flip()  # update screen
