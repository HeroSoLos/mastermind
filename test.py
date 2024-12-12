import pygame, random, time
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), 
        (255, 255, 0), (255, 0, 255), (0, 255, 255),
        (128, 0, 0), (0, 128, 0), (0, 0, 128)]

class CheckButton:
  def __init__(self, x, y, width, height, text, action):
    self.surface = pygame.Surface((width, height))
    self.rect = pygame.Rect(x, y, width, height)
    self.text = text
    self.action = checkWin
    
  def draw(self, screen):
    pygame.draw.rect(screen, (0, 0, 0), rect=self.rect) 
    screen.blit(textSurface, (self.rect.x+5, self.rect.y))



  def handle_click(self):
    count = None
    mouse_pos = pygame.mouse.get_pos()
    if self.rect.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0]:
            time.sleep(0.2)
            count = self.action()  # Call the action defined on button creation
    
    return count

class MastermindButton:
    

    def __init__(self, x, y, radius, color, yours):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.menu_open = False 
        self.menu_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), 
                           (255, 255, 0), (255, 0, 255), (0, 255, 255),
                           (128, 0, 0), (0, 128, 0), (0, 0, 128)]  
        self.yours = yours

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius) 

        
        mousex, mousey = pygame.mouse.get_pos()
        if self.is_hovering(mousex, mousey) and self.yours:
            cell_size = self.radius*30/50
            menu_x = self.x - 0.9*self.radius
            menu_y = self.y - 0.9*self.radius
            for i in range(3):
                for j in range(3):
                    color_rect = pygame.Rect(menu_x + j * cell_size, menu_y + i * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, self.menu_colors[i * 3 + j], color_rect) 
                    
                    if color_rect.collidepoint(mousex, mousey):
                        if pygame.mouse.get_pressed()[0]:  
                            self.color = self.menu_colors[i * 3 + j]  

    def is_hovering(self, mousex, mousey):
        distance_from_center = ((mousex - self.x) ** 2 + (mousey - self.y) ** 2) ** 0.5
        return distance_from_center <= self.radius

        

answers = [random.choice(colors), random.choice(colors), random.choice(colors), random.choice(colors)]
colorsAns = {(255, 0, 0): 0,
                 (0, 255, 0): 0,
                 (0, 0, 255): 0, 
                 (255, 255, 0): 0,
                 (255, 0, 255): 0,
                 (0, 255, 255): 0,
                 (128, 0, 0): 0, 
                 (0, 128, 0): 0,
                 (0, 0, 128): 0}
for answer in answers:
    colorsAns[answer] += 1

pygame.init()

font = pygame.font.SysFont('Comic Sans MS', 30)
win = pygame.display.set_mode((500, 500))
yawn = pygame.image.load(r"mastermind\yawn.jpg").convert()
yawn = pygame.transform.scale(yawn, (yawn.get_rect().width/3, yawn.get_rect().height/3))

textSurface = font.render('Check', False, (255, 255, 255))
pygame.display.set_caption("masterlose")

xCordinatePosition = 70
yCordinatePosition = 150
mind1 = MastermindButton(xCordinatePosition, yCordinatePosition, 50, (0, 0, 0), True)
mind2 = MastermindButton(xCordinatePosition+110, yCordinatePosition, 50, (0, 0, 0), True)
mind3 = MastermindButton(xCordinatePosition+220, yCordinatePosition, 50, (0, 0, 0), True)
mind4 = MastermindButton(xCordinatePosition+330, yCordinatePosition, 50, (0, 0, 0), True)



mindNodes = [mind1, mind2, mind3, mind4]

