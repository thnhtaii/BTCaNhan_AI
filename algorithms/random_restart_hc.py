import time
import random

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

def count_manhattan(mt, goal):
    dist = 0
    for i in range(9):
        val = mt[i]
        if val != 0:
            r, c = i // 3, i % 3
            goal_idx = goal.index(val)
            gr, gc = goal_idx // 3, goal_idx % 3
            dist += abs(r - gr) + abs(c - gc)
    return dist

def generate_random_state():
    state = list(range(9))
    random.shuffle(state)
    return state

def is_solvable(state, goal):
    def count_inversions(s):
        inv = 0
        s_no_zero = [x for x in s if x != 0]
        for i in range(len(s_no_zero)):
            for j in range(i + 1, len(s_no_zero)):
                if goal.index(s_no_zero[i]) > goal.index(s_no_zero[j]):
                    inv += 1
        return inv
    return count_inversions(state) % 2 == 0

def hill_climbing_one_run(start_state, goal_state):
    log_data = []
    def h(state): return count_manhattan(state, goal_state)
    h_label = "Manhattan"
    current_state = list(start_state)
    current_h = h(current_state)
    path = []
    nodes_generated = 1
    step_count = 0
    log_data.append({"step": 0, "action_html": f"Khởi tạo trạng thái bắt đầu với h({h_label}) = {current_h}", "frontier_str": f"Hiện tại: h={current_h}", "reached_str": f"Đường đi: [Start]"})
    while True:
        if current_state == goal_state:
            log_data.append({"step": step_count + 1, "action_html": f"Trạng thái hiện tại trùng khớp hoàn toàn với Goal.<br>THUẬT TOÁN DỪNG VÀ TRẢ VỀ THÀNH CÔNG", "frontier_str": "Đã đạt đích!", "reached_str": "Thành công!"})
            return path, nodes_generated, log_data, True
        successors = get_successors(current_state)
        children_logs = []
        better_neighbors = []
        for action, child, _ in successors:
            child_h = h(child)
            nodes_generated += 1
            if child_h < current_h:
                better_neighbors.append((action, child, child_h))
                status_str = f"<b style='color: #0d6e35;'>TỐT HƠN</b> (h={child_h} < h_hiện_tại={current_h})"
            else:
                status_str = f"<span style='color: #d62728;'>LOẠI</span> (h={child_h} >= h_hiện_tại={current_h})"
            children_logs.append((action, child_h, status_str))
        step_count += 1
        action_html = f"Bước {step_count} - Xét trạng thái hiện tại (h = {current_h}):<br>"
        action_html += f"Sinh ra {len(successors)} trạng thái lân cận và đánh giá:<br>"
        for act, ch, status in children_logs:
            action_html += f"- Di chuyển {act}: h = {ch} &rarr; {status}<br>"
        if better_neighbors:
            better_neighbors.sort(key=lambda x: x[2])
            chosen_action, chosen_state, chosen_h = better_neighbors[0]
            path.append((chosen_action, chosen_state))
            better_names = [f"{act}(h={ch})" for act, _, ch in better_neighbors]
            action_html += f"<br>Tập better_neighbors: [{', '.join(better_names)}]<br>"
            action_html += f"Chọn nút tốt nhất: Di chuyển <b>{chosen_action}</b> có h = {chosen_h}."
            current_state = chosen_state
            current_h = chosen_h
            log_data.append({"step": step_count, "action_html": action_html, "frontier_str": f"Hiện tại: h={current_h}", "reached_str": f"Đã đi {len(path)} bước"})
        else:
            action_html += f"<br><b style='color: #d62728;'>Tập better_neighbors RỖNG!</b> Không có nút con nào tốt hơn h_hiện_tại = {current_h}.<br>"
            action_html += f"<b>BỊ KẸT TẠI CỰC TRỊ ĐỊA PHƯƠNG (LOCAL OPTIMUM)</b><br>"
            action_html += f"Cần <b>RANDOM RESTART</b> - Tạo trạng thái mới ngẫu nhiên!"
            log_data.append({"step": step_count, "action_html": action_html, "frontier_str": f"Kẹt tại h={current_h}", "reached_str": "Cần restart!"})
            return path, nodes_generated, log_data, False

def random_restart_hill_climbing_solve(start_state, goal_state, max_restarts=20):
    """
    Thuật toán Random Restart Hill Climbing cho 8-puzzle.
    Khi bị kẹt tại cực trị địa phương, tạo trạng thái mới ngẫu nhiên và thử lại.
    """
    all_log_data = []
    total_nodes = 0
    best_path = None
    best_h = float('inf')
    current_start = list(start_state)
    for attempt in range(max_restarts + 1):
        if attempt == 0:
            attempt_html = f"<b style='color: #004ac6; font-size: 15px;'>LẦN THỬ {attempt + 1} (Trạng thái ban đầu)</b>"
        else:
            attempt_html = f"<b style='color: #e67e22; font-size: 15px;'>RANDOM RESTART - LẦN THỬ {attempt + 1}</b><br>"
            attempt_html += f"Tạo trạng thái ngẫu nhiên mới: {current_start}"
        all_log_data.append({"step": f"R{attempt + 1}", "action_html": attempt_html, "frontier_str": f"Lần thử {attempt + 1}/{max_restarts + 1}", "reached_str": f"Start: {current_start[:3]}|{current_start[3:6]}|{current_start[6:]}"})
        path, nodes, log_data, success = hill_climbing_one_run(current_start, goal_state)
        total_nodes += nodes
        all_log_data.extend(log_data)
        if success:
            final_summary = f"<b style='color: #0d6e35; font-size: 15px;'>THÀNH CÔNG sau {attempt + 1} lần thử!</b><br>"
            final_summary += f"Tổng số nút đã sinh: {total_nodes:,}<br>"
            final_summary += f"Số bước đi: {len(path)}"
            all_log_data.append({"step": "KQ", "action_html": final_summary, "frontier_str": "Hoàn thành!", "reached_str": f"{attempt + 1} lần thử, {len(path)} bước"})
            return path, total_nodes, all_log_data, attempt + 1, current_start
        if path:
            final_state = path[-1][1]
            final_h = count_manhattan(final_state, goal_state)
            if final_h < best_h:
                best_h = final_h
                best_path = path
        while True:
            new_state = generate_random_state()
            if is_solvable(new_state, goal_state):
                current_start = new_state
                break
    fail_summary = f"<b style='color: #c53030; font-size: 15px;'>THẤT BẠI sau {max_restarts + 1} lần thử!</b><br>"
    fail_summary += f"Tổng số nút đã sinh: {total_nodes:,}<br>"
    fail_summary += f"Kết quả tốt nhất: h = {best_h}"
    all_log_data.append({"step": "KQ", "action_html": fail_summary, "frontier_str": "Hết lần thử!", "reached_str": f"Tốt nhất: h={best_h}"})
    result_path = best_path if best_path else []
    return result_path, total_nodes, all_log_data, max_restarts + 1, current_start
