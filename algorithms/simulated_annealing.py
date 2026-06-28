import time
import random
import math

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
    count = 0
    for i in range(9):
        val = mt[i]
        if val != 0 and val != goal[i]:
            count += 1
    return count

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

def simulated_annealing_solve(start_state, goal_state, initial_temp=1000, cooling_rate=0.95, min_temp=1e-3, max_steps=10000):
    """
    Thuật toán Simulated Annealing (Luyện kim) cho 8-puzzle.
    Heuristic: Số ô sai vị trí. Nhiệt độ giảm dần (T = T * cooling_rate).
    """
    log_data = []
    def h(state): return count_misplaced(state, goal_state)
    h_label = "Số ô sai vị trí"
    nodes_generated = 1
    current_state = list(start_state)
    current_h = h(current_state)
    T = initial_temp
    path = []
    log_data.append({"step": 0, "action_html": f"Khởi tạo Simulated Annealing với T = {T}<br>Trạng thái bắt đầu: h({h_label}) = {current_h}", "frontier_str": f"T = {T:.2f}, h = {current_h}", "reached_str": ""})
    iteration = 0
    while T > min_temp and iteration < max_steps:
        iteration += 1
        if current_state == goal_state:
            log_data.append({"step": iteration, "action_html": f"Đạt được trạng thái Goal!<br>👉 THUẬT TOÁN DỪNG VÀ TRẢ VỀ THÀNH CÔNG 🎉", "frontier_str": "Đã đạt đích!", "reached_str": f"Thành công sau {iteration - 1} bước lặp!"})
            return path, nodes_generated, log_data
        successors = get_successors(current_state)
        if not successors:
            break
        action, next_state, _ = random.choice(successors)
        next_h = h(next_state)
        nodes_generated += 1
        delta_E = next_h - current_h
        action_html = f"<b>Bước lặp {iteration}</b> - T = {T:.4f}<br>"
        action_html += f"Sinh con ngẫu nhiên: {action} (h = {next_h})<br>"
        action_html += f"ΔE = {next_h} - {current_h} = {delta_E}<br>"
        accepted = False
        if delta_E < 0:
            accepted = True
            action_html += "ΔE < 0 ➔ <b>Chấp nhận 100%</b> (Đi xuống hướng tốt hơn)"
        elif delta_E == 0:
            accepted = True
            action_html += "ΔE = 0 ➔ <b>Chấp nhận</b> (Không đổi)"
        else:
            try:
                P = math.exp(-delta_E / T)
            except OverflowError:
                P = 0.0
            r = random.random()
            action_html += f"ΔE > 0 ➔ Xác suất chấp nhận P = e^(-{delta_E}/{T:.4f}) ≈ {P:.4f}<br>"
            action_html += f"Gieo số ngẫu nhiên r = {r:.4f}<br>"
            if r < P:
                accepted = True
                action_html += "r < P ➔ <b>Chấp nhận đi lùi</b> (Khám phá hướng tệ hơn)"
            else:
                action_html += "r ≥ P ➔ <b>Từ chối</b>"
        if accepted:
            current_state = next_state
            current_h = next_h
            path.append((action, current_state))
        log_data.append({"step": iteration, "action_html": action_html, "frontier_str": f"h = {current_h}", "reached_str": f"T = {T:.4f}"})
        T *= cooling_rate
    fail_html = f"<b style='color: #c53030;'>Nhiệt độ đã giảm về 0 hoặc vượt quá {max_steps} bước lặp mà chưa tìm ra lời giải!</b><br>"
    fail_html += f"👉 <b>THUẬT TOÁN DỪNG</b> ❌"
    log_data.append({"step": "KQ", "action_html": fail_html, "frontier_str": "Hết bước lặp / T ≈ 0!", "reached_str": f"Nodes: {nodes_generated}"})
    return path, nodes_generated, log_data
