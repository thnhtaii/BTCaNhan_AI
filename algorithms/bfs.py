import time
from collections import deque

def in_mt(mt):
    res = ""
    for i in range(3):
        row = ""
        for j in range(3):
            val = mt[i*3 + j]
            if val == 0:
                row += " [ ] "
            else:
                row += f"  {val}  "
        res += row + "\n"
    res += "-" * 20 + "\n"
    return res

def get_successors(mt):
    pos = mt.index(0)
    r, c = pos // 3, pos % 3
    successors = []
    
    def swap(mt, i, j):
        new_mt = list(mt)
        new_mt[i], new_mt[j] = new_mt[j], new_mt[i]
        return new_mt
        
    if r > 0: successors.append(("Lên", swap(mt, pos, pos - 3)))
    if r < 2: successors.append(("Xuống", swap(mt, pos, pos + 3)))
    if c > 0: successors.append(("Trái", swap(mt, pos, pos - 1)))
    if c < 2: successors.append(("Phải", swap(mt, pos, pos + 1)))
    return successors

def bfs(start_state, goal_state, mode="early"):
    if start_state == goal_state:
        return [], 0
    frontier = deque([(start_state, [])])
    
    if mode == "early":
        explored = set([tuple(start_state)])
    else:
        explored = set()
        
    nodes_generated = 1
    
    while frontier:
        node, path = frontier.popleft()
        
        if mode == "late" and node == goal_state:
            return path, nodes_generated
            
        if mode == "late":
            if tuple(node) in explored:
                continue
            explored.add(tuple(node))
            
        for action, child in get_successors(node):
            if mode == "early":
                nodes_generated += 1
                if child == goal_state:
                    return path + [(action, child)], nodes_generated
                if tuple(child) not in explored:
                    explored.add(tuple(child))
                    frontier.append((child, path + [(action, child)]))
            else:
                if tuple(child) not in explored:
                    frontier.append((child, path + [(action, child)]))
                    nodes_generated += 1
                    
    return None, nodes_generated