statusList = [False, False, False, False]
def checkWin():
    global answers, mindNodes, checks, statusList, ai
    inpColors = {(255, 0, 0): 0,
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
    for i ,mindNode in enumerate(mindNodes):
        inpColors[mindNode.color] += 1
        if (colorsAns[mindNode.color] >= inpColors[mindNode.color]):
            if mindNode.color == answers[i]:
                statusList[i] = 'YES'
                count += 1 
            elif mindNode.color in answers:
                statusList[i] = 'Close'
            else:
                statusList[i] = 'NO'
        else:
            statusList[i] = 'NO'
    ai.check()
    
    checks += 1
    return count
        
check = CheckButton(200, 250, 100, 50, '', checkWin)        
checks = 0


class AI:
    def __init__(self):
        self.colors = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        self.mindNodes = [MastermindButton(xCordinatePosition, yCordinatePosition+250, 50, (0, 0, 0), False),
                          MastermindButton(xCordinatePosition+110, yCordinatePosition+250, 50, (0, 0, 0), False),
                          MastermindButton(xCordinatePosition+220, yCordinatePosition+250, 50, (0, 0, 0), False),
                          MastermindButton(xCordinatePosition+330, yCordinatePosition+250, 50, (0, 0, 0), False)]
        self.result = ['NO', 'NO', 'NO', 'NO']
        self.correct = []
        self.fakeresult = [random.choice(['Close', 'No']), random.choice(['Close', 'No']), random.choice(['Close', 'No']), random.choice(['Close', 'No', 'Yes'])]
    
    def draw(self):
        global win
        global AIturnsTillWin, checks
        if checks > AIturnsTillWin:
            for i, mindNode in enumerate(self.mindNodes):
                mindNode.draw(win)
                textSurfaceAI = font.render('YES', False, (255, 255, 255))
                win.blit(textSurfaceAI, (mindNode.x-25, mindNode.y-25)) 
        elif checks < 2:
            for i, mindNode in enumerate(self.mindNodes):
                mindNode.draw(win)
                textSurfaceAI = font.render(self.result[i], False, (255, 255, 255))
                win.blit(textSurfaceAI, (mindNode.x-25, mindNode.y-25)) 
        else:
            for i, mindNode in enumerate(self.mindNodes):
                mindNode.draw(win)
                textSurfaceAI = font.render(self.fakeresult[i], False, (255, 255, 255))
                win.blit(textSurfaceAI, (mindNode.x-25, mindNode.y-25)) 
            
        
    def moveOne(self):
        self.colors = [(255, 0, 0),
                 (0, 255, 0),
                 (0, 0, 255), 
                 (255, 255, 0)]
        
    def moveTwo(self):
        self.colors = [(255, 0, 255),
                 (0, 255, 255),
                 (128, 0, 0), 
                 (0, 128, 0)]
        
    def moves(self):
        if len(self.correct) == 4:
            return 0#0
        elif len(self.correct) == 3:
            return 1#1
        elif len(self.correct) == 2:
            return 2#2
        elif len(self.correct) == 1:
            return 2#2
        else:
            return 0#0
        
    def check(self):
        global answers
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
                self.correct.append(color)
                
    def win(self):
        return (not 'NO' in self.result)
        

ai = AI()
AIturnsTillWin = 100000
aiWin = False
running = True
while running:
    textSurfaceTwo = font.render(f'Checks Left: {7-checks}', False, (0, 0, 0))
    textSurfaceAITitle = font.render(f'AI:', False, (0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    mousex, mousey = pygame.mouse.get_pos()
   
    win.fill((255, 255, 255))
    
    for mind in mindNodes:
        mind.draw(win)
    check.draw(win)
    
    
    numberOfCorrect = check.handle_click()
    
    for i, status in enumerate(statusList):
        if status == False:
            pass
        else:
            if not mindNodes[i].is_hovering(mousex, mousey):
                textSurfaceFour = font.render(status, False, (0, 0, 0))
                win.blit(textSurfaceFour, (mindNodes[i].x-25, mindNodes[i].y-25)) 
    
    # AI SECTION
    win.blit(textSurfaceAITitle, (25, 300)) 
    ai.draw()
    if not aiWin:
        if checks == 0:
            ai.moveOne()
        elif checks == 1:
            ai.moveTwo()
            AIturnsTillWin = ai.moves() + checks
        else:
            AIturnsTillWin = ai.moves() + checks
            aiWin = True
    
    if numberOfCorrect == 4 and (checks > AIturnsTillWin):
        textSurfaceThree = font.render(f'DRAW, NEXT TIME!!!', False, (0, 0, 0))
        win.blit(textSurfaceThree, (100, 10))
        win.blit(yawn, (150, 150))
        pygame.display.flip()
        time.sleep(5)
        break
    elif numberOfCorrect == 4:
        textSurfaceThree = font.render(f'YOU WIN!!!', False, (0, 0, 0))
        win.blit(textSurfaceThree, (100, 10))
        pygame.display.flip()
        time.sleep(5)
        break
    elif checks > 6 or (checks > AIturnsTillWin):
        textSurfaceThree = font.render(f'YOU LOSE!!!', False, (0, 0, 0))
        win.blit(textSurfaceThree, (100, 10))
        win.blit(yawn, (150, 150))
        pygame.display.flip()
        time.sleep(5)
        break
    else:
        win.blit(textSurfaceTwo, (100, 10))
        
    pygame.display.flip()    
