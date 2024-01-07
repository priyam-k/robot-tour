import heapq
import itertools


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
path, alt = path_gates(adj_matrix, start, finish, gates, opt=True)
print(f"The shortest path from node {start} to node {finish} is {path} with len {pathlen(adj_matrix, path)}")
print(f"Alternate paths: {alt}")

moves = [0]*(len(path)-1)  # empty list of moves

# creates a set of moves if facing straight forward (0 is forward, 90 is right, etc)
for i in range(len(path)-1):
    r1 = path[i]//4  # row 1
    r2 = path[i+1]//4
    c1 = path[i]%4  # column 1
    c2 = path[i+1]%4

    if c1 > c2:
        moves[i] = 270
    elif c1 < c2:
        moves[i] = 90
    elif r1 > r2:
        moves[i] = 0
    elif r1 < r2:
        moves[i] = 180
gate_entry = sorted([path.index(i)-1 for i in gates])  # find move number where robot enters gate

# split list of moves into sections based on the gate zones
# every time the robot needs to enter another gate zone (and turn bc of it) is another section
splice_moves = moves
if gate_entry:
    splice_moves = []
    splice_moves.append(moves[:gate_entry[0]])
    for i in range(len(gate_entry)-1):
        splice_moves.append(moves[gate_entry[i]:gate_entry[i+1]])
    splice_moves.append(moves[gate_entry[-1]:])


rmoves = []  # real moves or robot moves
rmoves += splice_moves[0]  # first section is always facing forward
prevdir = 0  # previous robot heading
for i in range(1,len(splice_moves)):  # loop over remaining sections
    rmoves.append(f"t{(moves[gate_entry[i-1]] - prevdir)%360}")  # add the turning instruction
    rmoves += [(j-moves[gate_entry[i-1]])%360 for j in splice_moves[i]] # rotate everything yeehaw
    prevdir = moves[gate_entry[i-1]]  # update heading

print(rmoves)