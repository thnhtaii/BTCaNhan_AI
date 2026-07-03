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
        return new_mt, new_mt[i]
        
    if c > 0: 
        new_state, cost = swap(mt, pos, pos - 1)
        successors.append(("Trái", new_state, cost))
    if c < 2: 
        new_state, cost = swap(mt, pos, pos + 1)
        successors.append(("Phải", new_state, cost))
    if r > 0: 
        new_state, cost = swap(mt, pos, pos - 3)
        successors.append(("Lên", new_state, cost))
    if r < 2: 
        new_state, cost = swap(mt, pos, pos + 3)
        successors.append(("Xuống", new_state, cost))
    return successors

def count_misplaced(mt, goal):
    """h(n): Đếm số ô sai vị trí so với trạng thái đích."""
    misplaced = 0
    for i in range(9):
        if mt[i] != 0 and mt[i] != goal[i]:
            misplaced += 1
    return misplaced

def count_manhattan(mt, goal):
    """h(n): Khoảng cách Manhattan."""
    dist = 0
    for i in range(9):
        val = mt[i]
        if val != 0:
            r, c = i // 3, i % 3
            goal_idx = goal.index(val)
            gr, gc = goal_idx // 3, goal_idx % 3
            dist += abs(r - gr) + abs(c - gc)
    return dist

def hill_climbing_solve(start_state, goal_state, heuristic_name="misplaced"):
    log_data = []
    
    # Lựa chọn hàm heuristic
    if heuristic_name == "manhattan":
        def h(state): return count_manhattan(state, goal_state)
        h_label = "Manhattan"
    else:
        def h(state): return count_misplaced(state, goal_state)
        h_label = "Số ô sai"
        
    current_state = list(start_state)
    current_h = h(current_state)
    
    path = [] 
    
    nodes_generated = 1
    step_count = 0

    log_data.append({
        "step": 0,
        "action_html": f"Khởi tạo trạng thái bắt đầu S với h({h_label}) = {current_h}",
        "frontier_str": f"Hiện tại: S(h={current_h})",
        "reached_str": f"Đường đi: [S]"
    })
    
    while True:
        if current_state == goal_state:
            action_html = f"Trạng thái hiện tại trùng khớp hoàn toàn với Goal.<br>THUẬT TOÁN DỪNG VÀ TRẢ VỀ THÀNH CÔNG"
            log_data.append({
                "step": step_count + 1,
                "action_html": action_html,
                "frontier_str": "Đã đạt đích!",
                "reached_str": "Thành công!"
            })
            break
            
        successors = get_successors(current_state)
        
        # Đánh giá toàn bộ các nút con kế cận (Steepest-Ascent)
        evaluated_children = []
        min_child_h = None
        best_child_idx = -1
        
        for idx, (action, child, _) in enumerate(successors):
            child_h = h(child)
            nodes_generated += 1
            evaluated_children.append((action, child, child_h))
            
            if min_child_h is None or child_h < min_child_h:
                min_child_h = child_h
                best_child_idx = idx
        
        # Nếu có các nút con, ta xác định nút tốt nhất
        found_better = False
        next_state = None
        next_action = None
        next_h = None
        
        children_logs = []
        
        if len(evaluated_children) > 0:
            best_action, best_state, best_h = evaluated_children[best_child_idx]
            if best_h < current_h:
                found_better = True
                next_state = best_state
                next_action = best_action
                next_h = best_h
            
            for idx, (action, child, child_h) in enumerate(evaluated_children):
                if child_h >= current_h:
                    status_str = f"<span style='color: #d62728;'>LOẠI</span> (h={child_h} &ge; h_hiện_tại={current_h})"
                else:
                    if idx == best_child_idx:
                        status_str = f"<b style='color: #0d6e35;'>TỐT NHẤT (DỐC NHẤT)</b> (h={child_h} &lt; h_hiện_tại={current_h})"
                    else:
                        status_str = f"<span style='color: #a0a0a0;'>KHÔNG CHỌN</span> (Tốt hơn hiện tại nhưng không dốc nhất: h={child_h} &gt; h_tốt_nhất={best_h})"
                children_logs.append((action, child_h, status_str))
        
        # Xây dựng action_html 
        step_count += 1
        curr_name = "S" if step_count == 1 else f"N_{step_count-1}"
        next_name = f"N_{step_count}"
        
        action_html = f"Xét trạng thái hiện tại {curr_name} (h = {current_h}):<br>"
        action_html += f"Sinh ra và đánh giá TOÀN BỘ {len(successors)} nút con:<br>"
        for act, ch, status in children_logs:
            action_html += f"- Di chuyển {act}: h = {ch} &rarr; {status}<br>"
            
        if found_better:
            path.append((next_action, next_state))
            
            action_html += f"<br>Di chuyển sang hướng dốc nhất {next_action} ({next_name}) có h = {next_h}."
            
            # Cập nhật trạng thái hiện tại
            current_state = next_state
            current_h = next_h
            
            path_names = ["S"] + [f"N_{i+1}" for i in range(len(path))]
            log_data.append({
                "step": step_count,
                "action_html": action_html,
                "frontier_str": f"Hiện tại: {next_name}(h={current_h})",
                "reached_str": " &rarr; ".join(path_names)
            })
        else:
            if len(evaluated_children) > 0:
                best_action, best_state, best_h = evaluated_children[best_child_idx]
                action_html += f"<br><b style='color: #d62728;'>CẢNH BÁO:</b> Nút con tốt nhất có h_tốt_nhất = {best_h} không tốt hơn h_hiện_tại = {current_h}!<br>"
            else:
                action_html += f"<br><b style='color: #d62728;'>CẢNH BÁO:</b> Không có nút con nào được sinh ra!<br>"
            action_html += f"<b>THUẬT TOÁN DỪNG VÀ BỊ KẸT TẠI CỰC TRỊ ĐỊA PHƯƠNG (LOCAL OPTIMUM)</b>"
            log_data.append({
                "step": step_count,
                "action_html": action_html,
                "frontier_str": f"Bị kẹt tại: {curr_name}(h={current_h})",
                "reached_str": "Kẹt cực trị địa phương!"
            })
            break
            
    return path, nodes_generated, log_data
