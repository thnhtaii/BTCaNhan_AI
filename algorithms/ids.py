import time

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

def dfs_limit(start_state, goal_state, limit, mode="early"):
    if start_state == goal_state:
        return [], 0
        
    frontier = [(start_state, [], 0)]
    if mode == "early":
        explored = {tuple(start_state): 0}
    else:
        explored = {}
        
    nodes_generated = 1
    
    while frontier:
        node, path, depth = frontier.pop()
        
        if mode == "late" and node == goal_state:
            return path, nodes_generated
            
        if mode == "late":
            if tuple(node) in explored and explored[tuple(node)] <= depth:
                continue
            explored[tuple(node)] = depth
            
        if depth < limit:
            for action, child in get_successors(node):
                if mode == "early":
                    nodes_generated += 1
                    if child == goal_state:
                        return path + [(action, child)], nodes_generated
                    if tuple(child) not in explored or explored[tuple(child)] > depth + 1:
                        explored[tuple(child)] = depth + 1
                        frontier.append((child, path + [(action, child)], depth + 1))
                else:  
                    if tuple(child) not in explored or explored[tuple(child)] > depth + 1:
                        frontier.append((child, path + [(action, child)], depth + 1))
                        nodes_generated += 1
                        
    return None, nodes_generated
 
def ids(start_state, goal_state, mode="early", max_depth=50):
    if start_state == goal_state:
        return [], 0
    
    total_nodes = 0
    
    for depth in range(max_depth + 1):
        result, nodes = dfs_limit(start_state, goal_state, depth, mode)
        total_nodes += nodes
        if result is not None:
            return result, total_nodes
    
    return None, total_nodes
