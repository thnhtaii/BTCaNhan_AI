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

def get_successors_ucs(mt):
    pos = mt.index(0)
    r, c = pos // 3, pos % 3
    successors = []
    
    def swap(mt, i, j):
        new_mt = list(mt)
        new_mt[i], new_mt[j] = new_mt[j], new_mt[i]
        return new_mt, new_mt[i]
        
    if r > 0: 
        new_state, cost = swap(mt, pos, pos - 3)
        successors.append(("Lên", new_state, cost))
    if r < 2: 
        new_state, cost = swap(mt, pos, pos + 3)
        successors.append(("Xuống", new_state, cost))
    if c > 0: 
        new_state, cost = swap(mt, pos, pos - 1)
        successors.append(("Trái", new_state, cost))
    if c < 2: 
        new_state, cost = swap(mt, pos, pos + 1)
        successors.append(("Phải", new_state, cost))
    return successors

def ucs(start_state, goal_state, mode="late"):
    if start_state == goal_state:
        return [], 0
        
    counter = 0
    frontier = []
    heapq.heappush(frontier, (0, counter, start_state, []))
    
    explored = {tuple(start_state): 0}
    nodes_generated = 1
    
    while frontier:
        g, _, node, path = heapq.heappop(frontier)
        
        if mode == "late" and node == goal_state:
            return path, nodes_generated
            
        if mode == "late" and g > explored.get(tuple(node), float('inf')):
            continue
            
        for action, child, step_cost in get_successors_ucs(node):
            new_g = g + step_cost
            child_tuple = tuple(child)
            
            if mode == "early":
                nodes_generated += 1
                if child == goal_state:
                    return path + [(action, child)], nodes_generated
                if child_tuple not in explored or new_g < explored[child_tuple]:
                    explored[child_tuple] = new_g
                    counter += 1
                    heapq.heappush(frontier, (new_g, counter, child, path + [(action, child)]))
            else:
                if child_tuple not in explored or new_g < explored[child_tuple]:
                    explored[child_tuple] = new_g
                    nodes_generated += 1
                    counter += 1
                    heapq.heappush(frontier, (new_g, counter, child, path + [(action, child)]))
                    
    return None, nodes_generated
