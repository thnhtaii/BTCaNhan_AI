import time
from collections import deque

def get_one_alternate_state(state):
    # Generates exactly 1 valid neighbor state to serve as the second starting belief state
    pos = state.index(0)
    r, c = pos // 3, pos % 3
    
    def swap(mt, i, j):
        new_mt = list(mt)
        new_mt[i], new_mt[j] = new_mt[j], new_mt[i]
        return new_mt
        
    if c > 0: return swap(state, pos, pos - 1)
    if c < 2: return swap(state, pos, pos + 1)
    if r > 0: return swap(state, pos, pos - 3)
    return swap(state, pos, pos + 3)

def result_state(s, action):
    # Transition function (forgiving: invalid moves return the same state)
    pos = s.index(0)
    r, c = pos // 3, pos % 3
    new_s = list(s)
    if action == "Trái" and c > 0:
        new_s[pos], new_s[pos - 1] = new_s[pos - 1], new_s[pos]
    elif action == "Phải" and c < 2:
        new_s[pos], new_s[pos + 1] = new_s[pos + 1], new_s[pos]
    elif action == "Lên" and r > 0:
        new_s[pos], new_s[pos - 3] = new_s[pos - 3], new_s[pos]
    elif action == "Xuống" and r < 2:
        new_s[pos], new_s[pos + 3] = new_s[pos + 3], new_s[pos]
    return new_s

def format_state_ascii(state):
    lines = []
    for i in range(3):
        row = state[i*3 : i*3+3]
        row_str = " ".join("[ ]" if x == 0 else f"  {x}  " for x in row)
        lines.append(row_str)
    return lines

def format_two_states_ascii(s1, s2):
    lines1 = format_state_ascii(s1)
    lines2 = format_state_ascii(s2)
    res = " Trạng thái 1:             Trạng thái 2:\n"
    for l1, l2 in zip(lines1, lines2):
        res += f" {l1}    |    {l2}\n"
    return res

def format_po_states_ascii(actual, belief):
    lines_act = format_state_ascii(actual)
    res = " Mô hình thực tế:\n"
    for l in lines_act:
        res += f" {l}\n"
    res += "\n Trạng thái niềm tin (Belief State):\n"
    for idx, s in enumerate(belief):
        s_str = "".join(str(x) if x != 0 else "_" for x in s)
        res += f"  {idx+1}. {s_str[0:3]}|{s_str[3:6]}|{s_str[6:9]}\n"
    return res

# 1. AND-OR Graph Search
def and_or_graph_search_solve(start_state, goal_state, limit=15):
    nodes_generated = 1
    
    def get_actions(state):
        pos = state.index(0)
        r, c = pos // 3, pos % 3
        actions = []
        if c > 0: actions.append("Trái")
        if c < 2: actions.append("Phải")
        if r > 0: actions.append("Lên")
        if r < 2: actions.append("Xuống")
        return actions

    def get_result(state, action):
        pos = state.index(0)
        new_mt = list(state)
        if action == "Trái":
            new_mt[pos], new_mt[pos - 1] = new_mt[pos - 1], new_mt[pos]
        elif action == "Phải":
            new_mt[pos], new_mt[pos + 1] = new_mt[pos + 1], new_mt[pos]
        elif action == "Lên":
            new_mt[pos], new_mt[pos - 3] = new_mt[pos - 3], new_mt[pos]
        elif action == "Xuống":
            new_mt[pos], new_mt[pos + 3] = new_mt[pos + 3], new_mt[pos]
        return [new_mt]

    def or_search(state, path):
        nonlocal nodes_generated
        if state == goal_state:
            return []
        if state in path:
            return "failure"
        if len(path) >= limit:
            return "failure"
            
        for action in get_actions(state):
            result_states = get_result(state, action)
            for r_state in result_states:
                nodes_generated += 1
            plan = and_search(result_states, path + [state])
            if plan != "failure":
                return [action, plan]
        return "failure"

    def and_search(states, path):
        plans = {}
        for s in states:
            plan_s = or_search(s, path)
            if plan_s == "failure":
                return "failure"
            plans[tuple(s)] = plan_s
        return plans

    plan = or_search(start_state, [])
    
    # Construct path
    path = []
    if plan != "failure":
        current_plan = plan
        while current_plan:
            action = current_plan[0]
            plans = current_plan[1]
            if not plans:
                break
            child_state_tuple = list(plans.keys())[0]
            child_state = list(child_state_tuple)
            path.append((action, child_state))
            current_plan = plans[child_state_tuple]
    else:
        path = None
        
    # Return log_data = None so UI formats it exactly like uninformed search
    return path, nodes_generated, None

