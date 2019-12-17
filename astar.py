import pygame
import numpy as np
import sys

class Node:
    def __init__(self, x, y, s, g=None, h=None):
        self.x = x
        self.y = y
        self.val = s
        self.walkable = s != 3

        self.g = g
        self.h = h
        self.parent = None

    def set_g(self, g):
        self.g = g

    def set_h(self, h):
        self.h = h

    @property
    def f(self):
        return self.g + self.h

class Grid:
    def __init__(self, x, y, w):
        self.x = x - (x % w)
        self.y = y - (y % w)
        self.w = w
        self.grid = [[Node(j, i, 0) for j in range(x//w)] for i in range(y//w)]

    def __iter__(self):
        return self

    def __next__(self):
        return self

    def get_neighbours(self):
        x = self.current.x
        y = self.current.y

        contenders = [
            [x+1, y],
            [x-1, y],
            [x, y+1],
            [x, y-1]
        ]

        return filter(lambda i: self.grid[i[1]][i[0]] not in self.closed and self.grid[i[1]][i[0]].walkable and 0 <= i[0] <= len(self.grid[0]) - 1 and 0 <= i[1] <= len(self.grid) - 1, contenders)

    def dist(self, a, b):
        dx = np.abs(a.x - b.x)
        dy = np.abs(a.y - b.y)

        if dx > dy:
            return (14 * dy) + (10 * (dx - dy))
        else:
            return (14 * dx) + (10 * (dy - dx))

class UI(Grid):
    def __init__(self, x=1200, y=800, w=20):
        assert all(type(i) == int for i in [x, y, w]), "" # type check

        super().__init__(x, y, w)
        pygame.init()

        self.surf = pygame.display.set_mode((self.x, self.y), 0, 32)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("A* Demo")

        self.colours = {
            0: (255, 255, 255), # empty
            1: (255, 0, 0), # start
            2: (0, 255, 0), # end
            3: (0, 0, 0), # wall
            4: (0, 0, 255), # path
            5: (255, 255, 0), # search area
        }

    def draw(self):
        for y, i in enumerate(self.grid):
            for x, j in enumerate(i):
                pygame.draw.rect(self.surf, self.colours[j.val], [x*self.w, y*self.w, self.w, self.w], 0)

        pygame.display.flip()

    def usersetup(self):
        state = 1

        while not state == 4:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not state == 3:
                        x, y = list(map(lambda i: i//self.w, pygame.mouse.get_pos()))

                        if not self.grid[y][x].val:
                            self.grid[y][x].val = state

                            if state == 1:
                                self.current = self.grid[y][x]
                                self.start = self.grid[y][x]
                            elif state == 2:
                                self.dest = self.grid[y][x]
                        
                            state += 1
                        
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and state == 3:
                        state += 1

            if state == 3 and pygame.mouse.get_pressed()[0]:
                x, y = list(map(lambda i: i//self.w, pygame.mouse.get_pos()))

                if not self.grid[y][x].val:
                    self.grid[y][x].val = state
                    self.grid[y][x].walkable = False

            self.draw()

        self.current.set_g(0)
        self.current.set_h(self.dist(self.start, self.dest))
        self.open = [self.current]
        self.closed = []

    def run(self):
        while self.open:
            self.clock.tick(20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            print(1, self.open, self.closed, self.current)

            self.draw()
            next(self)##############

            self.current = min(self.open, key=lambda i: i.f)

            print(3, self.current)

            self.open.remove(self.current)
            self.closed.append(self.current)

            if self.current == self.dest:
                break

            for n in self.get_neighbours():
                n = self.grid[n[1]][n[0]]
                n.set_g(self.dist(self.start, n))
                n.set_h(self.dist(n, self.dest))

                movement_cost = self.current.g + self.dist(self.current, n)

                if movement_cost < n.g or not n in self.open:
                    n.set_g(movement_cost)
                    n.set_h(self.dist(n, self.dest))
                    n.parent = self.current

                    if not n in self.open:
                        self.open.append(n)

                    self.current = n

            self.current.val = 5

        #retrace
        current = self.dest
        path = []
        while not current == self.start:
            path.append(current)
            current = current.parent
        for i in path:
            i.val = 4

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit()
            
            self.draw()

def main(ui):
    ui.usersetup()
    ui.run()

if __name__ == "__main__":
    main(UI())
