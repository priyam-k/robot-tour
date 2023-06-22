import pygame
from math import *
import heapq
import itertools

pygame.init()
screen = pygame.display.set_mode((600, 600))

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

# make sure gates are not repeated!!!
def path_gates(adj_matrix, start, finish, gates):
    if gates == []:
        return dijkstra(adj_matrix, start, finish)

    best = []
    perms = list(itertools.permutations(gates))

    for perm in perms:
        path = []
        path += dijkstra(adj_matrix, start, perm[0])
        del path[-1]
        for i in range(len(perm)-1):
            path += dijkstra(adj_matrix, perm[i], perm[i+1])
            del path[-1]
        path += dijkstra(adj_matrix, perm[-1], finish)

        if best == [] or pathlen(adj_matrix, path) < pathlen(adj_matrix, best):
            best = path

    return best


def pathlen(adj_matrix, path):
    l = 0
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        l += adj_matrix[u][v]
    return l

s = 25
c = 6.25 * pi

adj_matrix = [
    [0, s, 0, c, c, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [s, 0, s, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, s, 0, 0, 0, c, c, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [c, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [c, 0, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, c, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, c, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, c, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, s, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, c, c, 0, 0, 0, 0, 0, c, c, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, s, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, s, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, s, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, c, c, 0, 0, 0, 0, 0, 0, c, c, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, c, c, 0, 0, 0, 0, 0, 0, c, c, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, s, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, s, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, s, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, c, c, 0, 0, 0, 0, 0, c, c, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, s, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, c, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, c, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, c, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, 0, c],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, c, 0, 0, 0, 0, 0, 0, c],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, c, c, 0, 0, 0, s, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, s, 0, s],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, c, c, 0, s, 0],
]

start = 11
finish = 9
gates = [20, 25]

