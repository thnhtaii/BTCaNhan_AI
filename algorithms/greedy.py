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
    """h(n): Hàm đánh giá khoảng cách Manhattan."""
    distance = 0
    for i in range(9):
        if state[i] != 0:
            goal_idx = goal.index(state[i])
            distance += abs(i // 3 - goal_idx // 3) + abs(i % 3 - goal_idx % 3)
    return distance

def greedy(start_state, goal_state, mode="late"):
    """Thuật toán Tìm kiếm Tham lam (Greedy Best-First Search) sử dụng khoảng cách Manhattan.
       Chỉ xem xét h(n), bỏ qua chi phí đường đi g(n).
    """
    if start_state == goal_state:
        return [], 0
        
    counter = 0
    h_start = manhattan_distance(start_state, goal_state)
    frontier = [(h_start, counter, start_state, [])]
    explored = set()
    nodes_generated = 1
    
    while frontier:
        h, _, node, path = heapq.heappop(frontier)
        
        if node == goal_state:
            return path, nodes_generated
            
        state_tuple = tuple(node)
        if state_tuple in explored:
            continue
        explored.add(state_tuple)
        
        for action, child in get_successors(node):
            if tuple(child) not in explored:
                nodes_generated += 1
                new_h = manhattan_distance(child, goal_state)
                counter += 1
                heapq.heappush(frontier, (new_h, counter, child, path + [(action, child)]))
                    
    return None, nodes_generated
