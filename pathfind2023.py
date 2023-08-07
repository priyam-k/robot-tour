# score: (lower is better)
#   + time score (how far from target time, x2 if under)
#   + distance score (distance from target point)
#   + gate bonus (-15 per gate zone)
#   + penalties (50pt for touching 2x4, 35pt for removing 2x4)

# maybe use splines to optimize path?

import pygame
import heapq
import itertools

pygame.init()
screen = pygame.display.set_mode((800, 600))

# steps:
#   1. find node path to target (through gates)
#   2. implement optimizations to cut corners
#   3. implement splines to optimize path

# possible other strategy: try to go in a straight line to the target, and
#   if there is a wall in the way, move to an adjacent square and try again

def dijkstra(adj_matrix, start, finish):
    n = len(adj_matrix)
    dist = [float('inf')] * n
    dist[start] = 0
    visited = [False] * n
    heap = [(0, start)]
    prev = [None] * n
    while heap:
        (d, u) = heapq.heappop(heap)
        if visited[u]:
            continue
        visited[u] = True
        if u == finish:
            path = []
            while prev[u] is not None:
                path.append(u)
                u = prev[u]
            path.append(start)
            path.reverse()
            return path
        for v in range(n):
            if adj_matrix[u][v] != 0:
                alt = dist[u] + adj_matrix[u][v]
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    heapq.heappush(heap, (dist[v], v))
    return None

def block(vb, hb):
    for i in range(len(vb)):
        for j in range(len(vb[i])):
            if vb[i][j] == 1:
                adj_matrix[i*4+j][i*4+j+1] = 0
                adj_matrix[i*4+j+1][i*4+j] = 0
            else:
                adj_matrix[i*4+j][i*4+j+1] = 1
                adj_matrix[i*4+j+1][i*4+j] = 1

    for i in range(len(hb)):
        for j in range(len(hb[i])):
            if hb[i][j] == 1:
                adj_matrix[i*4+j][i*4+j+4] = 0
                adj_matrix[i*4+j+4][i*4+j] = 0
            else:
                adj_matrix[i*4+j][i*4+j+4] = 1
                adj_matrix[i*4+j+4][i*4+j] = 1

def path_gates(adj_matrix, start, finish, gates, opt=True): # opt = optimize gate order
    if gates == []:
        p = dijkstra(adj_matrix, start, finish)
        if p is None:
            return [], []
        return dijkstra(adj_matrix, start, finish), []

    best = []
    alt = []
    if opt:
        perms = list(itertools.permutations(gates))
    else:
        perms = [gates]

    for perm in perms:
        path = []
        p = dijkstra(adj_matrix, start, perm[0])
        if p is None:
            return [], []
        path += p
        
        del path[-1]
        for i in range(len(perm)-1):
            p = dijkstra(adj_matrix, perm[i], perm[i+1])
            if p is None:
                return [], []
            path += p
            del path[-1]
        
        p = dijkstra(adj_matrix, perm[-1], finish)
        if p is None:
            return [], []
        path += p
        # print("yellow") why is this here???
        if best == [] or pathlen(adj_matrix, path) < pathlen(adj_matrix, best):
            best = path
        elif pathlen(adj_matrix, path) == pathlen(adj_matrix, best):
            alt.append(path)
    
    a = [i for i in alt if pathlen(adj_matrix, i) == pathlen(adj_matrix, best)]
    a.insert(0, best)
    alt = a

    return best, alt

def pathlen(adj, path):
    return 50*(len(path)-1) + 25

adj_matrix = [
    [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0]
]

vblock = [ # vertical block obstacles
    [0, 1, 1],
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
]

hblock = [ # horizontal block obstacles
    [0, 1, 0, 0],
    [1, 0, 1, 0],
    [0, 1, 0, 1]
]

gates = [11, 8, 2]
start = 13
finish = 1

block(vblock, hblock)
shortest_path, alt = path_gates(adj_matrix, start, finish, gates, opt=True)
print(f"The shortest path from node {start} to node {finish} is {shortest_path} with len {pathlen(adj_matrix, shortest_path)}")
print(f"Alternate paths: {alt}")

