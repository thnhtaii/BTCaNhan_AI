import time
import heapq

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
        
    if c > 0: successors.append(("Trái", swap(mt, pos, pos - 1)))
    if c < 2: successors.append(("Phải", swap(mt, pos, pos + 1)))
    if r > 0: successors.append(("Lên", swap(mt, pos, pos - 3)))
    if r < 2: successors.append(("Xuống", swap(mt, pos, pos + 3)))
    return successors

def manhattan_distance(state, goal):
    distance = 0
    for i in range(9):
        if state[i] != 0:
            goal_idx = goal.index(state[i])
            distance += abs(i // 3 - goal_idx // 3) + abs(i % 3 - goal_idx % 3)
    return distance

def astar(start_state, goal_state, mode="late"):
    if start_state == goal_state:
        return [], 0
        
    counter = 0
    frontier = []
    h_start = manhattan_distance(start_state, goal_state)
    heapq.heappush(frontier, (h_start, 0, counter, start_state, []))
    explored = {tuple(start_state): h_start}
    nodes_generated = 1
    
    while frontier:
        f, g, _, node, path = heapq.heappop(frontier)
        
        if mode == "late" and node == goal_state:
            return path, nodes_generated
            
        if mode == "late" and f > explored.get(tuple(node), float('inf')):
            continue
            
        for action, child in get_successors(node):
            new_g = g + 1
            h = manhattan_distance(child, goal_state)
            new_f = new_g + h
            child_tuple = tuple(child)
            
            if mode == "early":
                nodes_generated += 1
                if child == goal_state:
                    return path + [(action, child)], nodes_generated
                if child_tuple not in explored or new_f < explored[child_tuple]:
                    explored[child_tuple] = new_f
                    counter += 1
                    heapq.heappush(frontier, (new_f, new_g, counter, child, path + [(action, child)]))
            else:
                if child_tuple not in explored or new_f < explored[child_tuple]:
                    explored[child_tuple] = new_f
                    nodes_generated += 1
                    counter += 1
                    heapq.heappush(frontier, (new_f, new_g, counter, child, path + [(action, child)]))
                    
    return None, nodes_generated