# 2. Sensorless Search (Conformant Search)
def sensorless_search_solve(start_state, goal_state, start_state_2=None):
    if start_state_2 is None:
        alt_state = get_one_alternate_state(start_state)
    else:
        alt_state = start_state_2
    initial_belief = {tuple(start_state), tuple(alt_state)}
    
    frontier = deque([(initial_belief, [], start_state, alt_state)])
    explored = {tuple(sorted(initial_belief))}
    nodes_generated = 1
    max_nodes = 30000
    
    found_path = None
    
    while frontier and nodes_generated < max_nodes:
        curr_belief, path, curr_act1, curr_act2 = frontier.popleft()
        
        # Check if belief state contains only the goal
        if len(curr_belief) == 1 and list(curr_belief)[0] == tuple(goal_state):
            found_path = path
            break
            
        for action in ["Lên", "Xuống", "Trái", "Phải"]:
            next_act1 = result_state(curr_act1, action)
            next_act2 = result_state(curr_act2, action)
            next_belief = {tuple(next_act1), tuple(next_act2)}
            
            belief_key = tuple(sorted(next_belief))
            if belief_key not in explored:
                explored.add(belief_key)
                nodes_generated += 1
                frontier.append((next_belief, path + [(action, [next_act1, next_act2])], next_act1, next_act2))
                
    # Build logs
    log_data = []
    if found_path is not None:
        # Start state dual
        log_data.append({
            "step": 0,
            "action_html": "Trạng thái niềm tin bắt đầu (2 cấu hình):",
            "frontier_str": format_two_states_ascii(start_state, alt_state),
            "reached_str": ""
        })
        # Subsequent steps
        for idx, (action, act_states) in enumerate(found_path):
            log_data.append({
                "step": idx + 1,
                "action_html": f"Di chuyển ô trống sang <b>{action}</b>",
                "frontier_str": format_two_states_ascii(act_states[0], act_states[1]),
                "reached_str": ""
            })
    else:
        log_data.append({
            "step": 0,
            "action_html": "Không tìm thấy giải pháp sensorless.",
            "frontier_str": "",
            "reached_str": ""
        })
        
    return found_path, nodes_generated, log_data

# 3. Partially Observable Search
def partial_observable_search_solve(start_state, goal_state, start_state_2=None):
    if start_state_2 is None:
        alt_state = get_one_alternate_state(start_state)
    else:
        alt_state = start_state_2
    initial_belief = {tuple(start_state), tuple(alt_state)}
    
    # frontier stores: (current_belief, path, current_actual)
    frontier = deque([(initial_belief, [], start_state)])
    explored = {(tuple(sorted(initial_belief)), tuple(start_state))}
    nodes_generated = 1
    max_nodes = 30000
    
    found_path = None
    
    while frontier and nodes_generated < max_nodes:
        curr_belief, path, curr_actual = frontier.popleft()
        
        if len(curr_belief) == 1:
            belief_s = list(curr_belief)[0]
            if list(belief_s) == [1, 2, 3, 8, 0, 4, 7, 6, 5] or list(belief_s) == [1, 2, 3, 4, 5, 6, 7, 8, 0]:
                found_path = path
                break
            
        for action in ["Lên", "Xuống", "Trái", "Phải"]:
            next_actual = result_state(curr_actual, action)
            # Predict
            pred_belief = {tuple(result_state(s, action)) for s in curr_belief}
            # Update (Filter by blank position)
            percept = next_actual.index(0)
            next_belief = {s for s in pred_belief if s.index(0) == percept}
            
            state_key = (tuple(sorted(next_belief)), tuple(next_actual))
            if state_key not in explored:
                explored.add(state_key)
                nodes_generated += 1
                # Path stores actual_state and the first candidate in the belief state (or just the belief state subset)
                first_belief = list(next_belief)[0] if next_belief else next_actual
                frontier.append((next_belief, path + [(action, [next_actual, list(first_belief)])], next_actual))
                
    # Build logs
    log_data = []
    if found_path is not None:
        temp_belief = initial_belief
        temp_actual = start_state
        list_b = list(temp_belief)
        log_data.append({
            "step": 0,
            "action_html": f"Trạng thái niềm tin bắt đầu (Quan sát ô trống ở {temp_actual.index(0)}):",
            "frontier_str": format_two_states_ascii(list_b[0], list_b[1] if len(list_b) > 1 else list_b[0]),
            "reached_str": ""
        })
        for idx, (action, act_states) in enumerate(found_path):
            temp_actual = result_state(temp_actual, action)
            pred = {tuple(result_state(s, action)) for s in temp_belief}
            percept = temp_actual.index(0)
            temp_belief = {s for s in pred if s.index(0) == percept}
            
            list_b = list(temp_belief)
            log_data.append({
                "step": idx + 1,
                "action_html": f"Di chuyển ô trống sang <b>{action}</b> (Quan sát thấy ô trống ở vị trí {percept})",
                "frontier_str": format_two_states_ascii(list_b[0], list_b[1] if len(list_b) > 1 else list_b[0]),
                "reached_str": ""
            })
    else:
        log_data.append({
            "step": 0,
            "action_html": "Không tìm thấy giải pháp quan sát một phần.",
            "frontier_str": "",
            "reached_str": ""
        })
        
    return found_path, nodes_generated, log_data