nc = []
for i in range(len(adj_matrix)):
    nc.append((150+(i%4)*100, 150+(i//4)*100))

c = { # colors
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "dgreen": (93, 148, 83),
    "brown": (175, 144, 101),
    "yellow": (255, 255, 0),
    "orange": (255, 165, 0),
}
font = pygame.font.SysFont("Arial", 30)

show_alt = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                break
            if event.key == pygame.K_SPACE:
                show_alt = not show_alt
        if event.type == pygame.MOUSEBUTTONDOWN: # mouse click
            mx, my = pygame.mouse.get_pos()
            shift = event.button == 1 and pygame.key.get_pressed()[pygame.K_LSHIFT] # shift click
            for i in range(len(adj_matrix)):
                if (mx-nc[i][0])**2 + (my-nc[i][1])**2 <= 40**2: # if node clicked
                    if event.button == 2 or shift: # toggle gate
                        if i in gates: gates.remove(i)
                        else: gates.append(i)
                    
                    elif event.button == 1: start = i
                    elif event.button == 3: finish = i
                    
                    block(vblock, hblock)
                    shortest_path, alt = path_gates(adj_matrix, start, finish, gates)
                    print(f"The shortest path from node {start} to node {finish} is {shortest_path} with len {pathlen(adj_matrix, shortest_path)}")
                    print(f"Alternate paths: {alt}")
                    screen.fill(c["white"])
                    break
            # TODO toggle blocks and stuff
            for i in range(len(vblock)):
                for j in range(len(vblock[0])):
                    if 190+100*j <= mx <= 210+100*j and 100+100*i <= my <= 200+100*i:
                        if event.button == 2 or shift:
                            vblock[i][j] = 1-vblock[i][j]
                            print(vblock)
                            block(vblock, hblock)
                            shortest_path, alt = path_gates(adj_matrix, start, finish, gates)
                            print(f"The shortest path from node {start} to node {finish} is {shortest_path} with len {pathlen(adj_matrix, shortest_path)}")
                            print(f"Alternate paths: {alt}")
                            screen.fill(c["white"])
                            break
            for i in range(len(hblock)):
                for j in range(len(hblock[0])):
                    if 100+100*j <= mx <= 200+100*j and 190+100*i <= my <= 210+100*i:
                        if event.button == 2 or shift:
                            hblock[i][j] = 1-hblock[i][j]
                            print(hblock)
                            block(vblock, hblock)
                            shortest_path, alt = path_gates(adj_matrix, start, finish, gates)
                            print(f"The shortest path from node {start} to node {finish} is {shortest_path} with len {pathlen(adj_matrix, shortest_path)}")
                            print(f"Alternate paths: {alt}")
                            screen.fill(c["white"])
                            break
    
    screen.fill(c["white"])

    # draw grid lines
    for i in range(3):
        y = 200 + i*100
        pygame.draw.line(screen, c["black"], (100, y), (500, y), 2)

    for i in range(3):
        x = 200 + i*100
        pygame.draw.line(screen, c["black"], (x, 100), (x, 500), 2)
    
    # draw green border
    w = 10
    pygame.draw.rect(screen, c["dgreen"], pygame.Rect(100-w, 100-w, 400+2*w, 400+2*w), w)

    # draw gates
    for i in gates:
        pygame.draw.rect(screen, c["black"], (nc[i][0]-50, nc[i][1]-50, 100, 100), 7)

    # draw vertical blocks
    for i in range(len(vblock)):
        for j in range(len(vblock[i])):
            if vblock[i][j] == 1:
                pygame.draw.line(screen, c["brown"], (100*j+200, 100*i+100+5), (100*j+200, 100*i+200-5), 10)
    
    # draw horizontal blocks
    for i in range(len(hblock)):
        for j in range(len(hblock[i])):
            if hblock[i][j] == 1:
                pygame.draw.line(screen, c["brown"], (100*j+100+5, 100*i+200), (100*j+200-5, 100*i+200), 10)
    
    # draw path
    if shortest_path:
        pygame.draw.lines(screen, c["red"], False, [nc[i] for i in shortest_path], 3)

    # draw alternate paths
    if show_alt:
        ac = [c["red"], c["blue"], c["green"], c["orange"], c["yellow"]]*3
        for k in range(len(alt)):
            offset = 5*((k+1)//2)*((-1)**(k+1))
            pygame.draw.lines(screen, ac[k], False, [(nc[i][0]+offset, nc[i][1]+offset) for i in alt[k]], 3)

        g_ord = [[j for j in i if j in gates] for i in alt]
        for i in range(len(g_ord)):
            text = font.render(f"{g_ord[i]}", True, ac[i])
            screen.blit(text, (550, 100+50*i))

    # draw start and finish
    pygame.draw.circle(screen, c["green"], nc[start], 10)
    pygame.draw.circle(screen, c["red"], nc[finish], 10)

    # display length of path
    text = font.render(f"Length: {pathlen(adj_matrix, shortest_path)}", True, c["black"])
    screen.blit(text, (550, 50))

    pygame.display.flip()
    