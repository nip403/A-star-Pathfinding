import pygame
import numpy as np
import sys

class Node:
    def __init__(self, x, y, val):
        self.x = x
        self.y = y
        self.val = val
        self.walkable = True
        self.parent = None

class Grid:
    def __init__(self, x, y, w):
        self.x = x - (x % w)
        self.y = y - (y % w)
        self.w = w
        self.grid = [[Node(j, i, 0) for j in range(x//w)] for i in range(y//w)]

    def get_neighbours(self, current):
        x = current.x
        y = current.y

        contenders = [
            [x+1, y],
            [x-1, y],
            [x, y+1],
            [x, y-1]
        ]

        return list(map(lambda p: self.grid[p[1]][p[0]], filter(lambda i: 0 <= i[0] <= len(self.grid[0]) - 1 and 0 <= i[1] <= len(self.grid) - 1 and self.grid[i[1]][i[0]].walkable, contenders)))

    def heuristic(self, a, b):
        dx, dy = np.abs(a.x - b.x), np.abs(a.y - b.y)
        return (14 * min(dx, dy)) + (10 * np.abs(dx - dy))

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

    def dijkstra(self):
        pass

    def astar(self):
        fringe = set([self.start])
        closed = set()

        g = {self.start: 0}
        f = {self.start: self.heuristic(self.start, self.dest)}
        camefrom = {}

        while fringe:
            print(fringe)
            #self.clock.tick(20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.draw()

            current = None
            currentf = None

            for node in fringe:
                if current is None or f[node] < currentf:
                    currentf = f[node]
                    current = node
            
            if current == self.dest:
                path = [current]

                while current in camefrom:
                    current.val = 4
                    current = camefrom[current]
                    path.append(current)

                path[0].val = 2
                path[-1].val = 1

                return

            try:
                fringe.remove(current)
            except:
                pass

            closed.add(current)

            for n in self.get_neighbours(current):
                if n in closed:
                    continue

                n.val = 5
                n_g = g[current] + 1

                if not n in fringe:
                    fringe.add(n)
                elif n_g >= g[n]:
                    continue

                camefrom[n] = current
                g[n] = n_g
                f[n] = g[n] + self.heuristic(n, self.dest)

        raise Exception("No path found") # add screen for this case

    def waitingscr(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return
            
            self.draw()

    def reset(self, x=1200, y=800, w=20):
        self.__init__(x, y, w)

def main(app):
    while True:
        app.reset()
        app.usersetup()
        app.astar()
        app.waitingscr()

if __name__ == "__main__":
    main(UI())
