# path is the input shortest path
# gates is the gate zone tiles
# moves is the set of moves relative to the field
# rmoves is the set of moves that the robot has to do

path = [13, 14, 10, 11, 7, 6, 2, 6, 5, 9, 8, 9, 5, 4, 0, 1]
gates = [11, 8, 2]
''' grid looks like this
 0  1  2  3
 4  5  6  7
 8  9 10 11
12 13 14 15
'''

'''
NEW PLAN
ok so make the path and set of moves and stuff
then splice the set of moves into different sections
splice from 0 to right before gate 1
gate 1 to right before gate 2
etc
and then for each section
rotate the moves as per the robot heading
bam
proper robot moves
then make them mecanum yippe
'''

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
print(moves)
print(gate_entry)

# 2 5 9
# 0-2 2-5 5-9 9-end
# [:i] [i:i] [i:]

# split list of moves into sections based on the gate zones
# every time the robot needs to enter another gate zone (and turn bc of it) is another section
splice_moves = moves
if gate_entry:
    splice_moves = []
    splice_moves.append(moves[:gate_entry[0]])
    for i in range(len(gate_entry)-1):
        splice_moves.append(moves[gate_entry[i]:gate_entry[i+1]])
    splice_moves.append(moves[gate_entry[-1]:])


rmoves = []  # real/robot moves
rmoves += splice_moves[0]  # first section is always facing forward
prevdir = 0  # previous robot heading
for i in range(1,len(splice_moves)):  # loop over remaining sections
    rmoves.append(f"t{(moves[gate_entry[i-1]] - prevdir)%360}")  # add the turning instruction
    rmoves += [(j-moves[gate_entry[i-1]])%360 for j in splice_moves[i]] # rotate everything yeehaw
    prevdir = moves[gate_entry[i-1]]  # update heading

print(rmoves)