import pygame
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 15)

class QuadTree:

    max_level = 5
    max_points = 4

    def __init__(self, x, y, widht, height, color = (0,255,20), level = 0, mother = None):
        self.mother: QuadTree = mother #None = root
        self.x = x
        self.y = y
        self.w = widht
        self.h = height
        self.leafs = [[None, None],[None, None]]
        self.level = level
        self.divided = False
        self.color = color

        self.points = []
        self.total = 0

    def addPoint(self, pos):
        self.insert(pos)

    def removePoint(self, pos):
        self.remove(pos)

    def insert(self, pos):
        if not self.divided:
            self.points.append(pos)
            self.total += 1
            if len(self.points) == self.max_points and self.level < self.max_level:
                self.divide()
        else:
            half_w = self.w // 2
            half_h = self.h // 2

            destin = [0,0]
            
            if(pos[0] - self.x >= half_w):
                destin[1] = 1
            if(pos[1] - self.y >= half_h):
                destin[0] = 1

            self.leafs[destin[0]][destin[1]].insert(pos)
            self.total += 1

    def remove(self, pos):
        if not self.divided:
            if len(self.points) == 0:
                return
            self.points.pop()
            self.diminute()
        else:
            half_w = self.w // 2
            half_h = self.h // 2

            destin = [0,0]
            
            if(pos[0] - self.x >= half_w):
                destin[1] = 1
            if(pos[1] - self.y >= half_h):
                destin[0] = 1

            self.leafs[destin[0]][destin[1]].remove(pos)

    def diminute(self):
        self.total -= 1

        if(self.divided and self.total < self.max_points):
            self.undivide()
        
        if self.mother == None:
            return
        self.mother.diminute()

    def divide(self):
        half_w = self.w // 2
        half_h = self.h // 2
        
        self.leafs[0][0] = QuadTree(self.x, self.y, half_w, half_h,(100,255,0), self.level + 1, self)
        self.leafs[0][1] = QuadTree(self.x + half_w, self.y, self.w - half_w, half_h,(100,100,100), self.level + 1, self)
        self.leafs[1][0] = QuadTree(self.x, self.y + half_h, half_w, self.h - half_h,(200,10,10), self.level + 1, self)
        self.leafs[1][1] = QuadTree(self.x + half_w, self.y + half_h, self.w - half_w, self.h - half_h,(0,40,200), self.level + 1, self)

        self.divided = True
        self.total = 0
        for point in self.points:
            self.insert(point)

    def undivide(self):
        self.divided = False

        points = []
        points += self.leafs[0][0].points.copy()
        points += self.leafs[0][1].points.copy()
        points += self.leafs[1][0].points.copy()
        points += self.leafs[1][1].points.copy()

        self.points = points

        self.leafs = [[None, None],[None, None]]

    def update(self):
        pass

    def render(self, canvas: pygame.Surface):
        pygame.draw.rect(canvas, self.color, (self.x, self.y, self.w, self.h), 1)
        
        text = font.render(str(self.level)+ ': ' + str(self.total), False, self.color)
        canvas.blit(text, (self.x + (self.w//2), self.y + 5))
        
        if(self.divided):
            self.leafs[0][0].render(canvas)
            self.leafs[0][1].render(canvas)
            self.leafs[1][0].render(canvas)
            self.leafs[1][1].render(canvas)
        else:
            for point in self.points:
                pygame.draw.circle(canvas, (255,255,255) ,point,2)