shortest_path = path_gates(adj_matrix, start, finish, gates)
print(f"The shortest path from node {start} to node {finish} is {shortest_path} with len {pathlen(adj_matrix, shortest_path)}")

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (3, 127, 252)
yellow = (255, 255, 0)
path = yellow # path line color
pc = { # path colors
    'tlc1': white,
    'tlc2': white,
    'tlc3': white,
    'tlc4': white,
    'tlc5': white,
    'tlc6': white,
    'tlc7': white,
    'tlc8': white,
    'trc1': white,
    'trc2': white,
    'trc3': white,
    'trc4': white,
    'trc5': white,
    'trc6': white,
    'trc7': white,
    'trc8': white,
    'blc1': white,
    'blc2': white,
    'blc3': white,
    'blc4': white,
    'blc5': white,
    'blc6': white,
    'blc7': white,
    'blc8': white,
    'brc1': white,
    'brc2': white,
    'brc3': white,
    'brc4': white,
    'brc5': white,
    'brc6': white,
    'brc7': white,
    'brc8': white,
    'tl1': white,
    'tl2': white,
    'll1': white,
    'll2': white,
    'bl1': white,
    'bl2': white,
    'rl1': white,
    'rl2': white,
}
ntp = { # node to path
    '8-4': 'tlc1',
    '4-0': 'tlc2',
    '0-3': 'tlc3',
    '3-7': 'tlc4',
    '7-10': 'tlc5',
    '10-15': 'tlc6',
    '15-11': 'tlc7',
    '11-8': 'tlc8',
    '9-6': 'trc1',
    '6-2': 'trc2',
    '2-5': 'trc3',
    '5-8': 'trc4',
    '8-12': 'trc5',
    '12-16': 'trc6',
    '16-13': 'trc7',
    '13-9': 'trc8',
    '23-19': 'blc1',
    '19-15': 'blc2',
    '15-18': 'blc3',
    '18-22': 'blc4',
    '22-25': 'blc5',
    '25-29': 'blc6',
    '29-26': 'blc7',
    '26-23': 'blc8',
    '24-21': 'brc1',
    '21-16': 'brc2',
    '16-20': 'brc3',
    '20-23': 'brc4',
    '23-27': 'brc5',
    '27-31': 'brc6',
    '31-28': 'brc7',
    '28-24': 'brc8',
    '0-1': 'tl1',
    '1-2': 'tl2',
    '7-14': 'll1',
    '14-22': 'll2',
    '29-30': 'bl1',
    '30-31': 'bl2',
    '9-17': 'rl1',
    '17-24': 'rl2'
}
c = 100*(1-sqrt(2)/2) # curve offset
nc = { # node coordinates
    0: (200, 100),
    1: (300, 100),
    2: (400, 100),
    3: (100+c, 100+c),
    4: (300-c, 100+c),
    5: (300+c, 100+c),
    6: (500-c, 100+c),
    7: (100, 200),
    8: (300, 200),
    9: (500, 200),
    10: (100+c, 300-c),
    11: (300-c, 300-c),
    12: (300+c, 300-c),
    13: (500-c, 300-c),
    14: (100, 300),
    15: (200, 300),
    16: (400, 300),
    17: (500, 300),
    18: (100+c, 300+c),
    19: (300-c, 300+c),
    20: (300+c, 300+c),
    21: (500-c, 300+c),
    22: (100, 400),
    23: (300, 400),
    24: (500, 400),
    25: (100+c, 500-c),
    26: (300-c, 500-c),
    27: (300+c, 500-c),
    28: (500-c, 500-c),
    29: (200, 500),
    30: (300, 500),
    31: (400, 500)
}

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN: # mouse click
            mx, my = pygame.mouse.get_pos()
            for i in range(32):
                if (mx-nc[i][0])**2 + (my-nc[i][1])**2 <= 300:
                    if event.button == 1: start = i
                    if event.button == 3: finish = i
                    if event.button == 2:
                        if i in gates: gates.remove(i)
                        else: gates.append(i)
                    pc = {key:white for key in pc}
                    #shortest_path = dijkstra(adj_matrix, start, finish)
                    shortest_path = path_gates(adj_matrix, start, finish, gates)
                    screen.fill(black)


    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        break
    
    if True: # drawing arcs and lines
        cr = 200 # circle radius

        tlc = (100,100) # top left circle
        pygame.draw.arc(screen, pc['tlc1'], (*tlc, cr, cr), 0, 0.25*pi, 3)
        pygame.draw.arc(screen, pc['tlc2'], (*tlc, cr, cr), 0.25*pi, 0.5*pi, 3)
        pygame.draw.arc(screen, pc['tlc3'], (*tlc, cr, cr), 0.5*pi, 0.75*pi, 3)
        pygame.draw.arc(screen, pc['tlc4'], (*tlc, cr, cr), 0.75*pi, pi, 3)
        pygame.draw.arc(screen, pc['tlc5'], (*tlc, cr, cr), pi, 1.25*pi, 3)
        pygame.draw.arc(screen, pc['tlc6'], (*tlc, cr, cr), 1.25*pi, 1.5*pi, 3)
        pygame.draw.arc(screen, pc['tlc7'], (*tlc, cr, cr), 1.5*pi, 1.75*pi, 3)
        pygame.draw.arc(screen, pc['tlc8'], (*tlc, cr, cr), 1.75*pi, 2*pi, 3)

        trc = (300,100) # top right circle
        pygame.draw.arc(screen, pc['trc1'], (*trc, cr, cr), 0, 0.25*pi, 3)
        pygame.draw.arc(screen, pc['trc2'], (*trc, cr, cr), 0.25*pi, 0.5*pi, 3)
        pygame.draw.arc(screen, pc['trc3'], (*trc, cr, cr), 0.5*pi, 0.75*pi, 3)
        pygame.draw.arc(screen, pc['trc4'], (*trc, cr, cr), 0.75*pi, pi, 3)
        pygame.draw.arc(screen, pc['trc5'], (*trc, cr, cr), pi, 1.25*pi, 3)
        pygame.draw.arc(screen, pc['trc6'], (*trc, cr, cr), 1.25*pi, 1.5*pi, 3)
        pygame.draw.arc(screen, pc['trc7'], (*trc, cr, cr), 1.5*pi, 1.75*pi, 3)
        pygame.draw.arc(screen, pc['trc8'], (*trc, cr, cr), 1.75*pi, 2*pi, 3)

        blc = (100,300) # bottom left circle
        pygame.draw.arc(screen, pc['blc1'], (*blc, cr, cr), 0, 0.25*pi, 3)
        pygame.draw.arc(screen, pc['blc2'], (*blc, cr, cr), 0.25*pi, 0.5*pi, 3)
        pygame.draw.arc(screen, pc['blc3'], (*blc, cr, cr), 0.5*pi, 0.75*pi, 3)
        pygame.draw.arc(screen, pc['blc4'], (*blc, cr, cr), 0.75*pi, pi, 3)
        pygame.draw.arc(screen, pc['blc5'], (*blc, cr, cr), pi, 1.25*pi, 3)
        pygame.draw.arc(screen, pc['blc6'], (*blc, cr, cr), 1.25*pi, 1.5*pi, 3)
        pygame.draw.arc(screen, pc['blc7'], (*blc, cr, cr), 1.5*pi, 1.75*pi, 3)
        pygame.draw.arc(screen, pc['blc8'], (*blc, cr, cr), 1.75*pi, 2*pi, 3)

        brc = (300,300) # bottom right circle
        pygame.draw.arc(screen, pc['brc1'], (*brc, cr, cr), 0, 0.25*pi, 3)
        pygame.draw.arc(screen, pc['brc2'], (*brc, cr, cr), 0.25*pi, 0.5*pi, 3)
        pygame.draw.arc(screen, pc['brc3'], (*brc, cr, cr), 0.5*pi, 0.75*pi, 3)
        pygame.draw.arc(screen, pc['brc4'], (*brc, cr, cr), 0.75*pi, pi, 3)
        pygame.draw.arc(screen, pc['brc5'], (*brc, cr, cr), pi, 1.25*pi, 3)
        pygame.draw.arc(screen, pc['brc6'], (*brc, cr, cr), 1.25*pi, 1.5*pi, 3)
        pygame.draw.arc(screen, pc['brc7'], (*brc, cr, cr), 1.5*pi, 1.75*pi, 3)
        pygame.draw.arc(screen, pc['brc8'], (*brc, cr, cr), 1.75*pi, 2*pi, 3)

        # top line
        pygame.draw.line(screen, pc['tl1'], (200,100), (300,100), 3)
        pygame.draw.line(screen, pc['tl2'], (300,100), (400,100), 3)

        # left line
        pygame.draw.line(screen, pc['ll1'], (100,200), (100,300), 3)
        pygame.draw.line(screen, pc['ll2'], (100,300), (100,400), 3)

        # bottom line
        pygame.draw.line(screen, pc['bl1'], (200,500), (300,500), 3)
        pygame.draw.line(screen, pc['bl2'], (300,500), (400,500), 3)

        # right line
        pygame.draw.line(screen, pc['rl1'], (500,200), (500,300), 3)
        pygame.draw.line(screen, pc['rl2'], (500,300), (500,400), 3)
    
    # draw start and finish nodes and gates
    pygame.draw.rect(screen, green, (nc[start][0]-5,nc[start][1]-5,10,10))
    pygame.draw.rect(screen, red, (nc[finish][0]-5,nc[finish][1]-5,10,10))
    for i in gates:
        pygame.draw.rect(screen, blue, (nc[i][0]-5,nc[i][1]-5,10,10))

    font = pygame.font.Font(None, 36)
    text_surface = font.render(f"Length: {pathlen(adj_matrix, shortest_path)}", True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))

    assert type(shortest_path) == list
    for i in range(len(shortest_path)-1):
        u = shortest_path[i]
        v = shortest_path[i+1]
        
        try:
            pc[ntp[f'{u}-{v}']] = path
        except KeyError:
            pc[ntp[f'{v}-{u}']] = path

    pygame.display.flip()