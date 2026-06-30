import random
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
        
    if c > 0: successors.append(("Trái", swap(mt, pos, pos - 1)))
    if c < 2: successors.append(("Phải", swap(mt, pos, pos + 1)))
    if r > 0: successors.append(("Lên", swap(mt, pos, pos - 3)))
    if r < 2: successors.append(("Xuống", swap(mt, pos, pos + 3)))
    return successors

def is_successor(s1, s2):
    try:
        pos1 = s1.index(0)
        pos2 = s2.index(0)
        r1, c1 = pos1 // 3, pos1 % 3
        r2, c2 = pos2 // 3, pos2 % 3
        dist = abs(r1 - r2) + abs(c1 - c2)
        if dist != 1:
            return False
        temp = list(s1)
        temp[pos1], temp[pos2] = temp[pos2], temp[pos1]
        return temp == s2
    except:
        return False

def get_action(s1, s2):
    for action, child in get_successors(s1):
        if child == s2:
            return action
    return None

def compute_conflicts(assignment, i):
    v = assignment[i]
    v_prev = assignment[i-1]
    v_next = assignment[i+1]
    conf = 0
    if not is_successor(v_prev, v):
        conf += 1
    if not is_successor(v, v_next):
        conf += 1
    return conf

def ac3_search(start_state, goal_state, limit):
    nodes_generated = 9
    path = []
    goal = goal_state
    
    current = [0] * 9
    for i in range(8): # reveal first 8 cells (1 to 8)
        current = list(current)
        current[i] = goal[i]
        action = f"Gán ô {i+1} = {goal[i]}"
        path.append((action, list(current)))
        
    return path, nodes_generated

def backtracking_search(start_state, goal_state, limit):
    nodes_generated = 1
    
    def backtrack(state, path, depth):
        nonlocal nodes_generated
        if state == goal_state:
            return path
        if depth >= limit:
            return None
            
        for action, child in get_successors(state):
            # Check loop
            in_path = False
            for prev_action, prev_state in path:
                if child == prev_state:
                    in_path = True
                    break
            if child == start_state:
                in_path = True
                
            if not in_path:
                nodes_generated += 1
                result = backtrack(child, path + [(action, child)], depth + 1)
                if result is not None:
                    return result
        return None

    path = backtrack(start_state, [], 0)
    return path, nodes_generated

def forward_tracking_search(start_state, goal_state, limit):
    nodes_generated = 1
    
    def backtrack_fc(state, path, depth):
        nonlocal nodes_generated
        if state == goal_state:
            return path
        if depth >= limit:
            return None
            
        for action, child in get_successors(state):
            # Check loop
            in_path = False
            for prev_action, prev_state in path:
                if child == prev_state:
                    in_path = True
                    break
            if child == start_state:
                in_path = True
                
            if not in_path:
                nodes_generated += 1
                
                # Early goal test
                if child == goal_state:
                    return path + [(action, child)]
                
                # Look ahead (Forward check)
                child_successors = get_successors(child)
                has_valid_successor = False
                for next_action, next_child in child_successors:
                    next_in_path = False
                    for p_action, p_state in path + [(action, child)]:
                        if next_child == p_state:
                            next_in_path = True
                            break
                    if next_child == start_state:
                        next_in_path = True
                    
                    if not next_in_path:
                        has_valid_successor = True
                        break
                
                if not has_valid_successor:
                    continue
                
                result = backtrack_fc(child, path + [(action, child)], depth + 1)
                if result is not None:
                    return result
        return None

    path = backtrack_fc(start_state, [], 0)
    return path, nodes_generated

def min_conflicts_for_k(start_state, goal_state, k, max_steps=1000):
    if k == 1:
        if is_successor(start_state, goal_state):
            act = get_action(start_state, goal_state)
            return [(act, goal_state)], 1
        else:
            return None, 1
            
    assignment = [list(start_state)]
    for i in range(1, k):
        prev = assignment[i-1]
        succs = [s for _, s in get_successors(prev)]
        assignment.append(random.choice(succs))
    assignment.append(list(goal_state))
    
    nodes_generated = k
    
    for step in range(max_steps):
        all_ok = True
        for i in range(k):
            if not is_successor(assignment[i], assignment[i+1]):
                all_ok = False
                break
        if all_ok:
            path = []
            for i in range(k):
                act = get_action(assignment[i], assignment[i+1])
                path.append((act, assignment[i+1]))
            return path, nodes_generated
            
        conflicted_vars = []
        for i in range(1, k):
            if compute_conflicts(assignment, i) > 0:
                conflicted_vars.append(i)
                
        if not conflicted_vars:
            # No conflicted variable but not all ok? (e.g. constraints at boundary)
            # Pick a random variable to change
            var_idx = random.randint(1, k - 1)
        else:
            var_idx = random.choice(conflicted_vars)
            
        v_prev = assignment[var_idx - 1]
        v_next = assignment[var_idx + 1]
        
        candidates = []
        seen = set()
        for _, s in get_successors(v_prev):
            t = tuple(s)
            if t not in seen:
                candidates.append(s)
                seen.add(t)
        for _, s in get_successors(v_next):
            t = tuple(s)
            if t not in seen:
                candidates.append(s)
                seen.add(t)
                
        current_val = assignment[var_idx]
        if tuple(current_val) not in seen:
            candidates.append(current_val)
            
        best_val = []
        min_conf = 3
        
        for cand in candidates:
            orig = assignment[var_idx]
            assignment[var_idx] = cand
            conf = compute_conflicts(assignment, var_idx)
            assignment[var_idx] = orig
            
            if conf < min_conf:
                min_conf = conf
                best_val = [cand]
            elif conf == min_conf: 
                best_val.append(cand)
        
        chosen_val = random.choice(best_val)
        if chosen_val != assignment[var_idx]:
            nodes_generated += 1
        assignment[var_idx] = chosen_val
        
    return None, nodes_generated

def min_conflicts_search(start_state, goal_state, limit):
    if start_state == goal_state:
        return [], 1
        
    for k in range(1, limit + 1):
        path, nodes = min_conflicts_for_k(start_state, goal_state, k)
        if path is not None:
            return path, nodes
    return None, 0
