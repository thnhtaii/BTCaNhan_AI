import time
import math

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

def _search(node, goal_state, path, g, threshold, nodes_count, visited):
    """Hàm đệ quy hỗ trợ cho tìm kiếm IDA*."""
    f = g + manhattan_distance(node, goal_state)

    if f > threshold:
        return f, None, nodes_count

    if node == goal_state:
        return f, path, nodes_count

    min_threshold = math.inf
    visited.add(tuple(node))

    for action, child in get_successors(node):
        if tuple(child) not in visited:
            nodes_count += 1
            new_threshold, result, nodes_count = _search(
                child, goal_state, path + [(action, child)],
                g + 1, threshold, nodes_count, visited
            )
            if result is not None:
                visited.discard(tuple(node))
                return new_threshold, result, nodes_count
            min_threshold = min(min_threshold, new_threshold)

    visited.discard(tuple(node))
    return min_threshold, None, nodes_count

def ida_star(start_state, goal_state):
    """Tìm kiếm IDA* sử dụng hàm đánh giá khoảng cách Manhattan."""
    if start_state == goal_state:
        return [], 0

    threshold = manhattan_distance(start_state, goal_state)
    total_nodes = 0

    while True:
        visited = set()
        result_threshold, result, nodes = _search(
            start_state, goal_state, [], 0, threshold, 1, visited
        )
        total_nodes += nodes

        if result is not None:
            return result, total_nodes

        if result_threshold == math.inf:
            return None, total_nodes

        threshold = result_threshold
